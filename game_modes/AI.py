# Trey Ball
# Assignment 3
# 11-11-2024
# The real brains behind the operation! AI.py is responsible for managing the computer player (CPU). 
# It contains the AIMode class, which will calculate the best move for the AI player (and the user if SMART Move) using MiniMax 
# with the option of using alpha-beta pruning. The AIMode class also stores the heuristic values for eachmove. 
# Debug mode allows move-by-move analysis by showing heuristic values on the board grids and moves considered, which shows how the CPU came to that decision. 
# Alpha-beta pruning GREATLY optimizes performance by skipping irrelevant moves. The difference is night and day. 


import math
from board import copy_board
from helpers import count_pieces

class AIMode:
    def __init__(self, depth=3):
        self.depth = depth
        self.states_examined = 0
        self.debug_mode = False
        self.best_move = None
        self.use_alpha_beta = False
        self.heuristic_values = {}

    def set_debug_mode(self, debug, board, color):              # when debug mode turned on, it calculates current best move
        self.debug_mode = debug
        if debug:
            self.calculate_best_move(board, color)

    def set_depth(self, depth, board, color):
        self.depth = depth
        if self.debug_mode:
            self.calculate_best_move(board, color)

    def toggle_alpha_beta(self):
        self.use_alpha_beta = not self.use_alpha_beta

    def calculate_best_move(self, board, color):
        self.states_examined = 0
        self.heuristic_values.clear()

        if self.use_alpha_beta:
            _, self.best_move = self.minimax_alpha_beta(board, self.depth, -math.inf, math.inf, color == 'B')
        else:
            _, self.best_move = self.minimax(board, self.depth, color == 'B')
        
        board.update_heuristics(self.heuristic_values)
        
        print(f"Best move for {color} calculated with depth {self.depth}")
        print(f"Num of states examined: {self.states_examined}")



    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.game_over:
            return self.heuristic(board), None

        self.states_examined += 1
        best_move = None

        if maximizing_player:
            max_eval = -math.inf

            for move in self.get_valid_moves(board, 'B'):
                new_board = self.simulate_move(board, move, 'B')
                eval_score, _ = self.minimax(new_board, depth - 1, False)
                self.heuristic_values[move] = eval_score
                
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
                self.heuristic_values[move] = eval_score
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                if self.debug_mode:
                    print(f"Evaluating move {move}, Heuristic = {eval_score}")
                    
            return min_eval, best_move


    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.game_over:
            return self.heuristic(board), None

        self.states_examined += 1
        best_move = None

        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_valid_moves(board, 'B'):
                new_board = self.simulate_move(board, move, 'B')
                eval_score, _ = self.minimax_alpha_beta(new_board, depth - 1, alpha, beta, False)
                self.heuristic_values[move] = eval_score

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break
                
                if self.debug_mode:
                    print(f"Evaluating move {move}, Heuristic = {eval_score}, Alpha = {alpha}, Beta = {beta}")
                    
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in self.get_valid_moves(board, 'W'):
                new_board = self.simulate_move(board, move, 'W')
                eval_score, _ = self.minimax_alpha_beta(new_board, depth - 1, alpha, beta, True)
                self.heuristic_values[move] = eval_score

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break
                
                if self.debug_mode:
                    print(f"Evaluating move {move}, Heuristic = {eval_score}, Alpha = {alpha}, Beta = {beta}")
                    
            return min_eval, best_move


    def heuristic(self, board):
        black_count, white_count = count_pieces(board.grid)
        return black_count - white_count


    def get_valid_moves(self, board, color):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if board.is_valid_move(row, col, color):
                    valid_moves.append((row, col))
        return valid_moves

    def simulate_move(self, board, move, color):
        new_board = copy_board(board)
        new_board.make_move(move[0], move[1], color)
        return new_board

    def make_best_move(self, board, color):
        if self.best_move:
            board.make_move(self.best_move[0], self.best_move[1], color)
            print(f"Best move for {color}: {self.best_move}")
            self.calculate_best_move(board, 'W' if color == 'B' else 'B')
            return True
        return False
