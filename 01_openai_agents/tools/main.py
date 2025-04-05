# Import necessary libraries
import os  # For accessing environment variables
from dotenv import load_dotenv  # To load environment variables from a .env file
from typing import cast, List  # For type hinting
import chainlit as cl  # Chainlit is used to build conversational AI interfaces

# Import custom classes and functions from local modules
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool

# Load environment variables from the .env file into the system environment
load_dotenv()

# Retrieve the GEMINI_API_KEY from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Raise an error if the API key is missing
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Define starter prompts for the chat interface
@cl.set_starters  # Decorator to register initial options when chat starts
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Greetings",  # Label shown to user
            message="Hello! What can you help me with today?",  # Message sent if clicked
        ),
        cl.Starter(
            label="Weather",
            message="Find the weather in Karachi.",
        ),
    ]

# Create a custom tool using the @function_tool decorator that Chainlit can call
@function_tool
@cl.step(type="weather tool")  # Register this step as a "weather tool"
def get_weather(location: str, unit: str = "C") -> str:
    """
    Fetch the weather for a given location, returning a short description.
    In a real app, you would fetch this from a weather API.
    """
    # Example hardcoded weather result
    return f"The weather in {location} is 22 degrees {unit}."

# Called when a new chat session starts
@cl.on_chat_start
async def start():
    # Reference link to the Gemini API
    # https://ai.google.dev/gemini-api/docs/openai

    # Initialize the external OpenAI-compatible client with Gemini settings
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Create a chat model using Gemini through the OpenAI-compatible interface
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    # Configuration for running the agent
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True  # Disable tracing/debug tracking
    )

    # Save empty chat history in user session
    cl.user_session.set("chat_history", [])

    # Save the config in the user session
    cl.user_session.set("config", config)

    # Create an agent (like a chatbot) with a name and basic instruction
    agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

    # Add the custom weather tool to the agent
    agent.tools.append(get_weather)

    # Save the agent in user session
    cl.user_session.set("agent", agent)

    # Send a welcome message to the user
    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()

# Called when a user sends a message
@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""

    # Send a temporary message to show that the assistant is thinking
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Get the agent object from the session and cast it to correct type
    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    # Get the config object from the session
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve chat history or initialize an empty list
    history = cl.user_session.get("chat_history") or []

    # Add the user's new message to the history
    history.append({"role": "user", "content": message.content})

    try:
        # Log for debugging: show current conversation history
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")

        # Run the agent with the given history and config to generate a response
        result = Runner.run_sync(agent, history, run_config=config)

        # Get the final response from the agent
        response_content = result.final_output

        # Update the "Thinking..." message with the actual reply
        msg.content = response_content
        await msg.update()

        # Add the assistant's response to the history
        history.append({"role": "developer", "content": response_content})
        # Note: This is a known bug — it should be "assistant", not "developer"

        # Save updated history back to the session
        cl.user_session.set("chat_history", history)

        # Optional logging
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    # Catch any error and update the user with the error message
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
