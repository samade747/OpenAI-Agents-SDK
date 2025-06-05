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
    



# Tools
@function_tool
def track_topic(ctx: RunContextWrapper[SessionContext], topic: str) -> str:
    ctx.context.add_topic(topic)
    return f"Tracking topic: {topic}"

@function_tool
def set_mood(ctx: RunContextWrapper[SessionContext], mood: str) -> str:
    ctx.context.set_mood(mood)
    return f"Mood set to: {mood}"

@function_tool
def get_session_info(ctx: RunContextWrapper[SessionContext]) -> str:
    return ctx.context.get_session_info()

# Agent
session_agent = Agent(
    name="SessionAgent",
    instructions="Help users track topics and mood.",
    tools=[track_topic, set_mood, get_session_info]
)

async def test_session_agent():
    context = SessionContext()
    messages = [
        "Let's talk about AI",
        "I'm feeling happy today",
        "Now I want to discuss neural networks",
        "Can you give me session info?"
    ]

    for msg in messages:
        context.add_message()  # update msg count
        result = await Runner.run(session_agent, msg, context=context)
        print(result.final_output)



# ✅ Example 3: Advanced Memory and Task Agent
# Track conversation memory, profile, and tasks.


from typing import Dict, List, Any

# Context with memory and task support
class AdvancedContext:
    def __init__(self):
        self.user_profile: Dict[str, Any] = {}
        self.conversation_memory: List[str] = []
        self.task_queue: List[str] = []
        self.completed_tasks: List[str] = []

    def add_memory(self, memory: str):
        self.conversation_memory.append(memory)
        if len(self.conversation_memory) > 10:
            self.conversation_memory.pop(0)

    def add_task(self, task: str):
        self.task_queue.append(task)

    def complete_task(self, task: str):
        if task in self.task_queue:
            self.task_queue.remove(task)
            self.completed_tasks.append(task)
            return True
        return False

# Tools
@function_tool
def remember_fact(ctx: RunContextWrapper[AdvancedContext], fact: str) -> str:
    ctx.context.add_memory(fact)
    return f"Remembered: {fact}"

@function_tool
def add_task(ctx: RunContextWrapper[AdvancedContext], task: str) -> str:
    ctx.context.add_task(task)
    return f"Added task: {task}"

@function_tool
def complete_task(ctx: RunContextWrapper[AdvancedContext], task: str) -> str:
    if ctx.context.complete_task(task):
        return f"Completed: {task}"
    return f"Task not found: {task}"

@function_tool
def get_status(ctx: RunContextWrapper[AdvancedContext]) -> Dict[str, Any]:
    return {
        "memories": ctx.context.conversation_memory,
        "pending_tasks": ctx.context.task_queue,
        "completed_tasks": ctx.context.completed_tasks,
        "profile": ctx.context.user_profile
    }

@function_tool
def update_profile(ctx: RunContextWrapper[AdvancedContext], key: str, value: str) -> str:
    ctx.context.user_profile[key] = value
    return f"Updated profile: {key} = {value}"

# Agent
advanced_agent = Agent(
    name="AdvancedAgent",
    instructions="Remember things, manage tasks, update profile, and provide status.",
    tools=[remember_fact, add_task, complete_task, get_status, update_profile]
)

async def test_advanced_agent():
    context = AdvancedContext()
    interactions = [
        "I'm John, a Python developer",
        "Add a task to finish my ML project",
        "Remind me to call Alice",
        "I completed the ML project",
        "What’s my status?"
    ]

    for msg in interactions:
        print(f"User: {msg}")
        result = await Runner.run(advanced_agent, msg, context=context)
        print("Agent:", result.final_output)

        # Optional: show current context state after each run
        print(f"Memories: {context.conversation_memory}")
        print(f"Tasks: {context.task_queue}")
        print(f"Done: {context.completed_tasks}")
        print(f"Profile: {context.user_profile}")




# 🔄 main() to test any of the above
        async def main():
    # Uncomment any one to test
    # await test_preference_agent()
    # await test_session_agent()
    await test_advanced_agent()

if __name__ == "__main__":
    asyncio.run(main())


# # ✅ Summary
# | Agent           | Context Used      | Tools                                      |
# | --------------- | ----------------- | ------------------------------------------ |
# | PreferenceAgent | `MyContext`       | Save, retrieve, and clear user preferences |
# | SessionAgent    | `SessionContext`  | Track topics, mood, session state          |
# | AdvancedAgent   | `AdvancedContext` | Manage memory, tasks, profile, and status  |
