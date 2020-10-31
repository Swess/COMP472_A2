from typing import TypeVar, Generic, List

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        # Create an empty list with items of type T
        self.__items: List[T] = []

    def push(self, item: T) -> None:
        self.__items.append(item)

    def pop(self) -> T:
        return self.__items.pop()

    def empty(self) -> bool:
        return not self.__items
