import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load .env environment variables
load_dotenv()

# Get Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():
    """Set up the chat session when a user connects."""
    
    # Initialize external OpenAI-compatible client
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Define the chat model
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    # Configure the run environment
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    # Store necessary objects in session
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    
    agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
    cl.user_session.set("agent", agent)

    await cl.Message(content="Welcome to Samad Chatbot!").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle user message and generate response from agent."""
    
    # Initial response while thinking
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Retrieve session objects
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    history = cl.user_session.get("chat_history") or []

    # Append current user input to history
    history.append({"role": "user", "content": message.content})

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")

        # Run the agent with chat history
        result = Runner.run_sync(
            starting_agent=agent,
            input=history,
            run_config=config
        )

        # Get agent's final response
        response_content = result.final_output

        # Update placeholder message
        msg.content = response_content
        await msg.update()

        # Update chat history in session
        cl.user_session.set("chat_history", result.to_input_list())

        # Optional logging
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")





# import sys
# import os
# import chainlit as cl
# from dotenv import load_dotenv, find_dotenv
# from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner



# # Load environment variables from .env file
# load_dotenv(find_dotenv())

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # STep 1 
# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )



# # step 2
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider,
# )



# # Step 3 
# agent1 = Agent(
#     instructions = "You are a helpful assistant that can answer questions and provide information.",
#     name="Samad Support Agent"
# )

# @cl.on_chat_start
# async def handle_chat_start():
#     cl.user_session.set("history", [])
#     await cl.Message(
#         content="Welcome to the Samad chatbot!",
#     ).send()

# @cl.on_message
# async def handle_message(message: cl.Message):
#     history = cl.user_session.get("history")

#     history.append({"role": "user","content": message.content })
#     result = await Runner.run(
#         agent1,
#         input=history,
#         run_config=RunConfig,
#     )
    
#     history.append({  "role": "assistant",  "content": result.final_utput })
#     cl.user_session.set("history", history)
#     await cl.Message(
#         content=result.final_output,
#     ).send()

# import os
# from dotenv import load_dotenv
# from typing import cast
# import chainlit as cl
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig

# # Load the environment variables from the .env file
# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # Check if the API key is present; if not, raise an error
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


# @cl.on_chat_start
# async def start():
    
#     external_client = AsyncOpenAI(
#         api_key=gemini_api_key,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

#     model = OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client
#     )

#     config = RunConfig(
#         model=model,
#         model_provider=external_client,
#         tracing_disabled=True
#     )
#     """Set up the chat session when a user connects."""
#     # Initialize an empty chat history in the session.
#     cl.user_session.set("chat_history", [])

#     cl.user_session.set("config", config)
#     agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
#     cl.user_session.set("agent", agent)

#     await cl.Message(content="Welcome to samad chatbot?").send()

# @cl.on_message
# async def main(message: cl.Message):
#     """Process incoming messages and generate responses."""
#     # Send a thinking message
#     msg = cl.Message(content="Thinking...")
#     await msg.send()

#     agent: Agent = cast(Agent, cl.user_session.get("agent"))
#     config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

#     # Retrieve the chat history from the session.
#     history = cl.user_session.get("chat_history") or []
    
#     # Append the user's message to the history.
#     history.append({"role": "user", "content": message.content})
    

#     try:
#         print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
#         result = Runner.run_sync(starting_agent = agent,
#                     input=history,
#                     run_config=config)
        
#         response_content = result.final_output
        
#         # Update the thinking message with the actual response
#         msg.content = response_content
#         await msg.update()
    
#         # Update the session with the new history.
#         cl.user_session.set("chat_history", result.to_input_list())
        
#         # Optional: Log the interaction
#         print(f"User: {message.content}")
#         print(f"Assistant: {response_content}")
        
#     except Exception as e:
#         msg.content = f"Error: {str(e)}"
#         await msg.update()
#         print(f"Error: {str(e)}")