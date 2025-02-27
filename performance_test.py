import time
import chess
from bot import ChessBot
import chess_engine_cpp

# Create a test position
board = chess.Board()
bot = ChessBot()

# Test Python minimax
start_time = time.time()
# Original minimax call
python_eval, python_move = bot.minimax(board, 6, -float('inf'), float('inf'), board.turn)
python_time = time.time() - start_time

# Test C++ minimax
start_time = time.time()
cpp_eval, cpp_move = chess_engine_cpp.find_best_move(board, 6)
cpp_time = time.time() - start_time

print(f"Python: {python_time:.4f}s, C++: {cpp_time:.4f}s, Speedup: {python_time/cpp_time:.2f}x")