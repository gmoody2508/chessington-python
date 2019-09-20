"""
Definitions of each of the different chess pieces.
"""

from abc import ABC, abstractmethod

from chessington.engine.data import Player, Square


class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player
        self.has_moved = False

    @abstractmethod
    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)

    def position(self, board):
        return board.find_piece(self)

    def direction(self):
        return {Player.WHITE: 1, Player.BLACK: -1}[self.player]

    def steps(self, board, move, limit):
        if limit:
            move_limit = 1
        elif not limit:
            move_limit = 7
        current_square = self.position(board)
        moves = []
        step = {'forward_step': [1, 0], 'backward_step': [-1, 0], 'left_step': [0, -1], 'right_step': [0, 1], \
                'forward_left_diagonal': [1, -1], 'forward_right_diagonal': [1, 1], 'backward_left_diagonal': [-1, -1], \
                'backward_right_diagonal': [-1, 1]}
        xy = step[move]
        for i in range(1, move_limit + 1):
            next_square = Square.at(current_square.row + (self.direction() * i * xy[0]),
                                    current_square.col + (self.direction() * i * xy[1]))
            if board.in_board(next_square):
                if board.square_is_empty(next_square):
                    moves.append(next_square)
                elif board.has_enemy(next_square):
                    moves.append(next_square)
                    break
                elif board.has_friend(next_square):
                    break
        return moves


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):
        moves = []
        forward_step = self.steps(board, 'forward_step', limit=True)[0]
        if not board.has_enemy(forward_step):
            moves.append(forward_step)
        current_square = self.position(board)
        start_row = {Player.WHITE: 1, Player.BLACK: 6}[self.player]
        if current_square.row == start_row:
            double_step = Square.at(current_square.row + (2 * self.direction()), current_square.col)
            if board.square_is_empty(double_step):
                moves.append(double_step)
        moves += self.attackable_squares(board, current_square)
        return moves

    def attackable_squares(self, board, current_square):
        left_diagonal = Square.at(current_square.row + self.direction(), current_square.col - 1)
        left_en_passant = Square.at(current_square.row, current_square.col - 1)
        right_diagonal = Square.at(current_square.row + self.direction(), current_square.col + 1)
        right_en_passant = Square.at(current_square.row, current_square.col + 1)
        attack_moves = []
        if board.has_enemy(left_diagonal) or board.en_passant == left_en_passant:
            attack_moves.append(left_diagonal)
        if board.has_enemy(right_diagonal) or board.en_passant == right_en_passant:
            attack_moves.append(right_diagonal)
        return attack_moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        current_square = self.position(board)
        moves = [
            Square.at(current_square.row + 2, current_square.col - 1),
            Square.at(current_square.row + 2, current_square.col + 1),
            Square.at(current_square.row - 2, current_square.col - 1),
            Square.at(current_square.row - 2, current_square.col + 1),
            Square.at(current_square.row + 1, current_square.col - 2),
            Square.at(current_square.row - 1, current_square.col - 2),
            Square.at(current_square.row + 1, current_square.col + 2),
            Square.at(current_square.row - 1, current_square.col + 2)
        ]
        valid_moves = []
        for move in moves:
            if board.in_board(move):
                valid_moves.append(move)
        return valid_moves


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        moves = self.steps(board, 'forward_left_diagonal', limit=False) + self.steps(board, 'forward_right_diagonal',
                                                                                     limit=False) \
                + self.steps(board, 'backward_left_diagonal', limit=False) + self.steps(board,
                                                                                        'backward_right_diagonal',
                                                                                        limit=False)
        return moves


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        moves = self.steps(board, 'forward_step', limit=False) + self.steps(board, 'backward_step', limit=False) \
                + self.steps(board, 'left_step', limit=False) + self.steps(board, 'right_step', limit=False)
        return moves

    def castling(self, board, castling):
        current_square = self.position(board)
        if castling == 'left':
            if self.has_moved == False:
                board.move_piece(current_square, Square.at(current_square.row, current_square.col + 2))
        elif castling == 'right':
            if self.has_moved == False:
                board.move_piece(current_square, Square.at(current_square.row, current_square.col - 2))


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        moves = self.steps(board, 'forward_step', limit=False) + self.steps(board, 'backward_step', limit=False) \
                + self.steps(board, 'left_step', limit=False) + self.steps(board, 'right_step', limit=False) \
                + self.steps(board, 'forward_left_diagonal', limit=False) + self.steps(board, 'forward_right_diagonal',
                                                                                       limit=False) \
                + self.steps(board, 'backward_left_diagonal', limit=False) + self.steps(board,
                                                                                        'backward_right_diagonal',
                                                                                        limit=False)
        return moves


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        moves = self.steps(board, 'forward_step', limit=True) + self.steps(board, 'backward_step', limit=True) \
                + self.steps(board, 'left_step', limit=True) + self.steps(board, 'right_step', limit=True) \
                + self.steps(board, 'forward_left_diagonal', limit=True) + self.steps(board, 'forward_right_diagonal',
                                                                                      limit=True) \
                + self.steps(board, 'backward_left_diagonal', limit=True) + self.steps(board, 'backward_right_diagonal',
                                                                                       limit=True)
        if self.has_moved == False:
            current_square = self.position(board)
            left_squares = [Square.at(current_square.row, current_square.col - 3),
                            Square.at(current_square.row, current_square.col - 2), \
                            Square.at(current_square.row, current_square.col - 1),
                            Square.at(current_square.row, current_square.col + 1), \
                            Square.at(current_square.row, current_square.col + 2)]
            right_squares = [Square.at(current_square.row, current_square.col + 1),
                             Square.at(current_square.row, current_square.col + 2)]
            empty = True
            for square in left_squares:
                if not board.square_is_empty(square):
                    empty = False
            if empty:
                moves.append(Square.at(current_square.row, current_square.col - 2))
            empty = True
            for square in right_squares:
                if not board.square_is_empty(square):
                    empty = False
            if empty:
                moves.append(Square.at(current_square.row, current_square.col + 2))

        return moves
