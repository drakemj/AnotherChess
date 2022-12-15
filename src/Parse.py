import chess
import chess.pgn

game = chess.pgn.Game()
print(game.end().board())
game.add_main_variation(chess.Move(8, 16, 3))
print(game.end().board())