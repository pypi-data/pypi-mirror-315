import os
import subprocess
from os import getcwd
from pathlib import Path
from typing import Optional

import click
from click import Context

from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.cicd import init_cicd
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import _generate_datafile, coro, generate_datafile
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
    ctx: Context,
    demo: bool,
    data: Optional[str],
    prompt: Optional[str],
    folder: Optional[str],
    rows: int,
) -> None:
    """Initialize a new project."""
    folder = folder or getcwd()
    try:
        config = CLIConfig.get_project_config()
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
            datasource_content = """SCHEMA >
    `id` String `json:$.id`,
    `organization_id` String `json:$.organization_id`,
    `tier` String `json:$.tier`

ENGINE "MergeTree"
ENGINE_SORTING_KEY "id, organization_id"
"""
            datasource_path.write_text(datasource_content)
            click.echo(FeedbackManager.info(message=f"✓ /datasources/{ds_name}.datasource"))

            # Events datasource
            ds_name = "events"
            datasource_path = Path(folder) / "datasources" / f"{ds_name}.datasource"
            datasource_content = """SCHEMA >
    `request_id` String `json:$.request_id`,
    `timestamp` DateTime64(3) `json:$.timestamp`,
    `user_id` String `json:$.user_id`,
    `type` String `json:$.request.type`,
    `endpoint` String `json:$.request.endpoint`,
    `model` String `json:$.request.model`,
    `request_options_temperature` String `json:$.request.options.temperature`,
    `request_options_max_tokens` Int32 `json:$.request.options.max_tokens`,
    `request_options_stream` Boolean `json:$.request.options.stream`,
    `usage_prompt_tokens` Int32 `json:$.usage.prompt_tokens`,
    `usage_completion_tokens` Int32 `json:$.usage.completion_tokens`,
    `usage_total_tokens` Int32 `json:$.usage.total_tokens`

ENGINE "MergeTree"
ENGINE_SORTING_KEY "user_id, timestamp"
"""
            datasource_path.write_text(datasource_content)
            click.echo(FeedbackManager.info(message=f"✓ /datasources/{ds_name}.datasource"))

            ds_name = "users"
            ds_content = """
{"id":"usr_1","organization_id":"org_202","tier":"pro"}
{"id":"usr_2","organization_id":"org_49","tier":"enterprise"}
{"id":"usr_3","organization_id":"org_181","tier":"pro"}
{"id":"usr_4","organization_id":"org_194","tier":"pro"}
{"id":"usr_5","organization_id":"org_180","tier":"enterprise"}
{"id":"usr_6","organization_id":"org_112","tier":"enterprise"}
{"id":"usr_7","organization_id":"org_291","tier":"pro"}
{"id":"usr_8","organization_id":"org_150","tier":"free"}
{"id":"usr_9","organization_id":"org_127","tier":"enterprise"}
{"id":"usr_10","organization_id":"org_279","tier":"enterprise"}
{"id":"usr_11","organization_id":"org_58","tier":"pro"}
{"id":"usr_12","organization_id":"org_183","tier":"pro"}
{"id":"usr_13","organization_id":"org_2","tier":"pro"}
{"id":"usr_14","organization_id":"org_15","tier":"free"}
{"id":"usr_15","organization_id":"org_54","tier":"pro"}
{"id":"usr_16","organization_id":"org_24","tier":"pro"}
{"id":"usr_17","organization_id":"org_135","tier":"free"}
{"id":"usr_18","organization_id":"org_76","tier":"enterprise"}
{"id":"usr_19","organization_id":"org_166","tier":"enterprise"}
{"id":"usr_20","organization_id":"org_203","tier":"pro"}
{"id":"usr_21","organization_id":"org_103","tier":"pro"}
{"id":"usr_22","organization_id":"org_178","tier":"pro"}
{"id":"usr_23","organization_id":"org_41","tier":"pro"}
{"id":"usr_24","organization_id":"org_197","tier":"enterprise"}
{"id":"usr_25","organization_id":"org_21","tier":"pro"}
{"id":"usr_26","organization_id":"org_180","tier":"enterprise"}
{"id":"usr_27","organization_id":"org_216","tier":"enterprise"}
{"id":"usr_28","organization_id":"org_117","tier":"enterprise"}
{"id":"usr_29","organization_id":"org_73","tier":"pro"}
{"id":"usr_30","organization_id":"org_92","tier":"enterprise"}
{"id":"usr_31","organization_id":"org_272","tier":"enterprise"}
{"id":"usr_32","organization_id":"org_58","tier":"pro"}
{"id":"usr_33","organization_id":"org_158","tier":"pro"}
{"id":"usr_34","organization_id":"org_12","tier":"free"}
{"id":"usr_35","organization_id":"org_119","tier":"free"}
{"id":"usr_36","organization_id":"org_272","tier":"pro"}
{"id":"usr_37","organization_id":"org_1","tier":"enterprise"}
{"id":"usr_38","organization_id":"org_262","tier":"enterprise"}
{"id":"usr_39","organization_id":"org_189","tier":"pro"}
{"id":"usr_40","organization_id":"org_126","tier":"free"}
{"id":"usr_41","organization_id":"org_94","tier":"free"}
{"id":"usr_42","organization_id":"org_156","tier":"free"}
{"id":"usr_43","organization_id":"org_155","tier":"enterprise"}
{"id":"usr_44","organization_id":"org_151","tier":"pro"}
{"id":"usr_45","organization_id":"org_217","tier":"pro"}
{"id":"usr_46","organization_id":"org_111","tier":"enterprise"}
{"id":"usr_47","organization_id":"org_274","tier":"enterprise"}
{"id":"usr_48","organization_id":"org_117","tier":"enterprise"}
{"id":"usr_49","organization_id":"org_125","tier":"pro"}
{"id":"usr_50","organization_id":"org_42","tier":"pro"}
"""
            persist_fixture(f"{ds_name}", ds_content)
            click.echo(FeedbackManager.info(message=f"✓ /fixtures/{ds_name}"))

            ds_name = "events"
            ds_content = """
{"request_id":"req_1","timestamp":"2024-11-14T12:11:14.896Z","user_id":"usr_42","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-4","options":{"temperature":"0.8","max_tokens":1582,"stream":false}},"usage":{"prompt_tokens":499,"completion_tokens":123,"total_tokens":622}}
{"request_id":"req_2","timestamp":"2024-10-06T10:32:09.164Z","user_id":"usr_20","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"0.9","max_tokens":650,"stream":true}},"usage":{"prompt_tokens":384,"completion_tokens":103,"total_tokens":487}}
{"request_id":"req_3","timestamp":"2024-11-19T03:49:26.569Z","user_id":"usr_27","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"0.3","max_tokens":764,"stream":true}},"usage":{"prompt_tokens":63,"completion_tokens":284,"total_tokens":347}}
{"request_id":"req_4","timestamp":"2024-11-09T09:13:05.359Z","user_id":"usr_8","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.8","max_tokens":1790,"stream":true}},"usage":{"prompt_tokens":405,"completion_tokens":231,"total_tokens":636}}
{"request_id":"req_5","timestamp":"2024-11-24T17:48:03.640Z","user_id":"usr_45","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"1.0","max_tokens":1701,"stream":false}},"usage":{"prompt_tokens":342,"completion_tokens":258,"total_tokens":600}}
{"request_id":"req_6","timestamp":"2024-11-10T02:07:53.241Z","user_id":"usr_49","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.4","max_tokens":1049,"stream":false}},"usage":{"prompt_tokens":120,"completion_tokens":165,"total_tokens":285}}
{"request_id":"req_7","timestamp":"2024-10-14T06:43:14.759Z","user_id":"usr_48","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-4","options":{"temperature":"0.9","max_tokens":1548,"stream":true}},"usage":{"prompt_tokens":61,"completion_tokens":104,"total_tokens":165}}
{"request_id":"req_8","timestamp":"2024-11-21T20:52:03.378Z","user_id":"usr_30","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.5","max_tokens":1742,"stream":true}},"usage":{"prompt_tokens":326,"completion_tokens":236,"total_tokens":562}}
{"request_id":"req_9","timestamp":"2024-10-24T22:23:11.463Z","user_id":"usr_34","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"0.5","max_tokens":748,"stream":true}},"usage":{"prompt_tokens":488,"completion_tokens":148,"total_tokens":636}}
{"request_id":"req_10","timestamp":"2024-11-13T05:42:38.971Z","user_id":"usr_24","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.3","max_tokens":1729,"stream":true}},"usage":{"prompt_tokens":262,"completion_tokens":162,"total_tokens":424}}
{"request_id":"req_11","timestamp":"2024-10-21T07:20:51.693Z","user_id":"usr_1","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-opus","options":{"temperature":"0.3","max_tokens":1811,"stream":false}},"usage":{"prompt_tokens":342,"completion_tokens":274,"total_tokens":616}}
{"request_id":"req_12","timestamp":"2024-11-15T06:03:07.775Z","user_id":"usr_21","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-4","options":{"temperature":"0.3","max_tokens":1484,"stream":true}},"usage":{"prompt_tokens":273,"completion_tokens":266,"total_tokens":539}}
{"request_id":"req_13","timestamp":"2024-11-29T18:31:23.125Z","user_id":"usr_41","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"0.8","max_tokens":1812,"stream":true}},"usage":{"prompt_tokens":265,"completion_tokens":102,"total_tokens":367}}
{"request_id":"req_14","timestamp":"2024-11-13T23:50:03.888Z","user_id":"usr_13","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.9","max_tokens":1694,"stream":false}},"usage":{"prompt_tokens":76,"completion_tokens":290,"total_tokens":366}}
{"request_id":"req_15","timestamp":"2024-11-01T14:27:22.401Z","user_id":"usr_32","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-sonnet","options":{"temperature":"0.4","max_tokens":949,"stream":true}},"usage":{"prompt_tokens":105,"completion_tokens":197,"total_tokens":302}}
{"request_id":"req_16","timestamp":"2024-11-12T09:13:06.447Z","user_id":"usr_2","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"0.1","max_tokens":651,"stream":false}},"usage":{"prompt_tokens":348,"completion_tokens":80,"total_tokens":428}}
{"request_id":"req_17","timestamp":"2024-11-09T21:09:51.044Z","user_id":"usr_24","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.4","max_tokens":692,"stream":false}},"usage":{"prompt_tokens":195,"completion_tokens":178,"total_tokens":373}}
{"request_id":"req_18","timestamp":"2024-11-06T13:38:08.873Z","user_id":"usr_49","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-opus","options":{"temperature":"0.4","max_tokens":1303,"stream":true}},"usage":{"prompt_tokens":304,"completion_tokens":73,"total_tokens":377}}
{"request_id":"req_19","timestamp":"2024-11-06T20:47:35.718Z","user_id":"usr_33","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"0.8","max_tokens":1359,"stream":true}},"usage":{"prompt_tokens":55,"completion_tokens":258,"total_tokens":313}}
{"request_id":"req_20","timestamp":"2024-11-15T09:59:27.956Z","user_id":"usr_9","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-opus","options":{"temperature":"0.6","max_tokens":1768,"stream":true}},"usage":{"prompt_tokens":310,"completion_tokens":62,"total_tokens":372}}
{"request_id":"req_21","timestamp":"2024-11-17T03:46:10.219Z","user_id":"usr_6","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"0.8","max_tokens":1967,"stream":true}},"usage":{"prompt_tokens":87,"completion_tokens":275,"total_tokens":362}}
{"request_id":"req_22","timestamp":"2024-10-03T06:52:21.902Z","user_id":"usr_13","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.8","max_tokens":1338,"stream":true}},"usage":{"prompt_tokens":332,"completion_tokens":137,"total_tokens":469}}
{"request_id":"req_23","timestamp":"2024-11-10T02:53:06.630Z","user_id":"usr_16","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-opus","options":{"temperature":"0.1","max_tokens":1958,"stream":true}},"usage":{"prompt_tokens":444,"completion_tokens":294,"total_tokens":738}}
{"request_id":"req_24","timestamp":"2024-10-10T04:11:45.410Z","user_id":"usr_44","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"1.0","max_tokens":1241,"stream":false}},"usage":{"prompt_tokens":414,"completion_tokens":227,"total_tokens":641}}
{"request_id":"req_25","timestamp":"2024-10-15T09:53:09.379Z","user_id":"usr_24","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"0.4","max_tokens":1015,"stream":true}},"usage":{"prompt_tokens":433,"completion_tokens":119,"total_tokens":552}}
{"request_id":"req_26","timestamp":"2024-11-16T16:40:38.042Z","user_id":"usr_8","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"0.3","max_tokens":514,"stream":true}},"usage":{"prompt_tokens":86,"completion_tokens":241,"total_tokens":327}}
{"request_id":"req_27","timestamp":"2024-10-06T11:34:58.073Z","user_id":"usr_40","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.7","max_tokens":1752,"stream":true}},"usage":{"prompt_tokens":312,"completion_tokens":262,"total_tokens":574}}
{"request_id":"req_28","timestamp":"2024-10-21T05:35:11.046Z","user_id":"usr_22","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.5","max_tokens":1425,"stream":true}},"usage":{"prompt_tokens":50,"completion_tokens":182,"total_tokens":232}}
{"request_id":"req_29","timestamp":"2024-10-11T06:14:52.973Z","user_id":"usr_4","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-sonnet","options":{"temperature":"0.4","max_tokens":1660,"stream":true}},"usage":{"prompt_tokens":384,"completion_tokens":124,"total_tokens":508}}
{"request_id":"req_30","timestamp":"2024-11-13T10:48:53.729Z","user_id":"usr_22","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-4","options":{"temperature":"0.4","max_tokens":1425,"stream":true}},"usage":{"prompt_tokens":299,"completion_tokens":57,"total_tokens":356}}
{"request_id":"req_31","timestamp":"2024-10-01T03:26:07.133Z","user_id":"usr_41","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"0.8","max_tokens":1975,"stream":true}},"usage":{"prompt_tokens":471,"completion_tokens":245,"total_tokens":716}}
{"request_id":"req_32","timestamp":"2024-11-26T12:13:53.221Z","user_id":"usr_33","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-opus","options":{"temperature":"0.5","max_tokens":557,"stream":false}},"usage":{"prompt_tokens":75,"completion_tokens":92,"total_tokens":167}}
{"request_id":"req_33","timestamp":"2024-10-14T07:41:11.783Z","user_id":"usr_18","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-opus","options":{"temperature":"1.0","max_tokens":843,"stream":false}},"usage":{"prompt_tokens":321,"completion_tokens":258,"total_tokens":579}}
{"request_id":"req_34","timestamp":"2024-10-21T11:20:47.679Z","user_id":"usr_37","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.7","max_tokens":1148,"stream":false}},"usage":{"prompt_tokens":425,"completion_tokens":245,"total_tokens":670}}
{"request_id":"req_35","timestamp":"2024-11-18T12:02:12.268Z","user_id":"usr_38","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"0.2","max_tokens":1987,"stream":false}},"usage":{"prompt_tokens":50,"completion_tokens":223,"total_tokens":273}}
{"request_id":"req_36","timestamp":"2024-10-03T02:17:56.042Z","user_id":"usr_38","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.2","max_tokens":1339,"stream":false}},"usage":{"prompt_tokens":102,"completion_tokens":112,"total_tokens":214}}
{"request_id":"req_37","timestamp":"2024-11-02T19:52:17.904Z","user_id":"usr_34","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"0.3","max_tokens":1050,"stream":false}},"usage":{"prompt_tokens":485,"completion_tokens":189,"total_tokens":674}}
{"request_id":"req_38","timestamp":"2024-11-17T22:26:34.434Z","user_id":"usr_5","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"0.6","max_tokens":857,"stream":false}},"usage":{"prompt_tokens":442,"completion_tokens":224,"total_tokens":666}}
{"request_id":"req_39","timestamp":"2024-11-17T01:20:40.223Z","user_id":"usr_36","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.9","max_tokens":698,"stream":true}},"usage":{"prompt_tokens":430,"completion_tokens":185,"total_tokens":615}}
{"request_id":"req_40","timestamp":"2024-11-20T21:38:04.662Z","user_id":"usr_31","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.3","max_tokens":1226,"stream":true}},"usage":{"prompt_tokens":201,"completion_tokens":65,"total_tokens":266}}
{"request_id":"req_41","timestamp":"2024-11-07T11:20:55.217Z","user_id":"usr_34","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"0.1","max_tokens":1893,"stream":false}},"usage":{"prompt_tokens":307,"completion_tokens":224,"total_tokens":531}}
{"request_id":"req_42","timestamp":"2024-10-30T23:13:57.704Z","user_id":"usr_44","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"0.3","max_tokens":888,"stream":false}},"usage":{"prompt_tokens":212,"completion_tokens":53,"total_tokens":265}}
{"request_id":"req_43","timestamp":"2024-11-09T02:04:23.904Z","user_id":"usr_28","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"0.3","max_tokens":1574,"stream":true}},"usage":{"prompt_tokens":161,"completion_tokens":190,"total_tokens":351}}
{"request_id":"req_44","timestamp":"2024-11-20T21:28:23.931Z","user_id":"usr_22","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-opus","options":{"temperature":"0.4","max_tokens":578,"stream":true}},"usage":{"prompt_tokens":465,"completion_tokens":294,"total_tokens":759}}
{"request_id":"req_45","timestamp":"2024-11-15T14:02:11.552Z","user_id":"usr_2","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-opus","options":{"temperature":"0.4","max_tokens":502,"stream":true}},"usage":{"prompt_tokens":489,"completion_tokens":288,"total_tokens":777}}
{"request_id":"req_46","timestamp":"2024-10-22T23:05:29.902Z","user_id":"usr_15","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-4","options":{"temperature":"0.5","max_tokens":1280,"stream":true}},"usage":{"prompt_tokens":462,"completion_tokens":283,"total_tokens":745}}
{"request_id":"req_47","timestamp":"2024-10-28T01:16:36.936Z","user_id":"usr_28","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"0.4","max_tokens":1513,"stream":true}},"usage":{"prompt_tokens":421,"completion_tokens":204,"total_tokens":625}}
{"request_id":"req_48","timestamp":"2024-11-20T18:18:38.744Z","user_id":"usr_4","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.8","max_tokens":1194,"stream":true}},"usage":{"prompt_tokens":251,"completion_tokens":109,"total_tokens":360}}
{"request_id":"req_49","timestamp":"2024-10-12T17:21:20.482Z","user_id":"usr_11","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.3","max_tokens":621,"stream":false}},"usage":{"prompt_tokens":195,"completion_tokens":253,"total_tokens":448}}
{"request_id":"req_50","timestamp":"2024-11-27T14:14:23.737Z","user_id":"usr_8","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-4","options":{"temperature":"0.0","max_tokens":1468,"stream":true}},"usage":{"prompt_tokens":461,"completion_tokens":100,"total_tokens":561}}
{"request_id":"req_51","timestamp":"2024-10-15T14:58:09.623Z","user_id":"usr_48","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"1.0","max_tokens":1879,"stream":false}},"usage":{"prompt_tokens":51,"completion_tokens":215,"total_tokens":266}}
{"request_id":"req_52","timestamp":"2024-11-18T00:55:43.893Z","user_id":"usr_48","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"0.2","max_tokens":549,"stream":false}},"usage":{"prompt_tokens":481,"completion_tokens":142,"total_tokens":623}}
{"request_id":"req_53","timestamp":"2024-11-01T03:22:01.890Z","user_id":"usr_14","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.8","max_tokens":1771,"stream":false}},"usage":{"prompt_tokens":459,"completion_tokens":79,"total_tokens":538}}
{"request_id":"req_54","timestamp":"2024-10-26T08:57:25.867Z","user_id":"usr_17","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"0.4","max_tokens":1888,"stream":false}},"usage":{"prompt_tokens":219,"completion_tokens":226,"total_tokens":445}}
{"request_id":"req_55","timestamp":"2024-11-17T16:12:47.424Z","user_id":"usr_43","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"0.0","max_tokens":1281,"stream":false}},"usage":{"prompt_tokens":426,"completion_tokens":244,"total_tokens":670}}
{"request_id":"req_56","timestamp":"2024-10-10T01:03:29.669Z","user_id":"usr_6","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.3","max_tokens":1004,"stream":false}},"usage":{"prompt_tokens":420,"completion_tokens":69,"total_tokens":489}}
{"request_id":"req_57","timestamp":"2024-10-10T19:18:37.937Z","user_id":"usr_30","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"0.7","max_tokens":1209,"stream":true}},"usage":{"prompt_tokens":59,"completion_tokens":66,"total_tokens":125}}
{"request_id":"req_58","timestamp":"2024-10-07T19:20:21.754Z","user_id":"usr_4","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.5","max_tokens":1215,"stream":true}},"usage":{"prompt_tokens":197,"completion_tokens":201,"total_tokens":398}}
{"request_id":"req_59","timestamp":"2024-10-12T07:54:12.535Z","user_id":"usr_35","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-4","options":{"temperature":"0.1","max_tokens":1445,"stream":false}},"usage":{"prompt_tokens":318,"completion_tokens":111,"total_tokens":429}}
{"request_id":"req_60","timestamp":"2024-11-04T00:11:56.488Z","user_id":"usr_3","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"1.0","max_tokens":1127,"stream":true}},"usage":{"prompt_tokens":286,"completion_tokens":293,"total_tokens":579}}
{"request_id":"req_61","timestamp":"2024-10-15T10:29:51.122Z","user_id":"usr_36","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.9","max_tokens":1810,"stream":false}},"usage":{"prompt_tokens":308,"completion_tokens":238,"total_tokens":546}}
{"request_id":"req_62","timestamp":"2024-10-15T07:46:39.995Z","user_id":"usr_36","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.8","max_tokens":736,"stream":true}},"usage":{"prompt_tokens":102,"completion_tokens":194,"total_tokens":296}}
{"request_id":"req_63","timestamp":"2024-10-25T11:39:09.912Z","user_id":"usr_37","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.5","max_tokens":1112,"stream":true}},"usage":{"prompt_tokens":211,"completion_tokens":139,"total_tokens":350}}
{"request_id":"req_64","timestamp":"2024-10-20T16:35:00.170Z","user_id":"usr_32","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-4","options":{"temperature":"0.2","max_tokens":535,"stream":true}},"usage":{"prompt_tokens":355,"completion_tokens":116,"total_tokens":471}}
{"request_id":"req_65","timestamp":"2024-11-27T04:31:51.172Z","user_id":"usr_44","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"0.3","max_tokens":838,"stream":true}},"usage":{"prompt_tokens":468,"completion_tokens":298,"total_tokens":766}}
{"request_id":"req_66","timestamp":"2024-10-26T17:30:31.696Z","user_id":"usr_12","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-sonnet","options":{"temperature":"0.7","max_tokens":505,"stream":true}},"usage":{"prompt_tokens":190,"completion_tokens":207,"total_tokens":397}}
{"request_id":"req_67","timestamp":"2024-10-04T02:09:21.280Z","user_id":"usr_31","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"1.0","max_tokens":886,"stream":false}},"usage":{"prompt_tokens":264,"completion_tokens":60,"total_tokens":324}}
{"request_id":"req_68","timestamp":"2024-11-14T09:34:25.291Z","user_id":"usr_17","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"0.5","max_tokens":1794,"stream":true}},"usage":{"prompt_tokens":166,"completion_tokens":133,"total_tokens":299}}
{"request_id":"req_69","timestamp":"2024-10-13T20:06:12.700Z","user_id":"usr_18","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.6","max_tokens":555,"stream":false}},"usage":{"prompt_tokens":247,"completion_tokens":149,"total_tokens":396}}
{"request_id":"req_70","timestamp":"2024-10-05T01:45:08.193Z","user_id":"usr_31","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.9","max_tokens":1428,"stream":true}},"usage":{"prompt_tokens":54,"completion_tokens":132,"total_tokens":186}}
{"request_id":"req_71","timestamp":"2024-11-15T22:14:55.479Z","user_id":"usr_18","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"0.5","max_tokens":650,"stream":false}},"usage":{"prompt_tokens":65,"completion_tokens":206,"total_tokens":271}}
{"request_id":"req_72","timestamp":"2024-11-09T06:44:07.284Z","user_id":"usr_43","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"0.2","max_tokens":1363,"stream":false}},"usage":{"prompt_tokens":443,"completion_tokens":284,"total_tokens":727}}
{"request_id":"req_73","timestamp":"2024-11-06T01:10:44.917Z","user_id":"usr_24","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-4","options":{"temperature":"0.4","max_tokens":1927,"stream":true}},"usage":{"prompt_tokens":495,"completion_tokens":216,"total_tokens":711}}
{"request_id":"req_74","timestamp":"2024-10-19T14:43:49.854Z","user_id":"usr_26","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.4","max_tokens":679,"stream":false}},"usage":{"prompt_tokens":221,"completion_tokens":286,"total_tokens":507}}
{"request_id":"req_75","timestamp":"2024-10-05T06:19:28.703Z","user_id":"usr_25","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-opus","options":{"temperature":"0.8","max_tokens":1614,"stream":false}},"usage":{"prompt_tokens":59,"completion_tokens":93,"total_tokens":152}}
{"request_id":"req_76","timestamp":"2024-11-04T22:29:57.675Z","user_id":"usr_33","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.9","max_tokens":1491,"stream":false}},"usage":{"prompt_tokens":90,"completion_tokens":120,"total_tokens":210}}
{"request_id":"req_77","timestamp":"2024-11-08T02:17:28.909Z","user_id":"usr_4","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"0.0","max_tokens":1324,"stream":true}},"usage":{"prompt_tokens":355,"completion_tokens":102,"total_tokens":457}}
{"request_id":"req_78","timestamp":"2024-10-24T15:25:14.046Z","user_id":"usr_39","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"0.8","max_tokens":1529,"stream":false}},"usage":{"prompt_tokens":208,"completion_tokens":141,"total_tokens":349}}
{"request_id":"req_79","timestamp":"2024-10-27T13:01:16.190Z","user_id":"usr_40","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-opus","options":{"temperature":"0.0","max_tokens":1638,"stream":false}},"usage":{"prompt_tokens":243,"completion_tokens":274,"total_tokens":517}}
{"request_id":"req_80","timestamp":"2024-11-22T13:07:16.699Z","user_id":"usr_24","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.4","max_tokens":1397,"stream":true}},"usage":{"prompt_tokens":263,"completion_tokens":185,"total_tokens":448}}
{"request_id":"req_81","timestamp":"2024-11-29T03:35:54.264Z","user_id":"usr_26","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-4","options":{"temperature":"0.1","max_tokens":1521,"stream":false}},"usage":{"prompt_tokens":273,"completion_tokens":199,"total_tokens":472}}
{"request_id":"req_82","timestamp":"2024-11-20T08:27:02.022Z","user_id":"usr_38","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-opus","options":{"temperature":"0.6","max_tokens":1463,"stream":true}},"usage":{"prompt_tokens":192,"completion_tokens":120,"total_tokens":312}}
{"request_id":"req_83","timestamp":"2024-11-09T10:38:51.640Z","user_id":"usr_24","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-3.5-turbo","options":{"temperature":"1.0","max_tokens":1574,"stream":false}},"usage":{"prompt_tokens":406,"completion_tokens":58,"total_tokens":464}}
{"request_id":"req_84","timestamp":"2024-10-29T18:37:34.187Z","user_id":"usr_16","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-opus","options":{"temperature":"0.1","max_tokens":1924,"stream":true}},"usage":{"prompt_tokens":237,"completion_tokens":284,"total_tokens":521}}
{"request_id":"req_85","timestamp":"2024-10-17T21:47:26.419Z","user_id":"usr_49","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-opus","options":{"temperature":"0.7","max_tokens":1714,"stream":false}},"usage":{"prompt_tokens":114,"completion_tokens":194,"total_tokens":308}}
{"request_id":"req_86","timestamp":"2024-10-13T16:59:19.264Z","user_id":"usr_40","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.8","max_tokens":520,"stream":true}},"usage":{"prompt_tokens":227,"completion_tokens":190,"total_tokens":417}}
{"request_id":"req_87","timestamp":"2024-10-25T06:47:20.855Z","user_id":"usr_48","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.3","max_tokens":1904,"stream":false}},"usage":{"prompt_tokens":476,"completion_tokens":96,"total_tokens":572}}
{"request_id":"req_88","timestamp":"2024-11-05T07:30:25.734Z","user_id":"usr_4","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.9","max_tokens":535,"stream":false}},"usage":{"prompt_tokens":399,"completion_tokens":217,"total_tokens":616}}
{"request_id":"req_89","timestamp":"2024-11-13T01:46:36.632Z","user_id":"usr_20","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-4","options":{"temperature":"0.4","max_tokens":1260,"stream":true}},"usage":{"prompt_tokens":189,"completion_tokens":159,"total_tokens":348}}
{"request_id":"req_90","timestamp":"2024-11-29T06:17:41.475Z","user_id":"usr_7","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"claude-3-sonnet","options":{"temperature":"0.5","max_tokens":1105,"stream":false}},"usage":{"prompt_tokens":164,"completion_tokens":223,"total_tokens":387}}
{"request_id":"req_91","timestamp":"2024-11-21T21:18:42.618Z","user_id":"usr_31","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.1","max_tokens":1899,"stream":false}},"usage":{"prompt_tokens":424,"completion_tokens":121,"total_tokens":545}}
{"request_id":"req_92","timestamp":"2024-10-13T04:50:06.616Z","user_id":"usr_20","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-4","options":{"temperature":"0.6","max_tokens":752,"stream":true}},"usage":{"prompt_tokens":400,"completion_tokens":160,"total_tokens":560}}
{"request_id":"req_93","timestamp":"2024-10-06T12:44:26.578Z","user_id":"usr_18","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"0.4","max_tokens":1916,"stream":false}},"usage":{"prompt_tokens":193,"completion_tokens":299,"total_tokens":492}}
{"request_id":"req_94","timestamp":"2024-11-16T12:40:44.907Z","user_id":"usr_46","request":{"type":"chat","endpoint":"/v1/completions","model":"claude-3-sonnet","options":{"temperature":"0.9","max_tokens":1612,"stream":false}},"usage":{"prompt_tokens":149,"completion_tokens":181,"total_tokens":330}}
{"request_id":"req_95","timestamp":"2024-10-28T14:02:47.893Z","user_id":"usr_21","request":{"type":"chat","endpoint":"/v1/chat/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.6","max_tokens":1378,"stream":true}},"usage":{"prompt_tokens":363,"completion_tokens":292,"total_tokens":655}}
{"request_id":"req_96","timestamp":"2024-10-24T10:13:34.492Z","user_id":"usr_9","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-opus","options":{"temperature":"0.2","max_tokens":1055,"stream":true}},"usage":{"prompt_tokens":463,"completion_tokens":252,"total_tokens":715}}
{"request_id":"req_97","timestamp":"2024-10-25T05:35:39.972Z","user_id":"usr_32","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-3.5-turbo","options":{"temperature":"0.1","max_tokens":877,"stream":false}},"usage":{"prompt_tokens":451,"completion_tokens":211,"total_tokens":662}}
{"request_id":"req_98","timestamp":"2024-10-30T12:55:53.621Z","user_id":"usr_21","request":{"type":"chat","endpoint":"/v1/images/generations","model":"claude-3-sonnet","options":{"temperature":"0.8","max_tokens":1966,"stream":true}},"usage":{"prompt_tokens":497,"completion_tokens":93,"total_tokens":590}}
{"request_id":"req_99","timestamp":"2024-11-14T11:31:10.758Z","user_id":"usr_11","request":{"type":"chat","endpoint":"/v1/completions","model":"gpt-4","options":{"temperature":"0.4","max_tokens":564,"stream":true}},"usage":{"prompt_tokens":244,"completion_tokens":154,"total_tokens":398}}
{"request_id":"req_100","timestamp":"2024-11-22T13:43:33.802Z","user_id":"usr_25","request":{"type":"chat","endpoint":"/v1/images/generations","model":"gpt-4","options":{"temperature":"0.9","max_tokens":1096,"stream":true}},"usage":{"prompt_tokens":58,"completion_tokens":274,"total_tokens":332}}
"""
            persist_fixture(f"{ds_name}", ds_content)
            click.echo(FeedbackManager.info(message=f"✓ /fixtures/{ds_name}"))

            # Create sample endpoint
            pipe_name = "api_token_usage"
            pipe_path = Path(folder) / "endpoints" / f"{pipe_name}.pipe"
            pipe_content = """DESCRIPTION >
    Pipe to generate a token usage timeline.

NODE api_token_usage_node_1
SQL >
    %
    SELECT
        toDate(timestamp) as date,
        user_id,
        sum(usage_total_tokens) as total_tokens
    FROM
        events
    WHERE
        user_id IN (SELECT id FROM users WHERE organization_id = {{String(organization_id)}})
        {%if defined(start_date) and defined(end_date)%}
        AND timestamp BETWEEN {{DateTime(start_date)}} AND {{DateTime(end_date)}}
        {%else%}
        AND timestamp BETWEEN now() - interval 30 day AND now()
        {%end%}
    GROUP BY
        date, user_id
    ORDER BY
        date

TYPE Endpoint

"""
            pipe_path.write_text(pipe_content)
            click.echo(FeedbackManager.info(message=f"✓ /endpoints/{pipe_name}.pipe"))

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
    project_paths = ["datasources", "endpoints", "materializations", "copies", "sinks", "fixtures"]
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
            click.echo(FeedbackManager.error(message=f"Ersssssror: {str(e)}"))
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
