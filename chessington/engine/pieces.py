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

    def many_steps(self, move, current_square):
        moves=[]
        if move == 'one_step':
            for i in range(1,7):
                one_step = Square.at(current_square.row + (self.direction() * i), current_square.col)
                if board.square_is_empty(one_step) and board.in_board(one_step):
                    moves.append(one_step)
                elif board.has_enemy(one_step):
                    moves.append(one_step)
                else:
                    break
        elif move == 'left_step':
            for i in range(1,7):
                left_step = Square.at(current_square.row, current_square.col - i)
                if board.square_is_empty(left_step) and board.in_board(left_step):
                    moves.append(left_step)
                elif board.has_enemy(left_step):
                    moves.append(left_step)
                else:
                    break
        elif move == 'right_step':
            for i in range(1,7):
                right_step = Square.at(current_square.row, current_square.col + i)
                if board.square_is_empty(right_step) and board.in_board(right_step):
                    moves.append(right_step)
                elif board.has_enemy(right_step):
                    moves.append(right_step)
                else:
                    break
        elif move == 'left_diagonal':
            for i in range(1,7):
                left_diagonal = Square.at(current_square.row + (self.direction() * i), current_square.col - i)
                if board.square_is_empty(left_diagonal) and board.in_board(left_diagonal):
                    moves.append(left_diagonal)
                elif board.has_enemy(left_diagonal):
                    moves.append(left_diagonal)
                else:
                    break
        elif move == 'right_diagonal':
            for i in range(1,7):
                right_diagonal = Square.at(current_square.row + (self.direction() * i), current_square.col + i)
                if board.square_is_empty(right_diagonal) and board.in_board(right_diagonal):
                    moves.append(right_diagonal)
                elif board.has_enemy(right_diagonal):
                    moves.append(right_diagonal)
                else:
                    break
        return moves

class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):
        moves = []
        current_square = self.position(board)
        start_row = {Player.WHITE: 1, Player.BLACK: 6}[self.player]
        one_step = Square.at(current_square.row + self.direction(), current_square.col)
        if board.in_board(one_step) and board.square_is_empty(one_step):
            moves.append(one_step)
            if current_square.row == start_row:
                double_step = Square.at(current_square.row + (2 * self.direction()), current_square.col)
                if board.square_is_empty(double_step):
                    moves.append(double_step)
        moves += self.attackable_squares(board)
        return moves

    def attackable_squares(self, board):
        current_square = self.position(board)
        left_diagonal = Square.at(current_square.row + self.direction(), current_square.col - 1)
        right_diagonal = Square.at(current_square.row + self.direction(), current_square.col + 1)

        attack_moves = []
        if board.has_enemy(left_diagonal):
            attack_moves.append(left_diagonal)
        if board.has_enemy(right_diagonal):
            attack_moves.append(right_diagonal)
        return attack_moves

class Knight(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []



class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        current_square = self.position(board)
        moves = self.many_steps('one_step', current_square) + self.many_steps('left_step', current_square) +
        self.many_steps('right_step', current_square) + self.many_steps('left_diagonal', current_square) +
        self.many_steps('right_diagonal', current_square)
        return moves



class King(Piece):
    """
    A class representing a chess king.
    """
    def get_available_moves(self, board):
        moves = []
        current_square = self.position(board)
        one_step = Square.at(current_square.row + self.direction(), current_square.col)
        left_diagonal = Square.at(current_square.row + self.direction(), current_square.col - 1)
        right_diagonal = Square.at(current_square.row + self.direction(), current_square.col + 1)
        if board.in_board(one_step) and not board.has_friend(one_step):
            moves.append(one_step)
        if board.in_board(left_diagonal) and not board.has_friend(left_diagonal):
            moves.append(left_diagonal)
        if board.in_board(right_diagonal) and not board.has_friend(right_diagonal):
            moves.append(right_diagonal)
        return moves