import os

import pytest

from inspect_ai import eval
from inspect_ai.model import ChatMessage, ContentText, ModelName, ModelOutput
from inspect_ai.solver import TaskState, tool


def skip_if_env_var(var: str, exists=True):
    condition = (var in os.environ.keys()) if exists else (var not in os.environ.keys())
    return pytest.mark.skipif(
        condition,
        reason=f"Test doesn't work without {var} environment variable defined.",
    )


def skip_if_no_openai(func):
    return skip_if_env_var("OPENAI_API_KEY", exists=False)(func)


def skip_if_no_anthropic(func):
    return skip_if_env_var("ANTHROPIC_API_KEY", exists=False)(func)


def skip_if_no_google(func):
    return skip_if_env_var("GOOGLE_API_KEY", exists=False)(func)


def skip_if_no_mistral(func):
    return skip_if_env_var("MISTRAL_API_KEY", exists=False)(func)


def skip_if_no_cloudflare(func):
    return skip_if_env_var("CLOUDFLARE_API_TOKEN", exists=False)(func)


def skip_if_no_together(func):
    return skip_if_env_var("TOGETHER_API_KEY", exists=False)(func)


def skip_if_no_azureai(func):
    return skip_if_env_var("AZURE_API_KEY", exists=False)(func)


def skip_if_github_action(func):
    return skip_if_env_var("GITHUB_ACTIONS", exists=True)(func)


def run_example(example: str, model: str):
    example_file = os.path.join("examples", example)
    return eval(example_file, model=model, limit=1)


# define tool
@tool(
    prompt="""If you are given a math problem of any kind,
    please use the addition tool to compute the result.""",
    params={"color": "metadata.color"},
)
def addition():
    async def add(color: str, x: int, y: int):
        """
        Tool for adding two numbers.

        Args:
            color (str): Color
            x (int): First number to add.
            y (int): Second number to add.

        Returns:
            The sum of the two numbers.
        """
        # return as list[Content] to confirm that codepath works
        return [ContentText(text=str(x + y))]

    return add


# The intention of this `simple_task_state` helper is to remove some of the
# boiler plate of creating a task for use in solver checks where we just need
# "some" state. Over time this will likely expand and need to be extracted into
# its own helper file with multiple options.
def simple_task_state(
    choices: list[str] = [],
    messages: list[ChatMessage] = [],
    model_output: str = "",
) -> TaskState:
    return TaskState(
        choices=choices,
        epoch=0,
        input=[],
        messages=messages,
        model=ModelName(model="fake/model"),
        output=ModelOutput.from_content(model="model", content=model_output),
        sample_id=0,
    )
