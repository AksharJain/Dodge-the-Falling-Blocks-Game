# Dodge the Falling Blocks

## Description
A fast-paced, arcade-style survival game built purely in Python and Pygame. Dodge incoming neon geometric blocks, survive as long as possible, and watch out as the speed and difficulty gradually increase!

This project was built as a clean, structured Python mini-project, focusing on state machines, basic 2D graphics rendering, precise collision detection, and user interface overlays.

## Features
- **Fluid Gameplay:** Smooth continuous player movement and boundary collision.
- **Dynamic Difficulty:** Randomized enemy block sizes and speeds that increase automatically as you level up.
- **State Management:** Complete navigation system featuring Start Menu, Settings, Pause Menu, and Game Over screens.
- **Scoring System:** Session-based high score tracking.
- **Audio Support:** Toggleable sound and music engine (gracefully runs even without sound assets).
- **Visual Polish:** Neon glow effects, a scrolling starfield background, and explosive particle feedback upon collision.

## Requirements
- Python 3.x
- Pygame 2.x

## Installation
1. Ensure Python is installed on your system.
2. Install the required dependency using pip:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run
Navigate to the project directory and run the main game script:
```bash
python main.py
```

## Controls
- **Move Left / Right:** A / D or Left / Right Arrow Keys
- **Start Game:** ENTER
- **Pause / Resume:** P
- **Settings:** S (from Start Screen)
- **Restart Game:** R (from Game Over Screen)
- **Main Menu:** M
- **Quit Game:** ESC (Global)

## Adding Custom Audio (Optional)
The game is completely playable silently, but you can drop your own audio files into the `assets/sounds/` folder to enable them automatically!
- `assets/sounds/bgm.mp3` (Background Music)
- `assets/sounds/score.wav` (Point scored)
- `assets/sounds/level.wav` (Level up)
- `assets/sounds/hit.wav` (Collision / Game Over)
- `assets/sounds/menu.wav` (Menu selection)
