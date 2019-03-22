"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from copy import deepcopy
from typing import Any
from game import Game


class Stack:
    """
    Last-in, first-out (LIFO) stack.
    """

    def __init__(self) -> None:
        """
        Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contents = []

    def add(self, obj: object) -> None:
        """
        Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(7)
        """
        self._contents.append(obj)

    def remove(self) -> object:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not empty.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contents.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(7)
        >>> s.is_empty()
        False
        """
        return len(self._contents) == 0


class Tree:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.
    """

    def __init__(self, state=None, score=None, children=None, m=None) -> None:
        """
        Create Tree self with content value and 0 or more children
        """
        self.state = state
        self.score = score
        # copy children if not None
        self.children = children[:] if children is not None else []
        self.move = m

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

# TODO: Implement a recursive version of the minimax strategy.


def helper(game):
    """"helper function for recursive minimax"""
    best_score = -2
    game_copy = deepcopy(game)  # make a copy of the game
    if game_copy.is_over(game_copy.current_state):  # base case
        if game_copy.is_winner(
                game_copy.current_state.get_current_player_name()):
            return 1
        elif not game_copy.is_winner('p1') and not game_copy.is_winner('p2'):
            return 0

        return -1
    else:
        moves = game_copy.current_state.get_possible_moves()
        for move in moves:
            game_copy_1 = deepcopy(game_copy)
            game_copy_1.current_state = game_copy_1.current_state.make_move(
                move)
            score = helper(game_copy_1) * -1
            if score > best_score:
                best_score = score

        return best_score


def recursive_minimax(game: Game):
    """ Returns a move that maximises the chances of winning"""
    moves = game.current_state.get_possible_moves()
    best_score = -2
    for move in moves:
        weiran = deepcopy(game)
        weiran.current_state = weiran.current_state.make_move(move)
        score = helper(weiran) * -1
        if score > best_score:
            best_score = score
            score_move_tup = (best_score, move)
    return score_move_tup[1]

# TODO: Implement an iterative version of the minimax strategy.


def iterative_minimax(game)-> Any:
    """a strategy to give the highest guranteeable score"""

    stack = Stack()
    game_copy = deepcopy(game)
    t = Tree(game_copy.current_state)
    stack.add(t)
    while not stack.is_empty():
        check = stack.remove()
        if game_copy.is_over(check.state):
            game_copy.current_state = check.state
            if game_copy.is_winner\
                        (game_copy.current_state.get_current_player_name()):
                check.score = 1
            elif not game_copy.is_winner('p1') \
                    and not game_copy.is_winner('p2'):
                check.score = 0
            else:
                check.score = -1

        elif check.children != []:
            check.score = max([-1*c.score for c in check.children])

        else:
            check.children = []
            stack.add(check)
            for move in check.state.get_possible_moves():
                check_new_state = deepcopy(check.state)
                child_move = Tree(check_new_state.make_move(move))
                child_move.move = move
                check.children.append(child_move)
                stack.add(child_move)

    max_score = -5
    move_to_make = None
    for child in t.children:
        if child.score*-1 > max_score:
            max_score = child.score*-1
            move_to_make = child.move

    return move_to_make


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
