import heapq
import itertools
from typing import TypeVar, Generic, List

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self.__counter = itertools.count()  # unique sequence count
        self.__registry = {}
        self.__heap: List[List[int, int, T]] = []

    def enqueue(self, item: T, priority: int = 0) -> None:
        # If exist, remove to update priority
        if item in self.__registry:
            self.__remove(item)

        count = next(self.__counter)
        entry = [priority, count, item]
        self.__registry[item] = entry
        heapq.heappush(self.__heap, entry)

    def __remove(self, item: T) -> None:
        entry = self.__registry.pop(item)
        entry[-1] = None

    def dequeue(self) -> T:
        while self.__heap:
            priority, count, item = heapq.heappop(self.__heap)
            if item is not None:
                del self.__registry[item]
                return item
        raise KeyError('dequeue from an empty priority queue')

    def empty(self) -> bool:
        return len(self.__heap) == 0

    def __contains__(self, item: T):
        return item in self.__registry
