from abc import abstractmethod, ABCMeta


class BoardItemInput:
    def __init__(self, item_id="UnknownBoardItem"):
        self.item_id = item_id


class BoardItem:
    def __init__(self, board_item_input):
        self.board_item_input = board_item_input


class BoardInput:
    def __init__(self, n_rows, n_cols):
        if n_rows <= 0:
            raise ValueError("Number of board rows must be positive")
        self.n_rows = n_rows

        if n_cols <= 0:
            raise ValueError("Number of board rows must be positive")
        self.n_cols = n_cols


class Board(metaclass=ABCMeta):
    def __init__(self, board_input):
        self.board_input = board_input

        self._table = []
        self._make_board()

    @abstractmethod
    def _make_board(self):
        raise NotImplementedError()

    @property
    def n_rows(self):
        return self.board_input.n_rows

    @property
    def n_cols(self):
        return self.board_input.n_cols

    @property
    def shape(self):
        return self.n_rows, self.n_cols

    def __getitem__(self, coord):
        assert len(coord) in [1, 2]

        if len(coord) == 1:
            return self._table[coord[0]]

        return self._table[coord[0] + self.n_rows * coord[1]]

    def __setitem__(self, coord, board_item):
        assert len(coord) in [1, 2]

        if len(coord) == 1:
            self._table[coord[0]] = board_item
        else:
            self._table[coord[0] + self.n_rows * coord[1]] = board_item
