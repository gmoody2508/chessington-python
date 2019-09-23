"""
A module providing a representation of a chess board. The rules of chess are not implemented - 
this is just a "dumb" board that will let you move pieces around as you like.
"""

from collections import namedtuple
from enum import Enum, auto

from chessington.engine.data import Player, Square
from chessington.engine.pieces import Pawn, Knight, Bishop, Rook, Queen, King
import sys

BOARD_SIZE = 8

class Board:
    """
    A representation of the chess board, and the pieces on it.
    """

    def __init__(self, player, board_state):
        self.current_player = Player.WHITE
        self.board = board_state
        self.en_passant = None

    @staticmethod
    def empty():
        return Board(Player.WHITE, Board._create_empty_board())

    @staticmethod
    def at_starting_position():
        return Board(Player.WHITE, Board._create_starting_board())

    @staticmethod
    def _create_empty_board():
        return [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    @staticmethod
    def _create_starting_board():

        # Create an empty board
        board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # Setup the rows of pawns
        board[1] = [Pawn(Player.WHITE) for _ in range(BOARD_SIZE)]
        board[6] = [Pawn(Player.BLACK) for _ in range(BOARD_SIZE)]

        # Setup the rows of pieces
        piece_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        board[0] = list(map(lambda piece: piece(Player.WHITE), piece_row))
        board[7] = list(map(lambda piece: piece(Player.BLACK), piece_row))

        return board

    def in_board(self, square):
        return 0 <= square.row <= 7 and 0 <= square.col <= 7


    def set_piece(self, square, piece):
        """
        Places the piece at the given position on the board.
        """
        self.board[square.row][square.col] = piece

    def get_piece(self, square):
        """
        Retrieves the piece from the given square of the board.
        """
        return self.board[square.row][square.col]

    def square_is_empty(self, square):
        #Checks a square is empty
        return self.get_piece(square) is None

    def has_enemy(self, square):
        if self.in_board(square):
            if not self.square_is_empty(square):
                if not self.get_piece(square).player == self.current_player:
                    return True
        return False

    def has_friend(self, square):
        if self.in_board(square):
            if not self.square_is_empty(square):
                if self.get_piece(square).player == self.current_player:
                    return True
        return False

    def find_piece(self, piece_to_find):
        """
        Searches for the given piece on the board and returns its square.
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is piece_to_find:
                    return Square.at(row, col)
        raise Exception('The supplied piece is not on the board')


    def move_piece(self, from_square, to_square):
        """
        Moves the piece from the given starting square to the given destination square.
        """
        moving_piece = self.get_piece(from_square)
        if moving_piece is not None and moving_piece.player == self.current_player:
            self.checkmate(to_square)
            moving_piece.has_moved = True
            self.set_piece(to_square, moving_piece)
            self.set_piece(from_square, None)
            self.handle_castling(moving_piece, from_square, to_square)
            self.handle_en_passant_capture(moving_piece, to_square)
            #Location of square a pawn has double stepped to, i.e en passant may be possible
            self.en_passant = self.record_double_move(moving_piece, from_square, to_square)
            self.handle_promotion(moving_piece, to_square)
            self.current_player = self.current_player.opponent()
    #Identifies if a pawn has double stepped. If so, it returns the location of the square it has moved to
    def record_double_move(self, moving_piece, from_square, to_square):
        if isinstance(moving_piece,Pawn):
            if abs(from_square.row - to_square.row) > 1:
                return to_square
        return None

    #Checks moving piece is a pawn gets the previous 'en passant' double step made by another pawn
    def handle_en_passant_capture(self, moving_piece, to_square):
        if self.en_passant is None:
            return
        if not isinstance(moving_piece, Pawn):
            return
        if to_square.col == self.en_passant.col:
            if to_square.row == 2 or to_square.row == 5:
                self.set_piece(self.en_passant, None)


    def handle_castling(self, moving_piece, from_square, to_square):
        if isinstance(moving_piece, King):
            if abs(from_square.col - to_square.col) > 1:
                if to_square.row == 0:
                    if to_square.col == 2:
                        self.set_piece(Square.at(0,0), None)
                        self.set_piece(Square.at(0,3), Rook(self.current_player))
                    elif to_square.col == 6:
                        self.set_piece(Square.at(0, 7), None)
                        self.set_piece(Square.at(0, 5), Rook(self.current_player))
                elif to_square.row == 7:
                    if to_square.col == 2:
                        self.set_piece(Square.at(7, 0), None)
                        self.set_piece(Square.at(7, 3), Rook(self.current_player))
                    elif to_square.col == 6:
                        self.set_piece(Square.at(7, 7), None)
                        self.set_piece(Square.at(7, 5), Rook(self.current_player))
        return

    def handle_promotion(self, moving_piece, to_square):
        if isinstance(moving_piece, Pawn):
            if to_square.row == 0 or to_square.row == 7:
                piece = input("Select piece to promote pawn to: 'Q', 'K', 'R' or 'B'.")
                if piece == 'Q':
                    self.set_piece(to_square, Queen(self.current_player))
                elif piece == 'K':
                    self.set_piece(to_square, Knight(self.current_player))
                elif piece == 'R':
                    self.set_piece(to_square, Rook(self.current_player))
                elif piece == 'B':
                    self.set_piece(to_square, Bishop(self.current_player))
                else:
                    self.set_piece(to_square, Queen(self.current_player))
        return

    def checkmate(self, to_square):
        if isinstance(self.get_piece(to_square), King):
            if self.get_piece(to_square).player == self.current_player.opponent():
                player = str(self.current_player)
                player = player[7:]
                print("Checkmate - Player " + player + " wins!")
                sys.exit()

