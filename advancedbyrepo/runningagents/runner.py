# https://openai.github.io/openai-agents-python/running_agents/

# You can run agents via the Runner class. You have 3 options:

# 1. Runner.run(), which runs async and returns a RunResult.

# 2. Runner.run_sync(), which is a sync method and just runs .run() under the hood.

# 3. Runner.run_streamed(), which runs async and returns a RunResultStreaming. It calls the LLM in streaming mode, and streams those events to you as they are received.

# Source code in src/agents/run.py


from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.


# The agent loop
# When you use the run method in Runner, you pass in a starting agent and input. The input can either be a string (which is considered a user message), or a list of input items, which are the items in the OpenAI Responses API.

# The runner then runs a loop:

# 1. We call the LLM for the current agent, with the current input.
# 2. The LLM produces its output.
#       If the LLM returns a final_output, the loop ends and we return the result.
#       If the LLM does a handoff, we update the current agent and input, and re-run the loop.
#       If the LLM produces tool calls, we run those tool calls, append the results, and re-run the loop.
# 3. If we exceed the max_turns passed, we raise a MaxTurnsExceeded exception.

