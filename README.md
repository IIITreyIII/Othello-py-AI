# Welcome to the Othello-py-AI Wiki!

This project was created by Trey Ball for the CSC-475 Artificial Intelligence class at Louisiana Tech University.

## Project Overview

Othello-py-AI is a Python-based Othello game featuring both a Player vs. Player mode and a Player vs. CPU mode. The CPU uses an AI built with the MiniMax algorithm and optional alpha-beta pruning to provide a challenging opponent. Players can also enable Debug mode, which shows the AI's decision process.

### Table of Contents

1. **[Main.py - Game Menu](main.py)**  
   The main entry point for the game, offering options for two-player mode or playing against the CPU.

2. **[Board.py - Game Board Management](board.py)**  
   Manages the game board, drawing pieces, and handling all move logic, including validation and winner detection.

3. **[Sidebar.py - Sidebar Interface and Debug Options](sidebar.py)**  
   The right-side sidebar containing buttons for game controls, score tracking, and Debug options like "Smart Move" and alpha-beta pruning.

4. **[AI.py - CPU Player Logic](AI.py)**  
   The AI brain of the project. It uses MiniMax with optional alpha-beta pruning to decide the best moves, with Debug mode available to visualize move evaluations.

5. **[PvCPU.py - Player vs CPU Mode](PvCPU.py)**  
   Runs the game mode where players can compete against the AI. CPU difficulty can be set in the Debug menu, and alpha-beta pruning is recommended for performance.

6. **[twoPlayer.py - Two Player Mode](twoPlayer.py)**  
   Allows two players to compete, taking turns. Debug mode is available to assist players by showing recommended moves.

7. **[settings.py - Game Configuration](settings.py)**  
   Stores global constants like colors, dimensions, and fonts for the game.

8. **[helpers.py - Utility Functions](helpers.py)**  
   Contains helper functions, like `count_pieces`, which calculates the number of pieces for each player.

9. **[score_manager.py - Score Persistence](score_manager.py)**  
   Manages reading and writing player scores to `scores.json` to keep track of wins across sessions.

---
