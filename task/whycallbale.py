



# 1) Why is the Agent class defined as a @dataclass?

# 2a) Why is the “system prompt” stored in the Agent class as instructions, and why can it also be a callable?

# Single source of truth: Keeping the core “system prompt” with the agent definition bundles behavior and identity together.

# Static or dynamic: Sometimes you want a fixed instruction string; other times you want to generate instructions at runtime (e.g. adding a timestamp, user profile data, or external context). Allowing instructions to be a Callable[[], str] covers both:


def dynamic_instructions() -> str:
    from datetime import datetime
    return f"You are an agent. Current time: {datetime.utcnow().isoformat()}"

agent_static = Agent(name="StaticBot", instructions="Always be friendly.")
agent_dynamic = Agent(name="TimeBot", instructions=dynamic_instructions)

# When running:
inst1 = agent_static.instructions  # "Always be friendly."
inst2 = agent_dynamic.instructions()  # "You are an agent. Current time: 2025-05-23T10:15:00"
