# ESP32 Mini Console with MicroPython Games 🎮
---

## 🔧 Hardware Features

- **ESP32** microcontroller (any MicroPython-compatible module)
- **OLED display** via I2C (e.g., SSD1306 128x64)
- **Physical buttons** for directional input (up, down, left, right)
- (Optional) **Extra button** for exiting or pausing
- (Optional) Buzzer, LEDs, or other peripherals for extra effects

---

## 🚀 What does it do?

The console is designed to be modular and extensible. Currently, it includes:

- A basic **Simon Says** memory game with physical input
- A classic **Snake** game adapted to the screen resolution
- Responsive button input using edge detection
- Visual feedback on the OLED screen
- A structure ready to support more games and a menu system

---

## ⚙️ How to Use

1. Flash MicroPython onto your ESP32.
2. Use [Thonny](https://thonny.org/), [ampy](https://github.com/scientifichackers/ampy), or [rshell] to copy the files.
3. Upload `main.py` to the root of the ESP32 file system.
4. Reset or power the board to start the console.
