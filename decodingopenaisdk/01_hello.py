# Import the asyncio module to handle asynchronous operations
import asyncio

# Import the os module to access environment variables like API keys
import os

# Import dotenv functions to load environment variables from a .env file
from dotenv import load_dotenv, find_dotenv

# Import necessary classes from the agents library
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

# Load environment variables from the .env file automatically
load_dotenv(find_dotenv())

# Create an instance of AsyncOpenAI to interact with the OpenAI API asynchronously
provider = AsyncOpenAI(
    base_url="https://api.openai.com/v1",  # Base URL for OpenAI API
    api_key=os.getenv("OPENAI_API_KEY")    # API key from environment variables
)


# Define an asynchronous main function
async def main():
    # Create an Agent instance with a name, instructions, and a model
    agent = Agent(
        name="Assistant",  # Name of the agent
        instructions="You only respond in eng.",  # System instructions for the agent
        model=OpenAIChatCompletionsModel(
            openai_client=provider,  # Use the AsyncOpenAI client we created
            model="gpt-4o-mini"      # Specify the OpenAI model to use
        ),
    )

    # Use Runner to run the agent with an input message
    result = await Runner.run(agent, "Tell me about agents!")

    # Print the final output of the agent's response
    print(result.final_output)

    # Just a fun poem-style comment for developers (not executed)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


# This block runs when the script is executed directly (not imported)
if __name__ == "__main__":
    print("\n[STARTING AGENT]\n")  # Print a startup message
    asyncio.run(main())            # Run the async main() function


# Summary:
# You define a GPT-4o-mini-based assistant using OpenAI’s API and the OpenAI Agents SDK.

# The agent is run once using Runner.run with a question.

# The response is printed, and the whole execution is handled asynchronously using asyncio.