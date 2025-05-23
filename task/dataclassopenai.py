# 1) Why is the Agent class defined as a @dataclass?
# The OpenAI Agents SDK marks Agent with @dataclass 
# to streamline the creation and management of its many 
# configuration fields 
# (e.g. name, instructions, tools, handoffs, # etc.). 
# By using a dataclass, the SDK automatically generates an __init__, __repr__, and __eq__, 
# reducing boilerplate and improving debugging. It also supports default factories
#  (e.g. for tools and handoffs) and makes cloning simple via dataclasses.replace under the hood 




from dataclasses import dataclass, field
from typing import Callable, Generic, TypeVar

TContext = TypeVar("TContext")

@dataclass
class Agent(Generic[TContext]):
    name: str
    instructions: str  # system prompt
    tools: list = field(default_factory=list)
    handoffs: list = field(default_factory=list)
    # ... many more fields with defaults
