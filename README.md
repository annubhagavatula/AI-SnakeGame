# 🐍 Two-Player Snake Game (with AI & Obstacles)

A **Pygame-based two-player Snake game** where one player is human-controlled and the other is AI-driven with simple pathfinding.  
Includes obstacles, separate food for each snake, collision detection, and a timer-based win system.

---

## 🎮 Gameplay

- **Player 1 (Green Snake)** — Controlled by arrow keys.
- **Player 2 (Blue Snake)** — AI-controlled, moves toward its own food while avoiding obstacles and the other snake.
- **Food**:  
  - Red — for Green Snake  
  - Pink — for Blue Snake  
- **Obstacles**: White squares randomly placed on the grid.
- **Timer**: 5 minutes; highest score wins if time runs out.

---

## 🛠 Features
- Grid-based movement.
- Random obstacle generation.
- Safe food placement avoiding obstacles and snake bodies.
- AI pathfinding for Blue Snake (shortest safe move with randomness).
- Collision detection:
  - Walls
  - Self
  - Other snake
  - Obstacles
- Snake growth on food consumption.

---

## ⌨️ Controls
**Green Snake (Player 1):**
- ⬆️ `Arrow Up` — Move Up
- ⬇️ `Arrow Down` — Move Down
- ⬅️ `Arrow Left` — Move Left
- ➡️ `Arrow Right` — Move Right

**Blue Snake (Player 2):**  
- Moves automatically via AI logic.

---

## 🏆 Win Conditions
- A player collides with wall, self, other snake, or obstacle → Other player wins instantly.
- Timer reaches 0:
  - Higher score wins.
  - Equal score → Tie.

---

## 📦 Requirements
- Python 3.x
- Pygame

Install Pygame:
```bash
pip install pygame

To run the game:
python two_player_snake.py


If you want, I can also add **a nice ASCII art snake** at the top of the README so it feels more fun and retro-gaming themed. That would make your repo stand out.
