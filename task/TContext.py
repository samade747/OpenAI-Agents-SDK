# 4) What are generics in Python? Why use them for TContext?

# Generics (via the typing module) allow classes and functions to be parameterized by types, improving type safety and clarity.

# In agent code, you often carry around a context object (e.g. conversation history, external state) whose shape can vary. Using a type variable TContext lets you:

# Specify at compile time what type of context your agent will use.

# Avoid Any-typed pockets that defeat static checking.


from typing import TypeVar, Generic

TContext = TypeVar("TContext")

class Agent(Generic[TContext]):
    name: str
    instructions: str
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

class Runner(Generic[TContext]):
    @classmethod
    def run(cls, agent: Agent[TContext], user_input: str, context: TContext) -> TContext:
        # operate on context of the specific type
        return context

# Define a custom context type:
class MyContext:
    prompt_count: int = 0

ctx = MyContext()
agent = Agent[MyContext](name="CtxAgent", instructions="Count prompts.")
new_ctx = Runner[MyContext].run(agent, "Hello", ctx)
