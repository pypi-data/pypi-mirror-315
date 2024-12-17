import asyncio
import cmd
import random
import subprocess
import sys

import click
import humanfriendly

from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager, bcolors
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.table import format_table


class BuildShell(cmd.Cmd):
    prompt = "\n\001\033[1;32m\002tb > \001\033[0m\002"

    def __init__(self, folder: str, client: TinyB):
        super().__init__()
        self.folder = folder
        self.client = client

    def do_exit(self, arg):
        sys.exit(0)

    def do_quit(self, arg):
        sys.exit(0)

    def do_build(self, arg):
        click.echo(FeedbackManager.error(message=f"'tb {arg}' command is not available in watch mode"))

    def do_auth(self, arg):
        click.echo(FeedbackManager.error(message=f"'tb {arg}' command is not available in watch mode"))

    def do_workspace(self, arg):
        click.echo(FeedbackManager.error(message=f"'tb {arg}' command is not available in watch mode"))

    def do_mock(self, arg):
        subprocess.run(f"tb mock {arg} --folder {self.folder}", shell=True, text=True)

    def do_tb(self, arg):
        click.echo("")
        arg = arg.strip().lower()
        if arg.startswith("build"):
            self.do_build(arg)
        elif arg.startswith("auth"):
            self.do_auth(arg)
        elif arg.startswith("workspace"):
            self.do_workspace(arg)
        elif arg.startswith("mock"):
            self.do_mock(arg)
        else:
            subprocess.run(f"tb --local {arg}", shell=True, text=True)

    def default(self, argline):
        click.echo("")
        arg = argline.strip().lower()
        if not arg:
            return
        if arg.startswith("with") or arg.startswith("select"):
            try:
                self.run_sql(argline)
            except Exception as e:
                click.echo(FeedbackManager.error(message=str(e)))
        else:
            subprocess.run(f"tb --local {arg}", shell=True, text=True)

    def reprint_prompt(self):
        self.stdout.write(self.prompt)
        self.stdout.flush()

    def run_sql(self, query, rows_limit=20):
        try:
            q = query.strip()
            if q.startswith("insert"):
                click.echo(FeedbackManager.info_append_data())
                raise CLIException(FeedbackManager.error_invalid_query())
            if q.startswith("delete"):
                raise CLIException(FeedbackManager.error_invalid_query())

            # fuck my life
            def run_query_in_thread():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(
                        self.client.query(f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT JSON")
                    )
                finally:
                    loop.close()

            # Run the query in a separate thread
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                res = executor.submit(run_query_in_thread).result()

        except Exception as e:
            raise CLIException(FeedbackManager.error_exception(error=str(e)))

        if isinstance(res, dict) and "error" in res:
            raise CLIException(FeedbackManager.error_exception(error=res["error"]))

        if isinstance(res, dict) and "data" in res and res["data"]:
            print_table_formatted(res, "QUERY")
        else:
            click.echo(FeedbackManager.info_no_rows())


def print_table_formatted(res: dict, name: str):
    rebuild_colors = [bcolors.FAIL, bcolors.OKBLUE, bcolors.WARNING, bcolors.OKGREEN, bcolors.HEADER]
    rebuild_index = random.randint(0, len(rebuild_colors) - 1)
    rebuild_color = rebuild_colors[rebuild_index % len(rebuild_colors)]
    data = []
    limit = 5
    for d in res["data"][:5]:
        data.append(d.values())
    meta = res["meta"]
    row_count = res.get("rows", 0)
    stats = res.get("statistics", {})
    elapsed = stats.get("elapsed", 0)
    cols = len(meta)
    try:

        def print_message(message: str, color=bcolors.CGREY):
            return f"{color}{message}{bcolors.ENDC}"

        table = format_table(data, meta)
        colored_char = print_message("│", rebuild_color)
        table_with_marker = "\n".join(f"{colored_char} {line}" for line in table.split("\n"))
        click.echo(f"\n{colored_char} {print_message('⚡', rebuild_color)} Running {name}")
        click.echo(colored_char)
        click.echo(table_with_marker)
        click.echo(colored_char)
        rows_read = humanfriendly.format_number(stats.get("rows_read", 0))
        bytes_read = humanfriendly.format_size(stats.get("bytes_read", 0))
        elapsed = humanfriendly.format_timespan(elapsed) if elapsed >= 1 else f"{elapsed * 1000:.2f}ms"
        stats_message = f"» {bytes_read} ({rows_read} rows x {cols} cols) in {elapsed}"
        rows_message = f"» Showing {limit} first rows" if row_count > limit else "» Showing all rows"
        click.echo(f"{colored_char} {print_message(stats_message, bcolors.OKGREEN)}")
        click.echo(f"{colored_char} {print_message(rows_message, bcolors.CGREY)}")
    except ValueError as exc:
        if str(exc) == "max() arg is an empty sequence":
            click.echo("------------")
            click.echo("Empty")
            click.echo("------------")
        else:
            raise exc
