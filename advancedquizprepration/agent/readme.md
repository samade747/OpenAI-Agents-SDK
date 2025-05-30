# 🧠 What is an OpenAI Agent?

> Learn how OpenAI Agents work using the official [OpenAI Python SDK](https://openai.github.io/openai-agents-python/agents/)

---

## 🚀 Introduction

An **OpenAI Agent** is a smart, LLM-powered assistant that can **think, reason, and use tools (functions, APIs, files, etc.)** to solve real-world tasks — automatically.

Agents combine the power of:
- 🧠 **Large Language Models (LLMs)** (like GPT-4 Turbo)
- 🔧 **Tools** (custom Python functions, APIs, calculators, etc.)
- 🔁 **Autonomous loops** (to reflect and iterate)

---

## 🧩 Why Use Agents?

Agents are ideal for:
- Automating complex tasks (e.g., file summarization, scraping, data analysis)
- Calling APIs based on user queries
- Reasoning through multi-step problems
- Integrating LLMs into real-world workflows

---

## ⚙️ How It Works

### ✅ You create an Agent:
- Provide it with a name, instructions, and an LLM (like `gpt-4-turbo`).
- Optionally attach tools (e.g., calculator, API calls).

### 📨 You give it a task:
- Use `create_and_run()` to pass a message like "Summarize this PDF".

### 🧠 It thinks like a human:
- Decides what tools to use.
- Gathers information.
- Loops internally if needed.
- Returns the final answer.

---

## 🛠️ Code Example (Minimal Agent)

```python
from openai import OpenAI
from openai.agents import Agent

client = OpenAI()

# 1. Create an agent
agent = client.beta.agents.create(
    name="Simple Agent",
    instructions="You are a helpful assistant.",
    model="gpt-4-turbo"
)

# 2. Run the agent with a message
run = client.beta.threads.create_and_run(
    agent_id=agent.id,
    instructions="Answer the user's question clearly.",
    messages=[
        {"role": "user", "content": "What is 23 * 47?"}
    ]
)


🔁 How Agents Think (The Loop)
Internally, the Agent:

Reads the user’s message.

Plans what to do.

Uses tools (if necessary).

Reflects on the output.

Repeats until it reaches a final answer.

You don’t need to manage this loop — it’s automatic.

🧠 TL;DR

| Concept      | Description                         |
| ------------ | ----------------------------------- |
| Agent        | A smart assistant powered by an LLM |
| Model        | The brain (e.g., `gpt-4-turbo`)     |
| Instructions | How it should behave                |
| Tools        | Extra functions/APIs it can use     |
| Run          | A task given to the agent           |
