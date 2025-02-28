from src.chess_bot.chess_board import ChessBoard
from src.chess_bot.bot import ChessBot
import time

board = ChessBoard()
bot = ChessBot()

# Test Python minimax
start_time = time.time()
# Original minimax call
python_eval, python_move = bot.minimax(board.get_board_state(), 6, -float('inf'), float('inf'), board.get_board_state().turn)
python_time = time.time() - start_time


print(f"Python: {python_time:.4f}s")