from abc import ABC, abstractmethod, ABCMeta
from typing import TypeVar, Any, List, Callable, Tuple, Dict

from data_struct import *

T = TypeVar('T')


class ISolvable(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_moves') and
                callable(subclass.get_moves) and
                hasattr(subclass, 'compute_move') and
                callable(subclass.compute_move) or
                NotImplemented)

    @abstractmethod
    def get_moves(self) -> List[Any]:
        pass

    @abstractmethod
    def compute_move(self, from_state: '__class__', move_to_apply) -> '__class__':
        pass


class Solver(ABC):
    @abstractmethod
    def solve(self, current: ISolvable, goal_state: ISolvable, heuristic_func: Callable[[ISolvable, ISolvable], float]):
        pass

    @abstractmethod
    def f(self, g, h):
        pass


class AStar(Solver):
    def __init__(self):
        self.search_path = None
        self.nodes_costs = None

    def solve(self, current: ISolvable, goal_state: ISolvable,
              heuristic_func: Callable[[ISolvable, ISolvable], int]) -> \
            Tuple[Dict[ISolvable, Tuple[ISolvable, Any]], Dict[ISolvable, Tuple[int, int, int]]]:
        self.nodes_costs = {}
        states_graph: Dict[ISolvable, Tuple[ISolvable, Any]] = {}  # Key: Node, Value: FromNode
        open_states_set = PriorityQueue()
        open_states_set.enqueue((current, 0, heuristic_func(current, goal_state)), 0)
        closed_states_set = {}

        while not open_states_set.empty():
            f, node = open_states_set.dequeue()
            current_state, g, h = node
            closed_states_set[current_state] = (f, g, h)  # Add in ordered dict representing the closed set

            # Reached goal, return steps to goal + search data
            if current_state == goal_state:
                return states_graph, closed_states_set

            next_moves = current_state.get_moves()
            for puzzle_move in next_moves:
                next_state = current_state.compute_move(current_state, puzzle_move)

                # Closed already
                if next_state in closed_states_set:
                    continue

                # CostSoFar + MoveCost
                next_cost = g + puzzle_move[0]

                # Add or update priority
                next_heuristic = heuristic_func(next_state, goal_state)
                open_states_set.enqueue((next_state, next_cost, next_heuristic), self.f(next_cost, next_heuristic))

                # Where from, and with what move
                states_graph[next_state] = (current_state, puzzle_move)

        # If open set empty, failed to solve
        return None, None

    def f(self, g, h):
        return g + h


# Uniform Cost Search
class UCS(AStar):
    def f(self, g, h):
        # Search by: total cost from the root to node n
        return g


# Greedy Best First Search
class GBFS(AStar):
    def f(self, g, h):
        # Search by: better heuristic only
        return h
