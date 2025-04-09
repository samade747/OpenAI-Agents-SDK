# callable in python 


# callable is a built-in function in Python that checks if an object appears to be callable (i.e., can be called as a function).
# It returns True if the object appears callable, and False otherwise.
# This can be useful for checking if an object is a function, method, or an object with a __call__() method.

# The callable() function is a built-in function in Python that checks if an object appears to be callable (i.e., can be called as a function).


from typing import Callable

# callable function takes two integers and return a string
#                      Input: 1, 2
#                                   Output: "1 + 2 = 3" 
MyFuncType = callable[[int, int], str]

print(MyFuncType) # <class 'callable'>


#Use case
from dataclasses import dataclass
from typing import Callable

@dataclass
class Calculator:
    operation: Callable[[int, int], str]

    def calculate(self, a: int, b: int) -> str:
        return self.operation(a, b)

def add_stringly(x: int, y: int) -> str:
    return str(x + y)

calc = Calculator(operation=add_stringly)
result = calc.calculate(1, 2)


print(result)  # Output: "3"
print(callable(calc))  # Output: True


