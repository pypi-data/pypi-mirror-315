import asyncio
import json
import urllib.parse
from copy import deepcopy
from typing import Awaitable, Callable, List, Optional

from openai import OpenAI
from pydantic import BaseModel

from tinybird.client import TinyB
from tinybird.prompts import create_test_calls_prompt
from tinybird.tb.modules.config import CLIConfig


class DataFile(BaseModel):
    name: str
    content: str


class DataProject(BaseModel):
    datasources: List[DataFile]
    pipes: List[DataFile]


class TestExpectation(BaseModel):
    name: str
    description: str
    parameters: str
    expected_result: str


class TestExpectations(BaseModel):
    tests: List[TestExpectation]


class LLM:
    def __init__(self, client: TinyB, api_key: Optional[str] = None):
        self.client = client
        user_token = CLIConfig.get_project_config().get_user_token()
        user_client = deepcopy(client)
        user_client.token = user_token
        self.user_client = user_client
        self.openai = OpenAI(api_key=api_key) if api_key else None

    async def _execute(self, action_fn: Callable[[], Awaitable[str]], checker_fn: Callable[[str], bool]):
        is_valid = False
        times = 0

        while not is_valid and times < 5:
            result = await action_fn()
            if asyncio.iscoroutinefunction(checker_fn):
                is_valid = await checker_fn(result)
            else:
                is_valid = checker_fn(result)
            times += 1

        return result

    async def create_project(self, prompt: str) -> DataProject:
        try:
            response = await self.user_client._req(
                "/v0/llm/create",
                method="POST",
                data=f'{{"prompt": {json.dumps(prompt)}}}',
                headers={"Content-Type": "application/json"},
            )

            return DataProject.model_validate(response.get("result", {}))
        except Exception:
            return DataProject(datasources=[], pipes=[])

    async def generate_sql_sample_data(self, schema: str, rows: int = 20, context: str = "") -> str:
        response = await self.user_client._req(
            "/v0/llm/mock",
            method="POST",
            data=f'{{"schema": "{urllib.parse.quote(schema)}", "rows": {rows}, "context": "{urllib.parse.quote(context)}"}}',
            headers={"Content-Type": "application/json"},
        )
        return response.get("result", "")

    async def create_test_commands(
        self, pipe_content: str, pipe_params: set[str], context: str = ""
    ) -> TestExpectations:
        if not self.openai:
            raise ValueError("OpenAI API key is not set")

        completion = self.openai.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": create_test_calls_prompt.format(context=context)},
                {"role": "user", "content": f"Pipe content: {pipe_content}\nPipe params: {pipe_params}"},
            ],
            response_format=TestExpectations,
        )
        return completion.choices[0].message.parsed or TestExpectations(tests=[])
