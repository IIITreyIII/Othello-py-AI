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