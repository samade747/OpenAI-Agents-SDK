#understanding generics in python

from typing import TypeVar, Generic, List, Dict, Tuple, Any

#type variable for generic typing
T = TypeVar('T')

def generic_first_element(items: list[T]) -> T:
    return items[0]

nums = [1, 2, 3, 4, 5]  # Define nums as a list of numbers
strings = ['apple', 'banana', 'cherry']  # Define strings as a list of strings

# Define a list of tuples with mixed types  
mixed = [(1, 'apple'), (2, 'banana'), (3, 'cherry')]

# Define a list of dictionaries with mixed types
dicts = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]


num_result = generic_first_element(nums)
string_result = generic_first_element(strings)
mixed_result = generic_first_element(mixed)
dict_result = generic_first_element(dicts) 

print(num_result)  # Output: 1
print(string_result)  # Output: 'apple'







