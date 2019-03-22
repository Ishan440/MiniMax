"""
Superclass Game
"""
from typing import Any
from game_state import GameState, StoneHengeState


class Game:
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        raise NotImplementedError

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        raise NotImplementedError

    def is_over(self, state: GameState) -> bool:
        """
        Return whether or not this game is over at state.
        """
        raise NotImplementedError

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        raise NotImplementedError

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        raise NotImplementedError


"""A place where the magic of stonehenge happens"""


# Helper Functions

def dict_rows(n: int)-> dict:
    """A board generator for the game stonehenge"""
    cells = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z']
    lc = 2
    row = 2
    d = [cells[0:2]]
    while row < n+1:
        d.append(cells[lc:lc + row + 1])
        lc += row + 1
        row += 1
    d.append(cells[lc:lc+n])
    rows = {}
    for num in range(n):
        rows['row{}'.format(num + 1)] = d[num]
    rows['row{}'.format(n + 1)] = d[-1]
    return rows


def ley_lines_horizontal(n)->dict:
    """Makes the initlal horizontal ley lines"""
    hlm = {}
    rows = dict_rows(n)
    marker = '@'
    for row in rows:
        hlm[row] = marker
    return hlm


def ley_lines_vertical(n)->dict:
    """Makes the initial vertical ley lines"""
    vlm = {}
    num_vlm = []
    marker = '@'
    for _ in range(n*2 + 2):
        num_vlm.append(marker)
    vlm['first2'] = num_vlm[0:2]
    vlm['lastn'] = num_vlm[2:n + 2]
    vlm['siden'] = num_vlm[n + 2:]
    return vlm


# *****************************************************************************


class StoneHenge(Game):
    """The stonehenge game"""

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        self.is_p1_turn = p1_starts
        self.board = int(input('choose the size of the board: '))
        cells = dict_rows(self.board)
        hlm = ley_lines_horizontal(self.board)
        vlm = ley_lines_vertical(self.board)
        self.current_state = StoneHengeState(self.is_p1_turn, self.board, cells,
                                             hlm, vlm)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        return """Players choose cells one by one and the player to capture
        more than half lines in a leyline captures that leyline. The player
        who captures more than half the leylines first wins the game"""

    def is_over(self, state: GameState) -> bool:
        """
        Return whether or not this game is over at state.
        """
        # when all the leylines have been captured, the game is over
        over = False
        hori = []
        verti = []
        for row in state.hlm:
            hori.append(state.hlm[row])
        for row in state.vlm:
            verti.extend(state.vlm[row])
        total = hori + verti
        num_1 = total.count('1')
        num_2 = total.count('2')
        if len(total) % 2 == 0:
            need = len(total) / 2
        else:
            need = len(total) // 2 + 1
        if num_1 >= need or num_2 >= need:
            over = True
        return over

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        hori = []
        verti = []
        for row in self.current_state.hlm:
            hori.append(self.current_state.hlm[row])
        for row in self.current_state.vlm:
            verti.extend(self.current_state.vlm[row])
        total = hori + verti
        num_1 = total.count('1')
        num_2 = total.count('2')
        if num_1 > num_2 and self.is_over(self.current_state):
            return player == 'p1'
        elif num_2 > num_1 and self.is_over(self.current_state):
            return player == 'p2'

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        if string in self.current_state.get_possible_moves():
            return string

        return 'some invalid move'


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
