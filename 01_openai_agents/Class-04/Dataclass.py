from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Person:
    name: str
    age: int
    email: str | None = None
    tags: list[str] = field(default_factory=list)


    def is_adult(self) -> bool:
        return self.age >= 18
    
def demo_good_usage():
    person1 = Person("John", 25, "8VWQ7@example.com", )
    person2 = Person("Alice", 17 )
    person3 = Person("Bob", 30, "n7FVZ@example.com", tags=["student", "part-time"])



     



