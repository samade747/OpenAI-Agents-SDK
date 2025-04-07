
from dataclasses import dataclass

from typing import ClassVar

@dataclass
class American:
  national_language: ClassVar[str] = "English"
  national_food: ClassVar[str] = "Hamburger"
  normal_body_temperature: ClassVar[float] = 98.6
  name: str
  age: int
  weight: float
  liked_food: str

  def speaks(self):
    return f"{self.name} is speaking... {American.national_language}"

  def eats(self):
    return f"{self.name} is eating..."

  @staticmethod
  def country_language():
    return American.national_language
  

American.country_language()


john = American(name="John", age=25, weight=65, liked_food="P")
print(john.speaks())
print(john.eats())


print(john)
print(john.name)
print(john.age)
print(john.weight)
print(American.national_language)