import asyncio
import os
import threading
import time
from pathlib import Path
from typing import Any, Awaitable, Callable, List, Union

import click
from click import Context
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import tinybird.context as context
from tinybird.client import TinyB
from tinybird.config import FeatureFlags
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.build_shell import BuildShell, print_table_formatted
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import coro, push_data
from tinybird.tb.modules.datafile.build import folder_build
from tinybird.tb.modules.datafile.common import get_project_filenames, get_project_fixtures, has_internal_datafiles
from tinybird.tb.modules.datafile.exceptions import ParseException
from tinybird.tb.modules.datafile.fixture import build_fixture_name, get_fixture_dir
from tinybird.tb.modules.datafile.parse_datasource import parse_datasource
from tinybird.tb.modules.datafile.parse_pipe import parse_pipe
from tinybird.tb.modules.local_common import get_tinybird_local_client


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filenames: List[str], process: Callable[[List[str]], None]):
        self.filenames = filenames
        self.process = process

    def on_modified(self, event: Any) -> None:
        is_not_vendor = "vendor/" not in event.src_path
        if (
            is_not_vendor
            and not event.is_directory
            and any(event.src_path.endswith(ext) for ext in [".datasource", ".pipe", ".ndjson"])
        ):
            filename = event.src_path.split("/")[-1]
            click.echo(FeedbackManager.highlight(message=f"\n\n⟲ Changes detected in {filename}\n"))
            try:
                self.process([event.src_path])
            except Exception as e:
                click.echo(FeedbackManager.error_exception(error=e))


def watch_files(
    filenames: List[str],
    process: Union[Callable[[List[str]], None], Callable[[List[str]], Awaitable[None]]],
    shell: BuildShell,
    folder: str,
) -> None:
    # Handle both sync and async process functions
    async def process_wrapper(files: List[str]) -> None:
        click.echo("⚡ Rebuilding...")
        time_start = time.time()
        if asyncio.iscoroutinefunction(process):
            await process(files, watch=True)
        else:
            process(files, watch=True)
        time_end = time.time()
        elapsed_time = time_end - time_start
        click.echo(
            FeedbackManager.success(message="\n✓ ")
            + FeedbackManager.gray(message=f"Rebuild completed in {elapsed_time:.1f}s")
        )
        shell.reprint_prompt()

    event_handler = FileChangeHandler(filenames, lambda f: asyncio.run(process_wrapper(f)))
    observer = Observer()

    observer.schedule(event_handler, path=folder, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


@cli.command()
@click.option(
    "--folder",
    default=".",
    help="Folder from where to execute the command. By default the current folder",
    hidden=True,
    type=click.types.STRING,
)
@click.option(
    "--watch",
    is_flag=True,
    help="Watch for changes in the files and re-check them.",
)
@click.pass_context
@coro
async def build(
    ctx: Context,
    folder: str,
    watch: bool,
) -> None:
    """
    Watch for changes in the files and re-check them.
    """
    ignore_sql_errors = FeatureFlags.ignore_sql_errors()
    context.disable_template_security_validation.set(True)
    is_internal = has_internal_datafiles(folder)

    folder_path = os.path.abspath(folder)
    tb_client = await get_tinybird_local_client(folder_path)

    def check_filenames(filenames: List[str]):
        parser_matrix = {".pipe": parse_pipe, ".datasource": parse_datasource}
        incl_suffix = ".incl"

        for filename in filenames:
            if os.path.isdir(filename):
                process(filenames=get_project_filenames(filename))

            file_suffix = Path(filename).suffix
            if file_suffix == incl_suffix:
                continue

            parser = parser_matrix.get(file_suffix)
            if not parser:
                raise ParseException(FeedbackManager.error_unsupported_datafile(extension=file_suffix))

            parser(filename)

    async def process(filenames: List[str], watch: bool = False):
        datafiles = [f for f in filenames if f.endswith(".datasource") or f.endswith(".pipe")]
        if len(datafiles) > 0:
            check_filenames(filenames=datafiles)
            await folder_build(
                tb_client,
                filenames=datafiles,
                ignore_sql_errors=ignore_sql_errors,
                is_internal=is_internal,
                watch=watch,
            )

        filename = filenames[0]
        if filename.endswith(".ndjson"):
            fixture_path = Path(filename)
            name = "_".join(fixture_path.stem.split("_")[:-1])
            ds_path = Path(folder) / "datasources" / f"{name}.datasource"
            if ds_path.exists():
                await append_datasource({}, tb_client, name, str(fixture_path), silent=True)

        if watch:
            if filename.endswith(".datasource"):
                ds_path = Path(filename)
                name = build_fixture_name(filename, ds_path.stem, ds_path.read_text())
                fixture_path = get_fixture_dir() / f"{name}.ndjson"
                if fixture_path.exists():
                    await append_datasource({}, tb_client, ds_path.stem, str(fixture_path), silent=True)
            if not filename.endswith(".ndjson"):
                await build_and_print_resource(tb_client, filename)

    datafiles = get_project_filenames(folder)
    fixtures = get_project_fixtures(folder)
    filenames = datafiles + fixtures

    async def build_once(filenames: List[str]):
        try:
            click.echo("⚡ Building project...\n")
            time_start = time.time()
            await process(filenames=filenames, watch=False)
            time_end = time.time()
            elapsed_time = time_end - time_start
            for filename in filenames:
                if filename.endswith(".datasource"):
                    ds_path = Path(filename)
                    name = build_fixture_name(filename, ds_path.stem, ds_path.read_text())
                    fixture_path = get_fixture_dir() / f"{name}.ndjson"
                    if fixture_path.exists():
                        await append_datasource({}, tb_client, ds_path.stem, str(fixture_path), silent=True)
            click.echo(FeedbackManager.success(message=f"\n✓ Build completed in {elapsed_time:.1f}s\n"))
        except Exception as e:
            click.echo(FeedbackManager.error(message=str(e)))

    await build_once(filenames)

    if watch:
        shell = BuildShell(folder=folder, client=tb_client)
        click.echo(FeedbackManager.highlight(message="◎ Watching for changes..."))
        watcher_thread = threading.Thread(target=watch_files, args=(filenames, process, shell, folder), daemon=True)
        watcher_thread.start()
        shell.cmdloop()


async def build_and_print_resource(tb_client: TinyB, filename: str):
    resource_path = Path(filename)
    name = resource_path.stem
    pipeline = name if filename.endswith(".pipe") else None
    res = await tb_client.query(f"SELECT * FROM {name} FORMAT JSON", pipeline=pipeline)
    print_table_formatted(res, name)


async def append_datasource(
    ctx: click.Context,
    tb_client: TinyB,
    datasource_name: str,
    url: str,
    silent: bool = False,
):
    await push_data(
        ctx,
        tb_client,
        datasource_name,
        url,
        connector=None,
        sql=None,
        mode="append",
        ignore_empty=False,
        concurrency=1,
        silent=silent,
    )
