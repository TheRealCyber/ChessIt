import chess
import chess.engine

STOCKFISH_PATH = "stockfish/stockfish.exe"  # Update path if needed

def make_move(board, move):
    if move:
        try:
            board.push_san(move)
            print(f"Move made: {move}")
        except ValueError:
            print(f"Invalid move: {move}")
            return False
    else:
        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            result = engine.play(board, chess.engine.Limit(time=0.5))
            board.push(result.move)
            print(f"Stockfish move: {result.move}")
            return board.san(result.move)
    return True

def get_board_state(board):
    return board.fen()
