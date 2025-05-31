# 🧠 What is an OpenAI Agent?
# In the OpenAI SDK, an Agent is a powerful tool designed to autonomously use tools (functions, APIs, files, etc.) to solve complex tasks.

# Think of it as:

# "A smart AI worker that can think, plan, and use tools to accomplish tasks you assign to it."

# ⚙️ How OpenAI Agent Works (Behind the Scenes)
# Basic Workflow:
# You give the agent a task (like "Summarize this PDF" or "Scrape product prices").

# The agent uses an LLM (like GPT-4) as its brain.

# The agent can call tools (functions you define) to fetch or act on data.

# It may loop, reflect, and retry internally until the final answer is ready.


# 🛠️ Agent Class: Core Structure
# The main class is openai.agents.Agent.


from openai import OpenAI
from openai.agents import Agent

client = OpenAI()

agent = client.beta.agents.create(
    name="Example Agent",
    instructions="You are an assistant that helps with calculations.",
    model="gpt-4-turbo"
)


# 📤 Using an Agent
# To use the agent, you run it with a task:


run = client.beta.threads.create_and_run(
    agent_id=agent.id,
    instructions="Help me solve this problem",
    messages=[
        {"role": "user", "content": "What's 23 * 47?"}
    ]
)


# 🧩 How Agents Use Tools
# You can give the agent tools (custom functions or APIs) using tools during agent creation:

tool = client.beta.tools.create(
    name="my_calculator",
    description="Performs basic arithmetic operations.",
    function={"parameters": {...}, "code": my_function}
)

agent = client.beta.agents.create(
    name="Math Agent",
    instructions="Use the calculator to help with math problems.",
    model="gpt-4-turbo",
    tools=[tool.id]  # Assign tools here
)

# 🧪 Methods in Agent Lifecycle
# ✅ client.beta.agents.create()
# Creates a new agent.

# 🔁 client.beta.threads.create_and_run()
# Creates a new thread and runs it with the agent.

# ✏️ client.beta.agents.update()
# Updates the agent’s name, instructions, or tools.

# ❌ client.beta.agents.delete()
# Deletes the agent.

# 🔁 Agent Autonomy Loop (Internally)
# Under the hood, the agent:

# Reads the user message.

# Decides whether it needs a tool.

# Calls the tool (if needed).

# Thinks again with the result.

# Repeats if necessary.

# Returns the final answer.

# This loop is called the agent loop, and it's handled automatically by the SDK.

# ✅ Summary: How Agents Work

# | Step | What Happens                                         |
# | ---- | ---------------------------------------------------- |
# | 1️⃣  | You define an agent with instructions and a model    |
# | 2️⃣  | Optionally attach tools (functions)                  |
# | 3️⃣  | Run the agent by creating a thread with messages     |
# | 4️⃣  | Agent autonomously reasons, uses tools, and replies  |
# | 5️⃣  | You get the final response after the agent completes |


from openai import OpenAI
import json

client = OpenAI()

# 1️⃣ Define a custom function the Agent can use
def calculator(a: float, b: float, operation: str) -> float:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else "Cannot divide by zero"
    else:
        return "Invalid operation"

# 2️⃣ Register the tool with OpenAI
tool = client.beta.tools.register(
    function=calculator,
    name="simple_calculator",
    description="Performs basic arithmetic operations: add, subtract, multiply, divide.",
    parameters={
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"},
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "Type of math operation"
            }
        },
        "required": ["a", "b", "operation"]
    }
)

# 3️⃣ Create an Agent with the tool
agent = client.beta.agents.create(
    name="Math Agent",
    instructions="You are a helpful agent that solves math problems using the calculator tool.",
    model="gpt-4-turbo",
    tools=[tool.id]
)

# 4️⃣ Create a conversation thread
thread = client.beta.threads.create()

# 5️⃣ Add a user message
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is 23 multiplied by 47?"
)

# 6️⃣ Run the agent on the thread
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    agent_id=agent.id,
    instructions="Use the calculator tool if needed to answer correctly."
)

# 7️⃣ Wait for the run to complete
import time

while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    if run_status.status == "completed":
        break
    elif run_status.status in ["failed", "cancelled"]:
        raise Exception(f"Run failed with status: {run_status.status}")
    time.sleep(1)

# 8️⃣ Get the final response
messages = client.beta.threads.messages.list(thread_id=thread.id)

print("🧠 Agent's Final Reply:")
for msg in messages.data:
    if msg.role == "assistant":
        print(msg.content[0].text.value)


# | Concept      | Code Part                                    |
# | ------------ | -------------------------------------------- |
# | Define tool  | `def calculator()` and `tools.register(...)` |
# | Create agent | `agents.create(...)` with tools              |
# | Add message  | `messages.create(...)`                       |
# | Run agent    | `runs.create(...)`                           |
# | Get response | `messages.list(...)`                         |
