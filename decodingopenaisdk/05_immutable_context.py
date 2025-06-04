# 🌟 Key Concept: Mutable Context in Agents SDK

"""
Mutable Context Benefits:
- Shared State: Tools can collaborate on a single state.
- Persistence: Changes persist across tool calls.
- Flexibility: Agents evolve in response to user inputs.
- Efficiency: Avoid creating new objects repeatedly.

Mutable Types: list, dict, set, custom classes, bytearray
Immutable Types: str, tuple, int, float, bool, frozenset
"""
# ✅ Example 1: User Preferences Agent
# Manage user preferences with a mutable MyContext object.

# Importing tools and types
from agents import Agent, Runner, RunContextWrapper, function_tool
import asyncio


# Define a mutable context class for storing preferences
class MyContext:
    def __init__(self):
        self.user_preferences: dict[str, str] = {}  # mutable dictionary
        self.call_count: int = 0  # keeps track of tool calls

    def add_user_preferences(self, preference: str, value: str):
        self.user_preferences[preference] = value
        self.increment_call_count()  # auto-update call count

    def increment_call_count(self):
        self.call_count += 1

# Tool to save a preference into context
@function_tool
def save_user_preference(ctx: RunContextWrapper[MyContext], preference: str, value: str) -> str:
    ctx.context.add_user_preferences(preference, value)
    return f"Saved {preference}: {value}"

# Tool to retrieve all preferences
@function_tool
def get_user_preferences(ctx: RunContextWrapper[MyContext]) -> dict[str, str]:
    return ctx.context.user_preferences


# Tool to clear preferences
@function_tool
def clear_user_preferences(ctx: RunContextWrapper[MyContext]) -> str:
    ctx.context.user_preferences.clear()
    return "All user preferences cleared"


# Create the agent
agent = Agent(
    name="PreferenceAgent",
    instructions="Help users manage their preferences. Use tools to save, retrieve, and clear preferences.",
    tools=[save_user_preference, get_user_preferences, clear_user_preferences]
)

# Test interaction
async def test_preference_agent():
    context = MyContext()
    result1 = await Runner.run(agent, "Save my favorite color as blue", context=context)
    print(result1.final_output)

    result2 = await Runner.run(agent, "What are all my preferences?", context=context)
    print(result2.final_output)

    result3 = await Runner.run(agent, "Clear all my preferences", context=context)
    print(result3.final_output)

# You can uncomment this in `main()` to test:
# await test_preference_agent()


# ✅ Example 2: Session Tracker Agent
# Track topics discussed, mood, and number of messages.

from datetime import datetime

# Context to track session state
class SessionContext:
    def __init__(self):
        self.messages_count = 0
        self.topics_discussed: set[str] = set()
        self.user_mood = "neutral"
        self.start_time = datetime.now()

    def add_message(self):
        self.messages_count += 1

    def add_topic(self, topic: str):
        self.topics_discussed.add(topic)

    def set_mood(self, mood: str):
        self.user_mood = mood

    def get_session_info(self) -> str:
        return f"Messages: {self.messages_count}, Topics: {self.topics_discussed}, Mood: {self.user_mood}"