# Trey Ball
# CSC 475 Assignment 3
# 11-11-2024
# Score manager was created to save score states accross new games. It reads and writes scores to a json file.
# This was needed sine the game is stateless and scores would reset after each game.
# Due to the nature of how the game board/main menu are processed (im admitting defeat here), the user must press RESET SCORE to clear the scores if needed.
# Scores also reset if the game is closed.

import json
import os

SCORE_FILE = 'scores.json'

def read_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as file:
            return json.load(file)
    return {'P1': 0, 'P2': 0}

def write_scores(scores):
    with open(SCORE_FILE, 'w') as file:
        json.dump(scores, file)