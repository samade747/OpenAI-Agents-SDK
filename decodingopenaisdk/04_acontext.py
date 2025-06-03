# Import the dataclass decorator for structured data
from dataclasses import dataclass

# Import Agent and Runner classes, and RunContextWrapper to handle custom context
from agents import Agent, Runner, RunContextWrapper

# asyncio is used for running asynchronous code
import asyncio


# 🧾 Define a Custom Context

@dataclass
class UserContext:
    uid: str            # Unique user identifier
    is_pro_user: bool   # Flag to indicate if the user is a Pro subscriber

    # Note: UserContext is defined but not used in this example. You could use it later to tailor prompts based on user type.


    # 🧠 Custom Prompt Generator Using RunContextWrapper

# Function to generate dynamic instructions based on the context
def create_prompt(ctx: RunContextWrapper[str], agent: Agent[str]) -> str:
    print(f"Creating prompt for {ctx.context}")  # Log the context data (e.g., "junaid")

    # Return dynamic instruction using the provided context (a name in this case)
    return f"You are a helpful assistant that provides concise answers. You are talking to {ctx.context}."

# ctx.context here is a string ("junaid"), passed during the run. RunContextWrapper gives you safe access to the context even in async functions or multi-agent pipelines.


# 🤖 Agent Setup with Callable Instructions

# Create an agent that uses the callable prompt creator
agent_basic = Agent[str](  # The `[str]` here tells the Agent to expect context of type `str`
    name="BasicAgent",
    instructions=create_prompt  # Dynamically generated prompt based on context
)


# ✅ Test Function

# Async function to test the agent behavior
async def test_basic():
    name = "samad"  # Custom context (the user's name)
    
    # Run the agent with the context
    result1 = await Runner.run(agent_basic, "What is my name?", context=name)
    
    # Print the final answer from the agent
    print("Basic Agent:", result1.final_output)


# Main function to run all async test cases
async def main():
    await test_basic()

# Start the async main loop if the script is run directly
if __name__ == "__main__":
    asyncio.run(main())


# 🔍 Summary of What’s Happening

# | Component                | Purpose                                                         |
# | ------------------------ | --------------------------------------------------------------- |
# | `RunContextWrapper[str]` | Wraps your context so it's accessible in instruction functions  |
# | `create_prompt(...)`     | Dynamically generates agent instructions using context (`name`) |
# | `Agent[str]`             | Agent expecting context of type `str`                           |
# | `Runner.run(...)`        | Runs the agent on a prompt with context provided                |

