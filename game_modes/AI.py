import math
from board import copy_board
from helpers import count_pieces

class AIMode:
    def __init__(self, depth=3):
        self.depth = depth
        self.states_examined = 0
        self.debug_mode = False
        self.best_move = None  # Stores the best move for the current state
        self.use_alpha_beta = False  # Toggle for alpha-beta pruning
        self.heuristic_values = {}  # Dictionary to store heuristic values per move

    def set_debug_mode(self, debug, board, color):
        """Enable debug mode and calculate the first best move for the current player."""
        self.debug_mode = debug
        if debug:
            self.calculate_best_move(board, color)

    def set_depth(self, depth, board, color):
        """Set the depth and immediately recalculate the best move if in debug mode."""
        self.depth = depth
        if self.debug_mode:
            self.calculate_best_move(board, color)

    def toggle_alpha_beta(self):
        """Toggle alpha-beta pruning on or off."""
        self.use_alpha_beta = not self.use_alpha_beta

    def calculate_best_move(self, board, color):
        """Run MiniMax with or without alpha-beta pruning at the current depth for the current player."""
        self.states_examined = 0
        self.heuristic_values.clear()  # Clear previous heuristic values

        if self.use_alpha_beta:
            _, self.best_move = self.minimax_alpha_beta(board, self.depth, -math.inf, math.inf, color == 'B')
        else:
            _, self.best_move = self.minimax(board, self.depth, color == 'B')
        
        # Pass heuristic values to the board for display
        board.update_heuristics(self.heuristic_values)
        
        print(f"Best move for {color} calculated with depth {self.depth}")
        print(f"States examined: {self.states_examined}")

    def minimax(self, board, depth, maximizing_player):
        """Standard MiniMax without alpha-beta pruning."""
        if depth == 0 or board.game_over:
            return self.heuristic(board), None

        self.states_examined += 1
        best_move = None

        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_valid_moves(board, 'B'):
                new_board = self.simulate_move(board, move, 'B')
                eval_score, _ = self.minimax(new_board, depth - 1, False)
                self.heuristic_values[move] = eval_score  # Store heuristic value for display
                
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
                self.heuristic_values[move] = eval_score  # Store heuristic value for display
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                if self.debug_mode:
                    print(f"Evaluating move {move}, Heuristic = {eval_score}")
                    
            return min_eval, best_move

    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        """MiniMax with alpha-beta pruning."""
        if depth == 0 or board.game_over:
            return self.heuristic(board), None

        self.states_examined += 1
        best_move = None

        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_valid_moves(board, 'B'):
                new_board = self.simulate_move(board, move, 'B')
                eval_score, _ = self.minimax_alpha_beta(new_board, depth - 1, alpha, beta, False)
                self.heuristic_values[move] = eval_score  # Store heuristic value for display

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:  # Pruning occurs here
                    break
                
                if self.debug_mode:
                    print(f"Evaluating move {move}, Heuristic = {eval_score}, Alpha = {alpha}, Beta = {beta}")
                    
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in self.get_valid_moves(board, 'W'):
                new_board = self.simulate_move(board, move, 'W')
                eval_score, _ = self.minimax_alpha_beta(new_board, depth - 1, alpha, beta, True)
                self.heuristic_values[move] = eval_score  # Store heuristic value for display

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                
                if beta <= alpha:  # Pruning occurs here
                    break
                
                if self.debug_mode:
                    print(f"Evaluating move {move}, Heuristic = {eval_score}, Alpha = {alpha}, Beta = {beta}")
                    
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
        """Execute the best move calculated in debug mode, then recalculate for the next player."""
        if self.best_move:
            board.make_move(self.best_move[0], self.best_move[1], color)
            print(f"Executing best move for {color}: {self.best_move}")
            # Recalculate the best move for the next player
            self.calculate_best_move(board, 'W' if color == 'B' else 'B')
            return True
        return False
