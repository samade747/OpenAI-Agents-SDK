
### 1. Why is `Agent` a dataclass?

A **dataclass** automatically generates common methods like `__init__`, `__repr__`, and `__eq__`. Since `Agent` mostly holds configuration (name, instructions, tools, etc.), using `@dataclass`:

* Reduces boilerplate code
* Provides a clear, declarative syntax
* Supports default values and factories easily
* Helps with debugging via a readable `repr`

```python
from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass
class Agent:
    name: str
    instructions: str | Callable[[], str]
    tools: list[Any] = field(default_factory=list)
```

### 2a. Why is the system prompt in `Agent` as `instructions` and callable?

* **Field name**: `instructions` holds the agent’s system prompt (its “job description”).
* **Callable support**: Sometimes you need a dynamic prompt (e.g. including the current time or user profile). Allowing `instructions` to be a function lets you generate the prompt at runtime.

```python
# Static prompt example
ing = Agent(name="StaticBot", instructions="Always be friendly.")

# Dynamic prompt example
def dynamic_instructions():
    from datetime import datetime
    return f"Current time: {datetime.utcnow()}"

dag = Agent(name="TimeBot", instructions=dynamic_instructions)
```

During execution, the runner checks if `instructions` is callable and, if so, calls it to get the final prompt.

### 2b. Why is the user prompt passed to `Runner.run()`?

* **Separation of concerns**:

  * `Agent` defines *how* to think (system prompt, tools).
  * `Runner` handles *when* and *what* to run.
* **Reusability**: You can call the same `Agent` on multiple different user inputs without changing the agent itself.

```python
from openai_agents import Runner
# You can reuse `agent` for different inputs:
out1 = Runner.run(agent, input="What is 2+2?")
out2 = Runner.run(agent, input="Tell me a joke.")
```

### 3. What is the purpose of the `Runner` class?

`Runner` manages the full agent execution loop:

1. **Builds messages**: Combines the system prompt (`instructions`) and user input.
2. **Calls the LLM**: Sends messages to OpenAI.
3. **Tool dispatch**: If the agent’s response asks to use a tool, `Runner` calls that tool and adds the tool output back.
4. **Handoffs**: Switches to another agent if instructed.
5. **Termination**: Stops when the agent gives a final answer or exceeds turn limits.

This encapsulation keeps your main code clean and focuses on defining agents, not on orchestration details.

### 4. What are generics in Python? Why use `TContext`?

* **Generics** (via `typing.TypeVar` and `Generic`) let classes and functions work with different types while preserving type safety.
* `TContext` is a placeholder type for a context object you pass through the run (e.g. to track state).
* Declaring `Agent[TContext]` and `Runner[TContext]` ensures your context type is consistent throughout.

```python
from typing import TypeVar, Generic

TContext = TypeVar("TContext")

class Agent(Generic[TContext]):
    name: str
    # ... other fields

class Runner(Generic[TContext]):
    def run(
        cls,
        agent: Agent[TContext],
        input: str,
        context: TContext,
    ) -> TContext:
        # use context safely
        return context
```

---


