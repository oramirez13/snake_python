# Snake Game

Classic snake game built with pygame. Cross-platform, no external assets required.

## Requirements

- Python 3.7+
- pygame

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd snake_python

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python snake.py
```

## Controls

| Key | Action |
|-----|--------|
| Arrow keys / WASD | Move snake |
| ESC | Quit game |
| SPACE / ENTER | Restart after game over |

## Features

- Score tracking with high score persistence
- Game over screen with restart option
- Grid background for visual reference
- Smooth movement with directional lock (no 180-degree turns)
- Cross-platform (Linux, Windows, macOS)

## Project Structure

```
snake_python/
├── snake.py           # Main game
├── requirements.txt   # Dependencies
├── .gitignore         # Excludes cache and venv
└── README.md          # This file
```

## How It Works

1. Snake moves on a grid, collecting red food items
2. Each food collected adds 10 points and grows the snake
3. Game ends if the snake hits a wall or its own body
4. High score is tracked during the session
