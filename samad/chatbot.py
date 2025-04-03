import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
from agents import Agent, runConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner



# Load environment variables from .env file
load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

# STep 1 
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)



# step 2
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)



# Step 3 
agent1 = Agent(
    instruction = "You are a helpful assistant that can answer questions and provide information.",
    name="Samad Support Agent"
)

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Welcome to the Samad chatbot!",
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    history.append({"role": "user",
                    "content": message.content })
    result = await Runner.run(
        agent1,
        input=history,
        run_config=runConfig,
    )
    
    history.append({  "role": "assistant",  "content": result.final_utput })
    cl.user_session.set("history", history)
    await cl.Message(
        content=result.final_output,
    ).send()

