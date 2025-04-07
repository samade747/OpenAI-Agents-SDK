# -*- coding: utf-8 -*-
"""01_hello_agent.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1T3JPcpC7B7_ASDFLifLwwDH0Ikgc68Am

# Install openai-agents SDK
"""

!pip install -Uq openai-agents

"""# Make your Jupyter Notebook capable of running asynchronous functions."""

import nest_asyncio
nest_asyncio.apply()

"""# Run Google Gemini with OPENAI-Agent SDK"""

import os

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from google.colab import userdata

gemini_api_key = userdata.get("GEMINI_API_KEY")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

"""# Hello world code | method one



"""

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print("\nCALLING AGENT\n")
print(result.final_output)

"""# Hello world code | method two

"""

import asyncio

from agents import Agent, Runner


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.",run_config=config)
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":
    asyncio.run(main())

"""# Agent Level Custom model configuration

```python
agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    )

```

> **Note** `model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)`
"""

import asyncio
import os

from openai import AsyncOpenAI

from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

BASE_URL = os.getenv("EXAMPLE_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.getenv("EXAMPLE_API_KEY") or userdata.get("GEMINI_API_KEY")
MODEL_NAME = os.getenv("EXAMPLE_MODEL_NAME") or "gemini-2.0-flash"

# print(BASE_URL, API_KEY, MODEL_NAME)

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )


client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)



async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    )

    result = await Runner.run(agent, "Who is the founder of Pakistan?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

"""# Set Model(LLM) configration on Global level
> **Note**
```python
set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)
```
"""

import asyncio
import os

from openai import AsyncOpenAI

from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

BASE_URL = os.getenv("EXAMPLE_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.getenv("EXAMPLE_API_KEY") or userdata.get("GEMINI_API_KEY")
MODEL_NAME = os.getenv("EXAMPLE_MODEL_NAME") or "gemini-2.0-flash"


if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )



client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=MODEL_NAME,
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())











