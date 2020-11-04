from abc import ABC, abstractmethod, ABCMeta
from enum import Enum
from typing import TypeVar, Any, List
from numpy import ndarray

from data_struct import *

T = TypeVar('T')


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
    def get_state(self) -> ndarray:
        pass

    @abstractmethod
    def set_state(self, new_state: ndarray):
        pass

    @abstractmethod
    def get_moves(self) -> List[Any]:
        pass

    @abstractmethod
    def compute_move(self, from_state: __class__, move_to_apply) -> __class__:
        pass


class Solver(ABC):
    @abstractmethod
    def solve(self, current: ISolvable, goal_state: ISolvable):
        pass


class AStar(Solver):
    def solve(self, current: ISolvable, goal_state: ISolvable) -> List[Any]:
        running_states_graph_edges = {}  # Key: Node, Value: FromNode
        open_states_set = PriorityQueue()
        open_states_set.enqueue(current, 0)
        closed_states_set = set()

        # Retracing steps backward
        def retrace_steps(final_state) -> List[Any]:
            steps = []
            c = final_state
            while c in running_states_graph_edges:
                steps.append(c)
                c = running_states_graph_edges[c]

            steps.reverse()
            return steps

        while not open_states_set.empty():
            current_cost, current_state = open_states_set.dequeue()

            # Reached goal, return steps to goal
            if current_state == goal_state:
                return retrace_steps(current_state)

            next_moves = current_state.get_moves()
            for puzzle_move in next_moves:
                next_state = current_state.compute_move(current_state, puzzle_move)

                # Closed already
                if next_state in closed_states_set:
                    continue

                next_cost = current_cost + puzzle_move[0]

                # Add or update priority
                open_states_set.enqueue(next_state, next_cost)

    @abstractmethod
    def heuristic(self, current_state: T, goal_state: T) -> float:
        # h(n)
        pass


class Djikstra(AStar):
    def heuristic(self, current_state: T, goal_state: T) -> float:
        return 0
