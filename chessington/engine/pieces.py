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

    def many_steps(self, board, move, current_square):
        moves=[]
        step = {'one_step': [1,0], 'left_step':[0,-1], 'right_step':[0,1], 'left_diagonal':[1,-1], 'right_diagonal':[1,1]}
        xy=step[move]
        for i in range(0,7):
            next_square = Square.at(current_square.row + (self.direction() * i * xy[0]), current_square.col + (self_direction() * i * xy[1]))
            if board.in_board(next_square):
                if board.square_is_empty(next_square):
                    moves.append(next_square)
                elif board.has_enemy(next_square):
                    moves.append(next_square)
                    break
                elif board.has_friend(next_square):
                    break
        if move == 'one_step':
            for i in range(1,7):
                one_step = Square.at(current_square.row + (self.direction() * i), current_square.col)
                if board.in_board(one_step):
                    if board.square_is_empty(one_step):
                        moves.append(one_step)
                    elif board.has_enemy(one_step):
                        moves.append(one_step)
                        break
                    elif board.has_friend(one_step):
                        break
                else:
                    break
        elif move == 'left_step':
            for i in range(1,7):
                left_step = Square.at(current_square.row, current_square.col - i)
                if board.in_board(left_step):
                    if board.square_is_empty(left_step):
                        moves.append(left_step)
                    elif board.has_enemy(left_step):
                        moves.append(left_step)
                        break
                    elif board.has_friend(left_step):
                        break
                else:
                    break
        elif move == 'right_step':
            for i in range(1,7):
                right_step = Square.at(current_square.row, current_square.col + i)
                if board.in_board(right_step):
                    if board.square_is_empty(right_step):
                        moves.append(right_step)
                    elif board.has_enemy(right_step):
                        moves.append(right_step)
                        break
                    elif board.has_friend(right_step):
                        break
                else:
                    break
        elif move == 'left_diagonal':
            for i in range(1,7):
                left_diagonal = Square.at(current_square.row + (self.direction() * i), current_square.col - i)
                if board.in_board(left_diagonal):
                    if board.square_is_empty(left_diagonal):
                        moves.append(left_diagonal)
                    elif board.has_enemy(left_diagonal):
                        moves.append(left_diagonal)
                        break
                    elif board.has_friend(left_diagonal):
                        break
                else:
                    break
        elif move == 'right_diagonal':
            for i in range(1,7):
                right_diagonal = Square.at(current_square.row + (self.direction() * i), current_square.col + i)
                if board.in_board(right_diagonal):
                    if board.square_is_empty(right_diagonal):
                        moves.append(right_diagonal)
                    elif board.has_enemy(right_diagonal):
                        moves.append(right_diagonal)
                        break
                    elif board.has_friend(right_diagonal):
                        break
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
        current_square = self.position(board)
        moves = self.many_steps(board, )
        return moves


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        current_square = self.position(board)
        moves = self.many_steps(board, 'one_step', current_square) + self.many_steps(board, 'left_step', current_square) + self.many_steps(board, 'right_step', current_square) + self.many_steps(board, 'left_diagonal', current_square) + self.many_steps(board, 'right_diagonal', current_square)
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