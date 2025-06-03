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

# ⚙️ Callable (Dynamic) Instructions

# Example 3: Simple callable function to generate instructions dynamically
def dynamic_instructions(context, agent):
    print("RECEIVED CONTEXT", context)
    print("RECEIVED AGENT", agent)
    return f"You are {agent.name}. Respond professionally and helpfully."

# Agent with callable instructions
agent_callable = Agent(
    name="DynamicAgent",
    instructions=dynamic_instructions
)


# 🧠 Context-Aware Callable Instructions

# Example 4: Callable that adapts based on conversation history
def context_aware_instructions(context, agent):
    print("RECEIVED CONTEXT", context)
    print("RECEIVED AGENT", agent)

    # Check number of past messages in the context
    message_count = len(getattr(context, 'messages', []))
    
    if message_count == 0:
        return "You are a friendly assistant. Introduce yourself and ask how you can help."
    elif message_count < 3:
        return "You are a helpful assistant. Be encouraging and detailed in your responses."
    else:
        return "You are an experienced assistant. Be concise but thorough."

# Agent using context-aware instructions
agent_context_aware = Agent(
    name="ContextAwareAgent",
    instructions=context_aware_instructions
)

# 🧪 Test Functions for Callable & String-Based Instructions

# Run agents with callable instructions
async def test_callable_instructions():
    result1 = await Runner.run(agent_callable, "Hello!")
    print("Callable Agent:", result1.final_output)
    
    result2 = await Runner.run(agent_context_aware, "What's the weather like?")
    print("Context Aware Agent:", result2.final_output)

# Run agents with static string-based instructions
async def test_string_instructions():
    result1 = await Runner.run(agent_basic, "What is Python?")
    print("Basic Agent:", result1.final_output)
    
    result2 = await Runner.run(agent_detailed, "How do I create a list comprehension?")
    print("Detailed Agent:", result2.final_output)


# ⏱️ Async Callable Instructions (Real-time example)


# Example 5: Async callable instructions that simulate delay or real-time info
async def async_instructions(context, agent):
    await asyncio.sleep(0.1)  # Simulate I/O delay (e.g., fetching info)
    current_time = asyncio.get_event_loop().time()
    parsed_time = datetime.fromtimestamp(current_time)
    
    return f"""You are {agent.name}, an AI assistant with real-time capabilities.
    Current timestamp: {parsed_time}
    Provide helpful and timely responses."""

# Agent with async instructions
agent_async = Agent(
    name="AsyncAgent",
    instructions=async_instructions
)

# Test function for async instructions
async def test_async_instructions():
    result = await Runner.run(agent_async, "What time is it?")
    print("Async Agent:", result.final_output)


# 🧠 Stateful Callable Instructions


# Example 7: Callable object that tracks interaction count (stateful)
class InstructionGenerator:
    def __init__(self):
        self.interaction_count = 0  # Track how many times it's been called

    def __call__(self, context, agent):
        self.interaction_count += 1

        if self.interaction_count == 1:
            return "You are a learning assistant. This is our first interaction - be welcoming!"
        elif self.interaction_count <= 3:
            return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation."
        else:
            return f"You are an experienced learning assistant. We've had {self.interaction_count} interactions - be efficient."

# Instantiate and assign the instruction generator
instruction_gen = InstructionGenerator()

# Agent using the stateful callable for instructions
agent_stateful = Agent(
    name="StatefulAgent",
    instructions=instruction_gen
)

# Test function to show stateful instruction evolution
async def test_stateful_instructions():
    for i in range(4):  # Run 4 interactions to demonstrate instruction evolution
        result = await Runner.run(agent_stateful, f"Question {i+1}: Tell me about Python")
        print(f"Interaction {i+1}:", result.final_output[:100] + "...")


# 🚀 Program Entry Point

# Main function to run all tests
def main():
    print("\n[1. STRING INSTRUCTIONS]")
    asyncio.run(test_string_instructions())  # Test string instruction agents
    
    print("\n[2. CALLABLE INSTRUCTIONS]")
    asyncio.run(test_callable_instructions())  # Test callable instruction agents
    
    print("\n[3. ASYNC INSTRUCTIONS]")
    asyncio.run(test_async_instructions())  # Test async instruction agent
    
    print("\n[4. STATEFUL INSTRUCTIONS]")
    asyncio.run(test_stateful_instructions())  # Test stateful callable instructions

# Run main if file is executed directly
if __name__ == "__main__":
    main()

# ✅ Summary of Instruction Types:

# | Example | Instruction Type         | Notes                                                              |
# | ------- | ------------------------ | ------------------------------------------------------------------ |
# | 1       | Static String            | Basic predefined instructions                                      |
# | 2       | Static String (Detailed) | Richer guidance and tone control                                   |
# | 3       | Callable Function        | Generates instructions dynamically using agent context             |
# | 4       | Context-Aware Callable   | Uses conversation history to adjust instructions                   |
# | 5       | Async Callable           | Useful for time-based or external I/O-based instruction generation |
# | 6       | —                        | (Skipped in your example, not needed)                              |
# | 7       | Stateful Callable Class  | Remembers past interactions and adapts instructions accordingly    |
