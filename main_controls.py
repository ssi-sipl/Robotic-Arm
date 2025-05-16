import json
import time
import sys
import tty
import termios
from adafruit_servokit import ServoKit

# Load servo configuration
with open('./config.json', 'r') as f:
    config = json.load(f)

kit = ServoKit(channels=16)
angles = {int(k): config[k]["initial"] for k in config}

# Apply initial positions
for ch in angles:
    kit.servo[ch].angle = angles[ch]

# --- Terminal key input setup ---
def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(3)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

# --- CLI Interface ---
print("Available servos:")
for ch in sorted(config.keys(), key=int):
    print(f"{ch}: {config[ch]['name']}")

selected = input("Select servo channel number to control: ")

try:
    selected_ch = int(selected)
    if str(selected_ch) not in config:
        print("Invalid selection. Exiting.")
        sys.exit(1)
except ValueError:
    print("Invalid input. Exiting.")
    sys.exit(1)

min_angle = config[str(selected_ch)]["min"]
max_angle = config[str(selected_ch)]["max"]
step = 1

print(f"Controlling Servo {selected_ch} ({config[str(selected_ch)]['name']})")
print("Use UP and DOWN arrows to move. Press 'q' to quit.")

while True:
    key = get_key()
    if key == '\x1b[A':  # UP arrow
        if angles[selected_ch] + step <= max_angle:
            angles[selected_ch] += step
            kit.servo[selected_ch].angle = angles[selected_ch]
            print(f"↑ Moved to {angles[selected_ch]}°")
        else:
            print(f"Max angle {max_angle}° reached.")

    elif key == '\x1b[B':  # DOWN arrow
        if angles[selected_ch] - step >= min_angle:
            angles[selected_ch] -= step
            kit.servo[selected_ch].angle = angles[selected_ch]
            print(f"↓ Moved to {angles[selected_ch]}°")
        else:
            print(f"Min angle {min_angle}° reached.")

    elif key == 'q':
        print("Exiting...")
        break