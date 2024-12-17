import os
import subprocess
from os import getcwd
from pathlib import Path
from typing import Optional

import click
import requests

from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.cicd import init_cicd
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import _generate_datafile, check_user_token, coro, generate_datafile
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.fixture import build_fixture_name, persist_fixture
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.llm import LLM


@cli.command()
@click.option(
    "--demo",
    is_flag=True,
    help="Demo data and files to get started",
)
@click.option(
    "--data",
    type=click.Path(exists=True),
    default=None,
    help="Initial data to be used to create the project",
)
@click.option(
    "--prompt",
    type=str,
    default=None,
    help="Prompt to be used to create the project",
)
@click.option(
    "--folder",
    default=None,
    type=click.Path(exists=True, file_okay=False),
    help="Folder where datafiles will be placed",
)
@click.option("--rows", type=int, default=10, help="Number of events to send")
@click.pass_context
@coro
async def create(
    ctx: click.Context,
    demo: bool,
    data: Optional[str],
    prompt: Optional[str],
    folder: Optional[str],
    rows: int,
) -> None:
    """Initialize a new project."""
    folder = folder or getcwd()
    try:
        config = CLIConfig.get_project_config(folder)

        if prompt:
            user_token = config.get_user_token()
            try:
                await check_user_token(ctx, token=user_token)
            except Exception:
                click.echo(FeedbackManager.error(message="This action requires authentication. Run 'tb login' first."))
                return

        tb_client = config.get_client()
        click.echo(FeedbackManager.gray(message="Creating new project structure..."))
        await project_create(tb_client, data, prompt, folder)
        click.echo(FeedbackManager.success(message="✓ Scaffolding completed!\n"))

        click.echo(FeedbackManager.gray(message="\nCreating CI/CD files for GitHub and GitLab..."))
        init_git(folder)
        await init_cicd(data_project_dir=os.path.relpath(folder))
        click.echo(FeedbackManager.success(message="✓ Done!\n"))

        click.echo(FeedbackManager.gray(message="Building fixtures..."))

        if demo:
            # Users datasource
            ds_name = "users"
            datasource_path = Path(folder) / "datasources" / f"{ds_name}.datasource"
            datasource_content = fetch_gist_content(
                "https://gist.githubusercontent.com/gnzjgo/b48fb9c92825ed27c04e3104b9e871e1/raw/1f33c20eefbabc4903f38e234329e028d8ef9def/users.datasource"
            )
            datasource_path.write_text(datasource_content)
            click.echo(FeedbackManager.info(message=f"✓ /datasources/{ds_name}.datasource"))

            # Users fixtures
            fixture_content = fetch_gist_content(
                "https://gist.githubusercontent.com/gnzjgo/8e8f66a39d7576ce3a2529bf773334a8/raw/9cab636767990e97d44a141867e5f226e992de8c/users.ndjson"
            )
            fixture_name = build_fixture_name(datasource_path.absolute(), ds_name, datasource_path.read_text())
            persist_fixture(fixture_name, fixture_content)
            click.echo(FeedbackManager.info(message=f"✓ /fixtures/{ds_name}"))

            # Events datasource
            ds_name = "events"
            datasource_path = Path(folder) / "datasources" / f"{ds_name}.datasource"
            datasource_content = fetch_gist_content(
                "https://gist.githubusercontent.com/gnzjgo/f8ca37b5b1f6707c75206b618de26bc9/raw/cd625da0dcd1ba8de29f12bc1c8600b9ff7c809c/events.datasource"
            )
            datasource_path.write_text(datasource_content)
            click.echo(FeedbackManager.info(message=f"✓ /datasources/{ds_name}.datasource"))

            # Events fixtures
            fixture_content = fetch_gist_content(
                "https://gist.githubusercontent.com/gnzjgo/859ab9439c17e77241d0c14a5a532809/raw/251f2f3f00a968f8759ec4068cebde915256b054/events.ndjson"
            )
            fixture_name = build_fixture_name(datasource_path.absolute(), ds_name, datasource_path.read_text())
            persist_fixture(fixture_name, fixture_content)
            click.echo(FeedbackManager.info(message=f"✓ /fixtures/{ds_name}"))

            # Create sample endpoint
            pipe_name = "api_token_usage"
            pipe_path = Path(folder) / "endpoints" / f"{pipe_name}.pipe"
            pipe_content = fetch_gist_content(
                "https://gist.githubusercontent.com/gnzjgo/68ecc47472c2b754b0ae0c1187022963/raw/52cc3aa3afdf939e58d43355bfe4ddc739989ddd/api_token_usage.pipe"
            )
            pipe_path.write_text(pipe_content)
            click.echo(FeedbackManager.info(message=f"✓ /endpoints/{pipe_name}.pipe"))

            # Create sample test
            test_name = "api_token_usage"
            test_path = Path(folder) / "tests" / f"{test_name}.yaml"
            test_content = fetch_gist_content(
                "https://gist.githubusercontent.com/gnzjgo/e58620bbb977d6f42f1d0c2a7b46ac8f/raw/a5f61d5019111f937484f941111829dfce69f648/api_token_usage.yaml"
            )
            test_path.write_text(test_content)
            click.echo(FeedbackManager.info(message=f"✓ /tests/{test_name}.yaml"))

        elif data:
            ds_name = os.path.basename(data.split(".")[0])
            data_content = Path(data).read_text()
            datasource_path = Path(folder) / "datasources" / f"{ds_name}.datasource"
            fixture_name = build_fixture_name(datasource_path.absolute(), ds_name, datasource_path.read_text())
            click.echo(FeedbackManager.info(message=f"✓ /fixtures/{ds_name}"))
            persist_fixture(fixture_name, data_content)
        elif prompt:
            datasource_files = [f for f in os.listdir(Path(folder) / "datasources") if f.endswith(".datasource")]
            for datasource_file in datasource_files:
                datasource_path = Path(folder) / "datasources" / datasource_file
                llm = LLM(client=tb_client)
                datasource_name = datasource_path.stem
                datasource_content = datasource_path.read_text()
                has_json_path = "`json:" in datasource_content
                if has_json_path:
                    sql = await llm.generate_sql_sample_data(schema=datasource_content, rows=rows, context=prompt)
                    result = await tb_client.query(f"{sql} FORMAT JSON")
                    data = result.get("data", [])
                    fixture_name = build_fixture_name(datasource_path.absolute(), datasource_name, datasource_content)
                    persist_fixture(fixture_name, data)
                    click.echo(FeedbackManager.info(message=f"✓ /fixtures/{datasource_name}"))

        click.echo(FeedbackManager.success(message="✓ Done!\n"))
    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Error: {str(e)}"))


