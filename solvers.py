from abc import ABC, abstractmethod, ABCMeta
from enum import Enum
from typing import TypeVar, Generic, List, Tuple
from data_struct import *

T = TypeVar('T')
Solvable = Generic[T]


class SearchType(Enum):
    DIJKSTRA = 1  # aka: Uniform Cost Search (UCS)
    GBFS = 2  # aka: Greedy Breadth First Search
    ASTAR = 3


class ISolvable(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_state') and
                callable(subclass.get_state) and
                hasattr(subclass, 'get_moves') and
                callable(subclass.get_moves) or
                NotImplemented)

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def get_moves(self) -> List[Tuple[int, int]]:
        pass


class Solver(ABC):
    def __init__(self, target: ISolvable) -> None:
        super().__init__()
        self.target = target

    def solve(self):
        pass


class AStar(Solver):
    @abstractmethod
    def heuristic(self, current: T, goal: T) -> float:
        # h()
        pass

    @abstractmethod
    def travel_cost(self) -> float:
        # g(n)
        pass


class Djikstra(AStar):
    def heuristic(self, current: T, goal: T) -> float:
        return 0

    def travel_cost(self) -> float:
        pass
