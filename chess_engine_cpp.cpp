// chess_engine_cpp.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <limits>
#include <algorithm>
#include <utility>
#include <unordered_map>

namespace py = pybind11;

// Piece values matching your Python code
const std::unordered_map<int, int> PIECE_VALUES = {
    {1, 100},  // PAWN
    {2, 300},  // KNIGHT
    {3, 300},  // BISHOP
    {4, 500},  // ROOK
    {5, 900},  // QUEEN
    {6, 20000} // KING
};

// Score a move (capture/promotion estimation)
int score_move(const py::object& board, const py::object& move) {
    int score = 0;

    // Check if capture
    if (board.attr("is_capture")(move).cast<bool>()) {
        auto to_square = move.attr("to_square").cast<int>();
        auto captured_piece_type = board.attr("piece_type_at")(to_square);

        if (!captured_piece_type.is_none()) {
            score += PIECE_VALUES.at(captured_piece_type.cast<int>());
        }

        auto from_square = move.attr("from_square").cast<int>();
        auto moving_piece = board.attr("piece_type_at")(from_square);

        if (!moving_piece.is_none()) {
            score -= PIECE_VALUES.at(moving_piece.cast<int>()) / 10;
        }
    }

    // Check for promotion
    auto promotion = move.attr("promotion");
    if (!promotion.is_none()) {
        int promotion_type = promotion.cast<int>();
        // Queen promotion (5 is QUEEN in python-chess)
        if (promotion_type == 5) {
            score += 800;
        } else {
            score += 200;
        }
    }

    return score;
}

// Position evaluation function
int evaluate_position(const py::object& board, int depth_searched) {
    // Check if game is over
    if (board.attr("is_game_over")().cast<bool>()) {
        if (board.attr("is_checkmate")().cast<bool>()) {
            bool turn = board.attr("turn").cast<bool>();
            return turn ? (-10000 + depth_searched) : (10000 - depth_searched);
        }
        return 0; // Draw
    }

    int score = 0;

    // Count material for each side
    for (const auto& pair : PIECE_VALUES) {
        int piece_type = pair.first;
        int value = pair.second;

        auto white_pieces = board.attr("pieces")(piece_type, true);
        auto black_pieces = board.attr("pieces")(piece_type, false);

        // Fix for len() - properly cast the Python objects to get their length
        int white_count = py::len(white_pieces);
        int black_count = py::len(black_pieces);

        score += white_count * value;
        score -= black_count * value;
    }

    return score;
}

// Minimax with alpha-beta pruning
std::pair<int, py::object> minimax(
    py::object board,
    int depth,
    int alpha,
    int beta,
    bool maximizing_player,
    int ply = 0
) {
    // Base case: leaf node or terminal position
    if (depth == 0 || board.attr("is_game_over")().cast<bool>()) {
        return {evaluate_position(board, ply), py::none()};
    }

    py::object best_move = py::none();

    // Get all legal moves
    py::list moves = board.attr("legal_moves");

    // Convert to vector for sorting
    std::vector<py::object> moves_vec;
    for (const py::handle& move : moves) {
        moves_vec.push_back(py::cast<py::object>(move));
    }

    // Sort moves by estimated value (captures/promotions first)
    std::sort(moves_vec.begin(), moves_vec.end(), [&board](const py::object& a, const py::object& b) {
        return score_move(board, a) > score_move(board, b);
    });

    if (maximizing_player) {
        int best_eval = std::numeric_limits<int>::min();
        for (const auto& move : moves_vec) {
            board.attr("push")(move);
            auto result = minimax(board, depth - 1, alpha, beta, false, ply + 1);
            int score = result.first;
            board.attr("pop")();

            if (score > best_eval) {
                best_eval = score;
                best_move = move;
            }

            alpha = std::max(alpha, best_eval);
            if (alpha >= beta) {
                break; // Beta cutoff
            }
        }
        return {best_eval, best_move};
    }
    else {
        int best_eval = std::numeric_limits<int>::max();
        for (const auto& move : moves_vec) {
            board.attr("push")(move);
            auto result = minimax(board, depth - 1, alpha, beta, true, ply + 1);
            int score = result.first;
            board.attr("pop")();

            if (score < best_eval) {
                best_eval = score;
                best_move = move;
            }

            beta = std::min(beta, best_eval);
            if (beta <= alpha) {
                break; // Alpha cutoff
            }
        }
        return {best_eval, best_move};
    }
}

// Main interface function
py::object find_best_move(py::object board, int depth) {
    auto result = minimax(
        board,
        depth,
        std::numeric_limits<int>::min(),
        std::numeric_limits<int>::max(),
        board.attr("turn").cast<bool>()
    );

    int eval_score = result.first;
    py::object best_move = result.second;

    return py::make_tuple(eval_score, best_move);
}

PYBIND11_MODULE(chess_engine_cpp, m) {
    m.doc() = "C++ extension for chess engine minimax algorithm";
    m.def("find_best_move", &find_best_move,
          "Find the best move using minimax with alpha-beta pruning",
          py::arg("board"), py::arg("depth") = 4);
}