🔰 PART 1: Setup & Installation
✅ Install the SDK

pip install openai-agents
🧠 PART 2: What Is an Agent?
An Agent in OpenAI’s SDK is:

A system that receives inputs

Thinks using an LLM (OpenAI models or others)

Can use tools

Maintains state (memory)

Returns output to the user

⚙️ PART 3: Your First Simple Agent
Let’s walk through the basic "Hello World" agent:

python
Copy
Edit
# basic_agent.py
from openai import OpenAI
from openai.agents import Agent

client = OpenAI()

agent = Agent(client=client)

response = agent.run("What is the capital of France?")
print(response)
🔍 Explanation:
Agent(...): Initializes an agent with default configuration

.run(...): Sends a message to the agent and gets a reply

🧰 PART 4: Using Tools with Agents
What Are Tools?
Tools let the agent perform actions like search, calculations, or file reading.

Example: Add a Calculator Tool
python
Copy
Edit
from openai import OpenAI
from openai.agents import Agent, tool

client = OpenAI()

@tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

agent = Agent(client=client, tools=[add_numbers])

response = agent.run("What is 15 plus 27?")
print(response)
🔍 What’s Happening:
You define a Python function as a tool using @tool

Agent decides when to use it

It automatically passes arguments and uses the return value

🧠 PART 5: Using State (Context)
You can use mutable state to maintain memory between runs:

python
Copy
Edit
from openai import OpenAI
from openai.agents import Agent, Context

client = OpenAI()

context = Context()

agent = Agent(client=client, context=context)

agent.run("My name is Alice.")
response = agent.run("What is my name?")
print(response)
🔍 Explanation:
The agent remembers that your name is Alice because of shared Context()

🗂️ PART 6: Structured Output with Pydantic
You can ask the agent to return data in a structured format.

python
Copy
Edit
from openai import OpenAI
from openai.agents import Agent
from pydantic import BaseModel

client = OpenAI()

class MovieInfo(BaseModel):
    title: str
    year: int

agent = Agent(client=client, output_format=MovieInfo)

response = agent.run("The movie is Inception released in 2010")
print(response.title, response.year)
✅ Benefit:
Structured data is typed, validated, and can be used in applications directly

📦 PART 7: Stateful Agents with Custom Tools & Context
You can build fully customized agents that:

Use tools

Maintain context

Produce structured output

python
Copy
Edit
from openai import OpenAI
from openai.agents import Agent, Context, tool
from pydantic import BaseModel

client = OpenAI()
context = Context()

@tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

class GreetOutput(BaseModel):
    greeting: str

agent = Agent(
    client=client,
    context=context,
    tools=[greet],
    output_format=GreetOutput,
)

response = agent.run("Greet Alice for me")
print(response.greeting)
🚀 PART 8: Next Steps
Would you like me to:

Teach how to build a full app using this agent (e.g., a travel planner, calculator, or chatbot)?

Go deeper into tools, memory, and structured outputs?

Make you a PDF cheat sheet with all concepts?

Help you deploy this agent in Streamlit or FastAPI?

Let me know what you want next 👇








