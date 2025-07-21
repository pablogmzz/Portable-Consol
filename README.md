# ESP32 Mini Console with MicroPython Games 🎮

---

## 🔧 Hardware Features

* **ESP32** microcontroller (any MicroPython-compatible module)
* **OLED display** via I2C (SSD1306 128×64)
* **Physical buttons** for directional input (Up, Down, Left, Right)
* **Select/Action button** for game actions (e.g., jump, shoot)
* (Optional) Buzzer, LEDs, or other peripherals for extra effects

---

## 🎮 Games Included

* **Simon Says**: Memory sequence game. Remember and repeat the button pattern.
* **Snake**: Classic snake game. Guide the snake to eat food without running into walls or itself.
* **Pong**: Two-player or player-vs-AI paddle game. Bounce the ball past your opponent’s paddle.
* **Breakout**: Paddle-and-brick game. Destroy all bricks by bouncing the ball off your paddle.
* **Flappy Bird**: Tap to make the bird flap and navigate through hollow pipes.

---

## ⚙️ Installation & Usage

1. **Flash MicroPython** onto your ESP32 module.
2. **Upload files** (`main.py`, `games/`, `lib/`) via Thonny, ampy, rshell, etc.
3. **Reset or power** the board to start the console.
4. Use the **directional buttons** to navigate the menu and the **select/action button** to choose games.

---

## ⚙️ Code Structure

* `main.py` — Bootloader & menu system.
* `games/` — Individual game modules (`simon.py`, `snake.py`, `pong.py`, `breakout.py`, `flappy.py`).
* `lib/` — Shared utilities (display wrapper, input handler).

---

## 🔄 Extending the Console

* Add new `.py` files under `games/` following the existing module template.
* Register your game in `main.py` by adding an entry in the menu mapping:

  ```python
  GAMES = {
      'simon': jugar_simon,
      'snake': jugar_snake,
      'pong': jugar_pong,
      'breakout': jugar_breakout,
      'flappy bird': jugar_flappy,
      # 'newgame': jugar_newgame,
  }
  ```
* Implement the game loop using the provided display and input helpers.

---

## 📝 License

MIT License. Feel free to fork and customize!

