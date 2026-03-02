# Connect 4 — Minimax AI Agent

A command-line Connect 4 engine where a human player competes against an AI opponent powered by the **Minimax adversarial search algorithm**. The AI exhaustively evaluates the game tree to select optimal moves, demonstrating core concepts in game theory, combinatorial search, and decision-making under perfect information.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
  - [Game Representation](#game-representation)
  - [Minimax Algorithm](#minimax-algorithm)
  - [Win Detection](#win-detection)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Future Improvements](#future-improvements)

---

## Overview

Connect 4 is a two-player, zero-sum, perfect-information game played on a **7×6** grid. Players alternate dropping pieces into columns; the first to align four pieces horizontally, vertically, or diagonally wins. This project implements:

- A full game loop with input validation and board rendering via NumPy arrays.
- An AI agent that uses **depth-limited Minimax** to search the game tree and select the highest-value move.
- Deterministic tie-breaking via random selection among equally scored moves.

---

## How It Works

### Game Representation

The board is stored as a `numpy.ndarray` of shape `(7, 6)` with three cell states:

| Value | Meaning       |
|-------|---------------|
| `1`   | Human piece   |
| `-1`  | AI piece      |
| `0`   | Empty cell    |

Gravity is simulated by scanning each column bottom-up and placing a piece in the lowest available row.

### Minimax Algorithm

The AI uses [Minimax](https://en.wikipedia.org/wiki/Minimax), a classical adversarial search algorithm for two-player zero-sum games.

```
minimax(state, player, depth) =
    ┌ utility(state)                          if terminal state or depth ≥ max_depth
    │ min over children  minimax(child, −player, depth+1)   if player = Human  (minimizing)
    └ max over children  minimax(child, −player, depth+1)   if player = AI     (maximizing)
```

**Key implementation details** (in `ai.py`):

- **Maximizing player**: AI (`-1`) — selects the child state with the highest minimax value.
- **Minimizing player**: Human (`1`) — selects the child state with the lowest minimax value.
- **Depth limit**: Configurable via `max_depth` (default `3`), bounding the search to keep move computation tractable. At depth 3 the AI evaluates up to $O(b^3)$ nodes where $b \leq 7$ is the branching factor.
- **Terminal evaluation**: `+1` for an AI win, `-1` for a human win, `0` for a draw or depth cutoff.
- **Move selection**: `get_best_move()` iterates over all legal moves, scores each via minimax, and returns a random choice among moves tied for the best score — introducing non-determinism at equal valuations.

### Win Detection

`check_winner()` scans the board for four consecutive same-player pieces across all four axes:

1. **Horizontal** — sliding window across each row.
2. **Vertical** — sliding window down each column.
3. **Diagonal (↘)** — top-left to bottom-right diagonals.
4. **Diagonal (↙)** — top-right to bottom-left diagonals.

Returns `1` (human wins), `-1` (AI wins), `0` (draw — board full, no winner), or `None` (game ongoing).

---

## Project Structure

```
connect-4-ai/
├── connect4.py        # Game loop, board I/O, win checking, human vs AI driver
├── ai.py              # Minimax search, move generation, board evaluation
├── requirements.txt   # Python dependencies (numpy, pygame)
├── .gitignore
└── README.md
```

| File | Responsibility |
|------|---------------|
| `connect4.py` | Initializes the 7×6 board, handles player input with column validation, alternates turns between human and AI, prints the board state each turn, and declares the winner. |
| `ai.py` | Implements `get_available_moves()` (gravity-aware legal move enumeration), `get_children()` (successor state generation), `minimax()` (depth-limited adversarial search), `check_winner()` (terminal state detection), and `get_best_move()` (top-level move selection). |

---

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

```bash
git clone https://github.com/<your-username>/connect-4-ai.git
cd connect-4-ai
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python connect4.py
```

---

## Usage

```
[[ 0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.]]
enter column number from 1-6 : 3
Ai has made the move:
```

You enter a column number each turn. The AI responds immediately with its computed optimal move.

---

## Technical Details

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Board dimensions | 7 rows × 6 columns |
| Max branching factor ($b$) | 6 (one per non-full column) |
| Search depth ($d$) | 3 (default) |
| Worst-case nodes evaluated | $O(b^d) = O(6^3) = 216$ |
| State representation | `numpy.ndarray` — $O(1)$ element access |

The depth-limited search ensures sub-second response times while still providing competitive play. Increasing `max_depth` yields stronger play at the cost of exponential time growth.

### Algorithm Properties

- **Optimality**: Minimax is optimal against a perfectly rational opponent in zero-sum games.
- **Completeness**: The depth limit makes the search incomplete — deeper game-ending sequences beyond the horizon may be missed.
- **Space complexity**: $O(b \cdot d)$ — linear in the depth of the search tree (DFS traversal).

---

## Future Improvements

- **Alpha-Beta Pruning** — Prune branches that cannot influence the final decision, reducing effective branching factor from $b$ to $O(\sqrt{b})$ in the best case.
- **Iterative Deepening** — Search at increasing depths within a time budget, combining the optimality of BFS with the space efficiency of DFS.
- **Heuristic Evaluation Function** — Replace the flat `0` at depth cutoff with a position-scoring heuristic (e.g., count of open 3-in-a-rows, center control) to improve play quality without increasing depth.
- **Transposition Table** — Cache evaluated board positions using Zobrist hashing to avoid redundant subtree evaluations.
- **Bitboard Representation** — Encode the board as two 64-bit integers for $O(1)$ win detection and faster move generation.
- **GUI** — Leverage the existing `pygame` dependency to build an interactive graphical interface.

---

## License

This project is open source and available under the [MIT License](LICENSE).
