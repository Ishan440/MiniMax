"""
The GameState superclass.

NOTE: You do not have to run python-ta on this file.
"""
from typing import Any


class GameState:
    """
    The state of a game at a certain point in time.

    WIN - score if player is in a winning position
    LOSE - score if player is in a losing position
    DRAW - score if player is in a tied position
    p1_turn - whether it is p1's turn or not
    """
    WIN: int = 1
    LOSE: int = -1
    DRAW: int = 0
    p1_turn: bool

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        """
        self.p1_turn = is_p1_turn

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        raise NotImplementedError

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        raise NotImplementedError

    def get_current_player_name(self) -> str:
        """
        Return 'p1' if the current player is Player 1, and 'p2' if the current
        player is Player 2.
        """
        if self.p1_turn:
            return 'p1'
        return 'p2'

    def make_move(self, move: Any) -> 'GameState':
        """
        Return the GameState that results from applying move to this GameState.
        """
        raise NotImplementedError

    def is_valid_move(self, move: Any) -> bool:
        """
        Return whether move is a valid move for this GameState.
        """
        return move in self.get_possible_moves()

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        raise NotImplementedError

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        raise NotImplementedError


def dict_rows(n: int) -> dict:
    """A board generator for the game stonehenge"""
    cells = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z']
    lc = 2
    row = 2
    d = [cells[0:2]]
    while row < n + 1:
        d.append(cells[lc:lc + row + 1])
        lc += row + 1
        row += 1
    d.append(cells[lc:lc + n])
    rows = {}
    for num in range(n):
        rows['row{}'.format(num + 1)] = d[num]
    rows['row{}'.format(n + 1)] = d[-1]
    return rows


def ley_lines_horizontal(n) -> dict:
    """no fking idea"""
    hlm = {}
    rows = dict_rows(n)
    marker = '@'
    for row in rows:
        hlm[row] = marker
    return hlm


def ley_lines_vertical(n) -> dict:
    """lololololol"""
    vlm = {}
    num_vlm = []
    marker = '@'
    for _ in range(n * 2 + 2):
        num_vlm.append(marker)
    vlm['first2'] = num_vlm[0:2]
    vlm['lastn'] = num_vlm[2:n + 2]
    vlm['siden'] = num_vlm[n + 2:]
    return vlm


def board_design(n: int, rows: dict, hlm: dict, vlm: dict) -> str:
    """Makes a board of size n for the game stonehenge"""

    board = ""
    k = n + 4
    indent = " "
    board = indent * (k + 6) + board
    for lm in vlm['first2']:
        board += lm + "   "
    board += '\n'
    board += indent * (k + 5)
    for _ in range(2):
        board += '/' + "   "
    board += '\n'
    board += indent * (k)
    for o in range(n - 1):
        board += hlm['row{}'.format(o + 1)] + " " + "-" + " "
        for i in range(len(rows['row{}'.format(o + 1)]) - 1):
            board += rows['row{}'.format(o + 1)][i] + " " + "-" + " "
        board += rows['row{}'.format(o + 1)][-1] + "   " + vlm['siden'][o]
        board += '\n'
        k -= 1
        board += indent * (k + 4)
        for i in range(len(rows['row{}'.format(o + 1)])):
            board += '/' + " "
            board += '\\' " "
        board += '/'
        board += '\n'
        k -= 2
        board += indent * k
    board += " "
    board += hlm['row{}'.format(n)] + " " + "-" + " "
    for i in range(len(rows['row{}'.format(n)]) - 1):
        board += rows['row{}'.format(n)][i] + " " + "-" + " "
    board += rows['row{}'.format(n)][-1]
    board += '\n'
    k -= 1
    board += indent * (k + 7)

    for i in range(n):
        board += '\\' + " "
        board += '/' + " "
    board += '\\'
    board += '\n'
    k -= 2
    board += indent * (k + 6)
    board += hlm['row{}'.format(n + 1)] + " " + "-" + " "
    for i in range(len(rows['row{}'.format(n + 1)]) - 1):
        board += rows['row{}'.format(n + 1)][i] + " " + "-" + " "
    board += rows['row{}'.format(n + 1)][-1] + "   " + vlm['siden'][-1]
    board += '\n'
    board += indent * (k + 11)
    for i in range(n):
        board += '\\' + "   "
    board += '\n'
    board += indent * (k + 13)
    for k in vlm['lastn']:
        board += k + "   "
    return board


def last_n_lm(n, cells):
    """A helper function"""
    s = {}
    for i in range(n):
        s[i + 1] = []
    for i in range(n):
        s[i + 1] = []
    for lm in s:
        if lm == 1:
            s[lm].append(cells['row{}'.format(n + 1)][0])
            s[lm].append(cells['row{}'.format(n)][0])
        elif lm == 2:
            s[lm].append(cells['row{}'.format(n + 1)][1])
            s[lm].append(cells['row{}'.format(n)][1])
            s[lm].append(cells['row{}'.format(n - 1)][0])
        elif lm == 3:
            s[lm].append(cells['row{}'.format(n + 1)][2])
            s[lm].append(cells['row{}'.format(n)][2])
            s[lm].append(cells['row{}'.format(n - 1)][1])
            s[lm].append(cells['row{}'.format(n - 2)][0])
        elif lm == 4:
            s[lm].append(cells['row{}'.format(n + 1)][3])
            s[lm].append(cells['row{}'.format(n)][3])
            s[lm].append(cells['row{}'.format(n - 1)][2])
            s[lm].append(cells['row{}'.format(n - 2)][1])
            s[lm].append(cells['row{}'.format(n - 3)][0])

        elif lm == 5:
            s[lm].append(cells['row{}'.format(n + 1)][4])
            s[lm].append(cells['row{}'.format(n)][4])
            s[lm].append(cells['row{}'.format(n - 1)][3])
            s[lm].append(cells['row{}'.format(n - 2)][2])
            s[lm].append(cells['row{}'.format(n - 3)][1])
            s[lm].append(cells['row{}'.format(n - 4)][0])

    return s


def side_n_lm(n, cells):
    """A helper function"""
    s = {}
    for i in range(n):
        s[i + 1] = []
    if n == 1:
        s[n].append(cells['row{}'.format(n)][-1])
    elif n == 2:
        s[n - 1].append(cells['row{}'.format(n)][-1])
        s[n - 1].append(cells['row{}'.format(n + 1)][-1])
        s[n].append(cells['row{}'.format(n)][-1])
        s[n].append(cells['row{}'.format(n - 1)][-1])
    elif n == 3:
        s[n - 2].append(cells['row{}'.format(n - 1)][-1])
        s[n - 2].append(cells['row{}'.format(n)][-2])
        s[n - 2].append(cells['row{}'.format(n + 1)][-2])
        s[n - 1].append(cells['row{}'.format(n)][-1])
        s[n - 1].append(cells['row{}'.format(n + 1)][-1])
        s[n].append(cells['row{}'.format(n - 2)][-1])
        s[n].append(cells['row{}'.format(n - 1)][-1])
        s[n].append(cells['row{}'.format(n)][-1])

    elif n == 4:
        s[n - 3].append(cells['row{}'.format(n - 2)][-1])
        s[n - 3].append(cells['row{}'.format(n - 1)][-2])
        s[n - 3].append(cells['row{}'.format(n)][-3])
        s[n - 3].append(cells['row{}'.format(n + 1)][-3])
        s[n - 2].append(cells['row{}'.format(n - 1)][-1])
        s[n - 2].append(cells['row{}'.format(n)][-2])
        s[n - 2].append(cells['row{}'.format(n + 1)][-2])
        s[n - 1].append(cells['row{}'.format(n)][-1])
        s[n - 1].append(cells['row{}'.format(n + 1)][-1])
        s[n].append(cells['row{}'.format(n - 3)][-1])
        s[n].append(cells['row{}'.format(n - 2)][-1])
        s[n].append(cells['row{}'.format(n - 1)][-1])
        s[n].append(cells['row{}'.format(n)][-1])

    elif n == 5:
        s[n - 4].append(cells['row{}'.format(n - 3)][-1])
        s[n - 4].append(cells['row{}'.format(n - 2)][-2])
        s[n - 4].append(cells['row{}'.format(n - 1)][-3])
        s[n - 4].append(cells['row{}'.format(n)][-4])
        s[n - 4].append(cells['row{}'.format(n + 1)][-4])
        s[n - 3].append(cells['row{}'.format(n - 2)][-1])
        s[n - 3].append(cells['row{}'.format(n - 1)][-2])
        s[n - 3].append(cells['row{}'.format(n)][-3])
        s[n - 3].append(cells['row{}'.format(n + 1)][-3])
        s[n - 2].append(cells['row{}'.format(n - 1)][-1])
        s[n - 2].append(cells['row{}'.format(n)][-2])
        s[n - 2].append(cells['row{}'.format(n + 1)][-2])
        s[n - 1].append(cells['row{}'.format(n)][-1])
        s[n - 1].append(cells['row{}'.format(n + 1)][-1])
        s[n].append(cells['row{}'.format(n - 4)][-1])
        s[n].append(cells['row{}'.format(n - 3)][-1])
        s[n].append(cells['row{}'.format(n - 2)][-1])
        s[n].append(cells['row{}'.format(n - 1)][-1])
        s[n].append(cells['row{}'.format(n)][-1])
    return s


class StoneHengeState(GameState):
    """
    The state of a game at a certain point in time.

    WIN - score if player is in a winning position
    LOSE - score if player is in a losing position
    DRAW - score if player is in a tied position
    p1_turn - whether it is p1's turn or not
    """
    WIN: int = 1
    LOSE: int = -1
    DRAW: int = 0
    p1_turn: bool

    def __init__(self, is_p1_turn: bool, board: int, cells: dict, hlm: dict,
                 vlm: dict) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        """
        self.p1_turn = is_p1_turn
        self.board_size = board
        self.cells = cells
        self.hlm = hlm
        self.vlm = vlm

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        board = board_design(self.board_size, self.cells, self.hlm, self.vlm)
        return board

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        over = False
        hori = []
        verti = []
        for row in self.hlm:
            hori.append(self.hlm[row])
        for row in self.vlm:
            verti.extend(self.vlm[row])
        total = hori + verti
        num_1 = total.count('1')
        num_2 = total.count('2')
        if len(total) % 2 == 0:
            need = len(total) / 2
        else:
            need = len(total) // 2 + 1
        if num_1 >= need or num_2 >= need:
            over = True
        if over:
            return []

        possible_moves = []
        for row in self.cells:
            for cell in self.cells[row]:
                if cell.isalpha():
                    possible_moves.append(cell)
        return possible_moves

    def get_current_player_name(self) -> str:
        """
        Return 'p1' if the current player is Player 1, and 'p2' if the current
        player is Player 2.
        """
        if self.p1_turn:
            return 'p1'
        return 'p2'

    def make_move(self, move: Any) -> 'GameState':
        """
        Return the GameState that results from applying move to this GameState.
        """
        # New state should be different from the last so you can't use
        # self dictionaries
        # make a copy dictionary
        cells_new = {}
        for i in self.cells:
            cells_new[i] = []
            for k in self.cells[i]:
                cells_new[i].extend(k)
        hlm_new = self.hlm.copy()
        vlm_new = {}
        for i in self.vlm:
            vlm_new[i] = []
            for k in self.vlm[i]:
                vlm_new[i].extend(k)

        # update cells
        for row in cells_new:
            for cell in cells_new[row]:
                if move == cell:
                    cells_new[row][cells_new[row].index(cell)] = '1' if \
                        self.p1_turn else '2'
        # update horizontal leyline markers
        for row in cells_new:
            num_1 = cells_new[row].count('1')
            num_2 = cells_new[row].count('2')
            if len(cells_new[row]) % 2 == 0:
                need = len(cells_new[row]) / 2
            else:
                need = len(cells_new[row]) // 2 + 1
            if hlm_new[row] == '@' and num_1 > num_2 and num_1 >= need:
                hlm_new[row] = '1'
            elif hlm_new[row] == '@' and num_2 > num_1 and num_2 >= need:
                hlm_new[row] = '2'
        # Update vertical leyline markers
        # the one on A
        checker = []
        for n in range(self.board_size):
            checker.append(cells_new['row{}'.format(n + 1)][0])
        num_1 = checker.count('1')
        num_2 = checker.count('2')
        if len(checker) % 2 == 0:
            need = len(checker) / 2
        else:
            need = len(checker) // 2 + 1
        if vlm_new['first2'][0] == '@' and num_1 > num_2 and num_1 >= need:
            vlm_new['first2'][0] = '1'
        elif vlm_new['first2'][0] == '@' and num_2 > num_1 and num_2 >= need:
            vlm_new['first2'][0] = '2'
        # the one on B
        checker = []
        for n in range(self.board_size):
            checker.append(cells_new['row{}'.format(n + 1)][1])
        checker.append(cells_new['row{}'.format(self.board_size + 1)][0])
        num_1 = checker.count('1')
        num_2 = checker.count('2')
        if len(checker) % 2 == 0:
            need = len(checker) / 2
        else:
            need = len(checker) // 2 + 1
        if vlm_new['first2'][1] == '@' and num_1 > num_2 and num_1 >= need:
            vlm_new['first2'][1] = '1'
        elif vlm_new['first2'][1] == '@' and num_2 > num_1 and num_2 >= need:
            vlm_new['first2'][1] = '2'
        # the last n
        last_n = last_n_lm(self.board_size, cells_new)
        for k in last_n:
            num_1 = last_n[k].count('1')
            num_2 = last_n[k].count('2')
            if len(last_n[k]) % 2 == 0:
                need = len(last_n[k]) / 2
            else:
                need = len(last_n[k]) // 2 + 1
            if vlm_new['lastn'][
                    k - 1] == '@' and num_1 > num_2 and num_1 >= need:
                vlm_new['lastn'][k - 1] = '1'
            elif vlm_new['lastn'][k - 1] == '@' and num_2 > num_1 \
                    and num_2 >= need:
                vlm_new['lastn'][k - 1] = '2'

        # the side n
        side_n = side_n_lm(self.board_size, cells_new)
        for k in side_n:
            num_1 = side_n[k].count('1')
            num_2 = side_n[k].count('2')
            if len(side_n[k]) % 2 == 0:
                need = len(side_n[k]) / 2
            else:
                need = len(side_n[k]) // 2 + 1
            if vlm_new['siden'][
                    k - 1] == '@' and num_1 > num_2 and num_1 >= need:
                vlm_new['siden'][k - 1] = '1'
            elif vlm_new['siden'][k - 1] == '@' and num_2 > num_1 and \
                    num_2 >= need:
                vlm_new['siden'][k - 1] = '2'

        new_state = StoneHengeState(not self.p1_turn, self.board_size,
                                    cells_new, hlm_new, vlm_new)
        return new_state

    def is_valid_move(self, move: Any) -> bool:
        """
        Return whether move is a valid move for this GameState.
        """
        return move in self.get_possible_moves()

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return """It is currently player{0}'s turn. 
        The board looks like:
        {1}""".format(self.get_current_player_name(), self.__str__())

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        initial = self
        moves = self.get_possible_moves()
        if self.get_possible_moves() == []:
            return -1
        for move in moves:
            new_state = self.make_move(move)
            if new_state.get_possible_moves() == []:
                if initial.get_current_player_name() != \
                        new_state.get_current_player_name():
                    return 1
                elif initial.get_current_player_name() == \
                        new_state.get_current_player_name():
                    return -1
                return 0

        for move in moves:
            new_state = self.make_move(move)
            return -1 * new_state.rough_outcome()


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
