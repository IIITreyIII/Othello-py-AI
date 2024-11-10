# ai_mode.py

import math
from board import copy_board
from helpers import count_pieces

class AIMode:
    def __init__(self, depth=3):
        self.depth = depth
        self.states_examined = 0
        self.debug_mode = False

    def set_debug_mode(self, debug):
        self.debug_mode = debug

    def minimax(self, board, depth, maximizing_player):
        """Recursive minimax with depth limit and heuristic scoring."""
        if depth == 0 or board.game_over:
            return self.heuristic(board), None

        self.states_examined += 1
        best_move = None

        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_valid_moves(board, 'B'):
                new_board = self.simulate_move(board, move, 'B')
                eval_score, _ = self.minimax(new_board, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                if self.debug_mode:
                    print(f"Evaluating move {move}, Heuristic = {eval_score}")
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in self.get_valid_moves(board, 'W'):
                new_board = self.simulate_move(board, move, 'W')
                eval_score, _ = self.minimax(new_board, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                if self.debug_mode:
                    print(f"Evaluating move {move}, Heuristic = {eval_score}")
            return min_eval, best_move

    def heuristic(self, board):
        """Heuristic: returns the difference in piece count as score."""
        black_count, white_count = count_pieces(board.grid)
        return black_count - white_count

    def get_valid_moves(self, board, color):
        """Get all valid moves for the current color."""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if board.is_valid_move(row, col, color):
                    valid_moves.append((row, col))
        return valid_moves

    def simulate_move(self, board, move, color):
        """Simulate a move by copying the board and making the move."""
        new_board = copy_board(board)
        new_board.make_move(move[0], move[1], color)
        return new_board

    def make_best_move(self, board, color):
        """Calculate and make the best move for the given color using Minimax."""
        self.states_examined = 0
        _, best_move = self.minimax(board, self.depth, True if color == 'B' else False)
        print(f"States examined: {self.states_examined}")
        return best_move
