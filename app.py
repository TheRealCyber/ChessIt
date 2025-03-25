from flask import Flask, request, jsonify, render_template
import chess
import chess.engine
import os

app = Flask(__name__)

# Load Stockfish engine
STOCKFISH_PATH = "C:/Users/AM/Desktop/ChessIt/stockfish/stockfish.exe"

if not os.path.exists(STOCKFISH_PATH):
    print(f"Error: Stockfish executable not found at {STOCKFISH_PATH}")
else:
    print("Stockfish found, proceeding...")

try:
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    print("Stockfish engine loaded successfully.")
except FileNotFoundError:
    print(f"Error: Stockfish not found at {STOCKFISH_PATH}. Update the path.")

board = chess.Board()

@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html exists in templates folder

@app.route("/validate-move")
def validate_move():
    from_square = request.args.get("from")
    to_square = request.args.get("to")

    try:
        move = chess.Move.from_uci(from_square + to_square)
        if move in board.legal_moves:
            board.push(move)  # Apply move if legal
            print(f"Move made: {from_square} -> {to_square}")
            return jsonify({"valid": True, "fen": board.fen()})
    except Exception as e:
        print(f"Invalid move attempt: {from_square} -> {to_square}. Error: {e}")
    
    return jsonify({"valid": False})

@app.route("/get-fen")
def get_fen():
    return jsonify({"fen": board.fen()})

@app.route("/stockfish-move")
def stockfish_move():
    if board.is_game_over():
        print("Game over detected.")
        return jsonify({"fen": board.fen(), "game_over": True})

    result = engine.play(board, chess.engine.Limit(time=0.5))
    board.push(result.move)
    print(f"Stockfish played: {result.move}")

    return jsonify({"fen": board.fen()})

if __name__ == "__main__":
    app.run(debug=True)
