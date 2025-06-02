# Import asyncio for handling asynchronous operations
import asyncio

# Import os for accessing environment variables (e.g., API keys)
import os

# Load environment variables from a .env file
from dotenv import load_dotenv, find_dotenv

# Import classes and functions from the OpenAI Agents SDK
from agents import (
    Agent,                      # Defines a conversational agent
    Runner,                     # Runs agents and manages execution
    OpenAIChatCompletionsModel, # (commented out) Defines the OpenAI model used for completions
    AsyncOpenAI,                # Asynchronous OpenAI API client
    GuardrailFunctionOutput,    # Wraps guardrail output and result status
    InputGuardrail,             # Used to define input-level checks (e.g., filtering or redirecting)
    function_tool               # Decorator to define callable tools/functions for agents
)

# Import BaseModel from Pydantic for structured output
from pydantic import BaseModel


# Define the expected output structure for the guardrail agent
class HomeworkOutput(BaseModel):
    is_homework: bool     # Whether the input is homework-related
    reasoning: str        # Reasoning behind the decision


# 📡 Set Up API Access:


# Load environment variables (like API keys) from .env file
load_dotenv(find_dotenv())

# Initialize the Async OpenAI client with API key and base URL
provider = AsyncOpenAI(
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 🔧 Define a Tool (Function Tool):

# Define a simple weather function tool (though unused in this example)
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"


# 🧠 Define Specialist Agents:

# Agent that handles historical questions
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

# Agent that handles math questions
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)


# 🛡️ Define Guardrail Agent:

# Agent that checks whether the user is asking about homework
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,  # Structured output using Pydantic
)

# 🧪 Define Guardrail Logic:

# Async function to apply guardrail logic using the guardrail agent
async def homework_guardrail(ctx, agent: Agent, input_data):
    print("RECEIVED AGENT IN GD", agent.name)  # Debug print
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)  # Run guardrail agent
    print("RESULT", result)  # Debug print
    final_output = result.final_output_as(HomeworkOutput)  # Convert output to HomeworkOutput model
    print("FINAL OUTPUT", final_output)  # Debug print

    # Return guardrail function result with a trigger if input is not about homework
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,  # Trigger only if it's not homework
    )



# 🎯 Main Agent with Guardrail and Routing:

async def main():
    # Define the main agent responsible for triage (routing requests)
    agent = Agent(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question",
        # model=OpenAIChatCompletionsModel(openai_client=provider, model="gpt-4o-mini"),  # Optional model specification
        handoffs=[history_tutor_agent, math_tutor_agent],  # List of agents to possibly route to
        input_guardrails=[InputGuardrail(homework_guardrail)],  # Apply homework guardrail first
    )

    # Run the agent with a user query related to history
    result = await Runner.run(agent, "I have homework about the french revolution. Can you help me?")
    
    # Print final response
    print(result.final_output)

    # Fun poem comment for developers (ignored by Python)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.

# 🚀 Entry Point:
# If script is run directly, not imported
if __name__ == "__main__":
    print("\n[STARTING AGENT]\n")  # Start message
    asyncio.run(main())  # Run the async main function

# ✅ Summary:

# You created multiple specialized agents.

# You added an input guardrail that checks whether the user input is homework-related.

# The Triage Agent uses this guardrail to decide if it should proceed or reject the input.

# If allowed, the agent hands off to a domain-specific agent (History or Math Tutor) based on the topic.