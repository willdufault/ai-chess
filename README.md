# AI Chess

A highly efficient Python chess engine.

https://github.com/user-attachments/assets/6d9ccc37-927b-4db1-b783-b1291b0c7879

### Overview

AI Chess is a 1400-rated (98th percentile) Python chess engine delivering fast, intelligent gameplay. It leverages bitboards for efficient board representation, Zobrist hashing for rapid state lookup, and a custom engine to evaluate positions. The AI uses minimax with alpha-beta pruning and a transposition table to cache board evaluations, producing strong, optimized moves while providing a challenging experience and showcasing advanced AI and performance techniques.

### Features

- Full chess game implementation using bitboards
- Zobrist hashing for efficient board state management
- Custom engine for evaluating positions
- Evaluation bar to display the current advantage
- AI using Minimax with alpha-beta pruning and transposition table caching
- Lazy move generation for efficient game tree exploration
- Unit tests with pytest to validate critical components

> Experimented with Python 3.14 free threading for AI evaluation, but running on a single thread proved faster due to thread overhead

### Technologies

- Python 3.14
- pytest
- cProfile

### Usage

- Enter moves in coordinate format `"rcrc"` (row/column &rarr; row/column, 0-based)
- Use `"!"` to skip legality checks (e.g., `"0077!"`)

### Installation

```bash
git clone https://github.com/willdufault/ai-chess.git
cd ai-chess
python main.py
```
