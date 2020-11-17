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
    # Retracing steps of solution backward in resulting search graph
    def _retrace_steps(self, search_graph: Dict[ISolvable, Tuple[ISolvable, Any]], final_state: ISolvable) -> List[
        Tuple[ISolvable, int, int]]:
        steps = []
        c = final_state
        while c in search_graph.keys():
            prev_state, move = search_graph[c]
            steps.append((c, move[0], prev_state[move[1]]))
            c = prev_state

        steps.append((c, 0, 0))  # Initial state
        steps.reverse()
        return steps

    @abstractmethod
    def solve(self, current: ISolvable, goal_states: List[ISolvable],
              heuristic_func: Callable[[ISolvable, ISolvable], float]):
        pass

    @abstractmethod
    def f(self, g, h):
        pass


class AStar(Solver):

    def solve(self, current: ISolvable, goal_states: List[ISolvable],
              heuristic_func: Callable[[ISolvable, ISolvable], int]) -> \
            Tuple[List[Tuple[ISolvable, int, int]], Dict[ISolvable, Tuple[int, int, int]]]:
        states_graph: Dict[ISolvable, Tuple[ISolvable, Any]] = {}  # Key: Node, Value: FromNode
        open_states_set = PriorityQueue()
        open_states_set.enqueue((current, 0, 0), 0)
        closed_states_set = {}

        while not open_states_set.empty():
            f, node = open_states_set.dequeue()
            current_state, g, h = node
            closed_states_set[current_state] = (f, g, h)  # Add in ordered dict representing the closed set

            # Reached a goal, return search data
            if current_state in goal_states:
                return self._retrace_steps(states_graph, current_state), closed_states_set

            next_moves = current_state.get_moves()
            for puzzle_move in next_moves:
                next_state = current_state.compute_move(current_state, puzzle_move)

                # Closed already
                if next_state in closed_states_set:
                    continue

                # CostSoFar + MoveCost
                next_cost = g + puzzle_move[0]

                # Add or update priority
                next_heuristic = float('inf')
                for goal in goal_states:
                    next_heuristic = min(next_heuristic, heuristic_func(next_state, goal))

                next_f = self.f(next_cost, next_heuristic)
                entry = (next_state, next_cost, next_heuristic)

                # If already in open, don't update if it's a worst path
                if entry in open_states_set:
                    look_f, _ = open_states_set[entry]
                    if look_f <= next_f:
                        continue

                # Add or Update
                open_states_set.enqueue((next_state, next_cost, next_heuristic), next_f)

                # Where from, and with what move
                states_graph[next_state] = (current_state, puzzle_move)

        # If open set empty, failed to solve
        return None, None

    def f(self, g, h):
        return g + h


# Uniform Cost Search
class UCS(Solver):

    def solve(self, current: ISolvable, goal_states: List[ISolvable],
              heuristic_func: Callable[[ISolvable, ISolvable], float]):
        self.nodes_costs = {}
        states_graph: Dict[ISolvable, Tuple[ISolvable, Any]] = {}  # Key: Node, Value: FromNode
        open_states_set = PriorityQueue()
        open_states_set.enqueue((current, 0, 0), 0)
        closed_states_set = {}

        while not open_states_set.empty():
            cost, node = open_states_set.dequeue()
            current_state, _, _ = node
            closed_states_set[current_state] = (cost, cost, 0)  # Add in ordered dict representing the closed set

            # Reached a goal, return search data
            if current_state in goal_states:
                return self._retrace_steps(states_graph, current_state), closed_states_set

            next_moves = current_state.get_moves()
            for puzzle_move in next_moves:
                next_state = current_state.compute_move(current_state, puzzle_move)

                # CostSoFar + MoveCost
                next_cost = cost + puzzle_move[0]

                # Closed already & better solution, back to open
                if (next_state not in closed_states_set) or (
                        next_state in closed_states_set and closed_states_set[next_state][0] > next_cost):
                    if next_state in closed_states_set:
                        del closed_states_set[next_state]

                    # Add or Update
                    open_states_set.enqueue((next_state, next_cost, 0), next_cost)
                    states_graph[next_state] = (current_state, puzzle_move)

        # If open set empty, failed to solve
        return None, None

    def f(self, g, h):
        # Search by: total cost from the root to node n
        return g


# Greedy Best First Search
class GBFS(AStar):
    def f(self, g, h):
        # Search by: better heuristic only
        return h