async def project_create(
    client: TinyB,
    data: Optional[str],
    prompt: Optional[str],
    folder: str,
):
    project_paths = ["datasources", "endpoints", "materializations", "copies", "sinks", "fixtures", "tests"]
    force = True
    for x in project_paths:
        try:
            f = Path(folder) / x
            f.mkdir()
        except FileExistsError:
            pass
        click.echo(FeedbackManager.info_path_created(path=x))

    if data:
        path = Path(folder) / data
        format = path.suffix.lstrip(".")
        try:
            await _generate_datafile(str(path), client, format=format, force=force)
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"Error: {str(e)}"))
        name = data.split(".")[0]
        generate_pipe_file(
            f"{name}_endpoint",
            f"""
NODE endpoint
SQL >
    SELECT * from {name}
TYPE ENDPOINT
            """,
            folder,
        )
    elif prompt:
        try:
            llm = LLM(client=client)
            result = await llm.create_project(prompt)
            for ds in result.datasources:
                content = ds.content.replace("```", "")
                generate_datafile(
                    content, filename=f"{ds.name}.datasource", data=None, _format="ndjson", force=force, folder=folder
                )

            for pipe in result.pipes:
                content = pipe.content.replace("```", "")
                generate_pipe_file(pipe.name, content, folder)
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"Error: {str(e)}"))


def init_git(folder: str):
    try:
        path = Path(folder)
        gitignore_file = path / ".gitignore"
        git_folder = path / ".git"
        if not git_folder.exists():
            subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)

        if gitignore_file.exists():
            content = gitignore_file.read_text()
            if ".tinyb" not in content:
                gitignore_file.write_text(content + "\n.tinyb\n")
        else:
            gitignore_file.write_text(".tinyb\n")

        click.echo(FeedbackManager.info_file_created(file=".gitignore"))
    except Exception as e:
        raise CLIException(f"Error initializing Git: {e}")


def generate_pipe_file(name: str, content: str, folder: str):
    base = Path(folder) / "endpoints"
    if not base.exists():
        base = Path()
    f = base / (f"{name}.pipe")
    with open(f"{f}", "w") as file:
        file.write(content)
    click.echo(FeedbackManager.info_file_created(file=f.relative_to(folder)))


def fetch_gist_content(url: str) -> str:  # TODO: replace this with a function that fetches the content from a repo
    response = requests.get(url)
    response.raise_for_status()
    return response.text
