import heapq
from typing import Tuple, TypeVar, Generic, List

T = TypeVar('T')
QueueEntry = Tuple[int, T]


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self.__heap: List[QueueEntry] = []

    def enqueue(self, item: QueueEntry) -> None:
        heapq.heappush(self.__heap, item)

    def dequeue(self) -> QueueEntry:
        return heapq.heappop(self.__heap)

    def empty(self) -> bool:
        return len(self.__heap) == 0
