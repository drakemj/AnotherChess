import chess
import chess.pgn


class AnalysisBoard:
    # Sets new board with a empty position and creates new game node for root of game tree
    def __init__(self):
        self.board = chess.Board()
        self.root = chess.pgn.Game()
        self.current_node = self.root
    
    # Makes a move on the board and adds new changes to the current version of the game node
    # If a player makes a illegal move it won't add a new change.
    def make_move(self, move):
        if move in self.board.legal_moves:
            self.board.push(move)
            self.current_node = self.current_node.add_variation(move)
    
    # Undo the previous move on board
    def undo_move(self):
        self.board.pop()
        self.current_node = self.current_node.parent

    # Returns a list of possible moves for current positions on board    
    def get_legal_moves(self):
        return list(self.board.legal_moves)
    
    # Returns current position on board
    def get_current_position(self):
        return self.board
    
    # Returns the game that can be saved to a file in PGN
    def get_pgn(self):
        return self.root
    
    # Sets the position from chess.pgn.game object to the board and game tree
    def set_position_from_pgn(self, pgn):
        self.board = pgn.board()
        self.root = pgn
        self.current_node = self.root
    
    # Resets board to starting positions and makes a new game tree
    def reset_board(self):
        self.board = chess.Board()
        self.root = chess.pgn.Game()
        self.current_node = self.root