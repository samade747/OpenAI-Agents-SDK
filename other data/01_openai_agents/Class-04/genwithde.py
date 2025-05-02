# #understanding generics in python

from typing import TypeVar, Generic, List, Dict, Tuple, Any, ClassVar, Optional, Union, Callable, Type, cast, field

# #type variable for generic typing
T = TypeVar('T')

# def generic_first_element(items: list[T]) -> T:
#     return items[0]

# nums = [1, 2, 3, 4, 5]  # Define nums as a list of numbers
# strings = ['apple', 'banana', 'cherry']  # Define strings as a list of strings

# # Define a list of tuples with mixed types  
# mixed = [(1, 'apple'), (2, 'banana'), (3, 'cherry')]

# # Define a list of dictionaries with mixed types
# dicts = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]


# num_result = generic_first_element(nums)
# string_result = generic_first_element(strings)
# mixed_result = generic_first_element(mixed)
# dict_result = generic_first_element(dicts) 

# print(num_result)  # Output: 1
# print(string_result)  # Output: 'apple'



# # with dic

# K = TypeVar('K') # Type variable for keys
# V = TypeVar('V') # Type variable for values

# def get_item(container: Dict[K, V], key: K) -> V:
#     return container[key]


# d = {'a': 1, 'b': 2, 'c': 3}

# value = get_item(d, 'b')  # returns int

# print(value)  # Output: 2

 
# usage in data class  

class Stack(Generic[T]):
    items: List[T] = field(default_factory=list)
    limit: ClassVar[int] = 10

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

stack_of_ints = Stack[int]()
print(stack_of_ints)  # Output: Stack[int](items=[])

stack_of_ints.push(1)
stack_of_ints.push(2)
stack_of_ints.push(3)
print(stack_of_ints)  # Output: Stack[int](items=[1, 2, 3])

stack_of_ints.pop() 
print(stack_of_ints)  # Output: Stack[int](items=[1, 2])
stack_of_ints.push(4)





