# 2b) Why is the user prompt passed to Runner.run() (a @classmethod), rather than stored on the Agent?

# Separation of roles:

# The Agent defines how to think (tools, system prompt, memory) but not what to think about in each invocation.

# The Runner is responsible for executing an agent on a particular task or user input.

# Statelessness & reusability:

# By passing the user prompt into Runner.run(), you can reuse the same Agent instance for different inputs without mutating it.

# Separation of concerns:

# The Agent defines how to operate (its system prompt, tools, handoffs, guardrails).

# The Runner is responsible for when and with what input the agent runs.

# Reusability & statelessness: You can invoke the same Agent on multiple, differing user inputs without mutating the agent itself.


class Runner:
    @classmethod
    def run(cls, agent: Agent, user_input: str):
        system_prompt = (
            agent.instructions() if callable(agent.instructions)
            else agent.instructions
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_input},
        ]
        # … loop calling LLM, tools, etc.
        return "agent’s response"

# Usage:
response1 = Runner.run(agent_static, "What is 2+2?")
response2 = Runner.run(agent_static, "What is 3+5?")

