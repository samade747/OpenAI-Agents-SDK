# Import required libraries
from datetime import datetime
from agents import Agent, Runner  # Core classes from OpenAI Agents SDK
import asyncio  # Used to handle async operations


# 🚀 Agent Instruction Variants

# Example 1: Basic static string instructions
agent_basic = Agent(
    name="BasicAgent",
    instructions="You are a helpful assistant that provides concise answers."
)

# Example 2: More detailed static string instructions
agent_detailed = Agent(
    name="DetailedAgent", 
    instructions="""You are an expert Python developer.
    - Always provide working code examples
    - Explain your reasoning step by step
    - Keep responses under 200 words
    - Use best practices and modern Python syntax"""
)
