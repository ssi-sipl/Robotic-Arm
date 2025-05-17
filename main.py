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
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch1 + ch2 + ch3  # e.g., '\x1b[A'
        else:
            return ch1  # e.g., 'q' or 'b'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def print_angle_bar(channel):
    angle = angles[channel]
    bar_length = 30
    min_angle = config[str(channel)]["min"]
    max_angle = config[str(channel)]["max"]
    scale = (angle - min_angle) / (max_angle - min_angle)
    pos = int(scale * bar_length)
    bar = "[" + "=" * pos + "|" + "-" * (bar_length - pos) + "]"
    print(f"{bar} {angle}°")

# --- CLI Interface ---
while True:
    print("\nAvailable servos:")
    for ch in sorted(config.keys(), key=int):
        print(f"{ch}: {config[ch]['name']}")

    selected = input("\nSelect servo channel number to control (or 'q' to quit): ")

    if selected == 'q':
        print("Exiting...")
        break

    try:
        selected_ch = int(selected)
        if str(selected_ch) not in config:
            print("Invalid selection. Try again.")
            continue
    except ValueError:
        print("Invalid input. Try again.")
        continue

    min_angle = config[str(selected_ch)]["min"]
    max_angle = config[str(selected_ch)]["max"]
    step = 1

    print(f"\nControlling Servo {selected_ch} ({config[str(selected_ch)]['name']})")
    print("Use UP and DOWN arrows to move. Press 'b' to go back. Press 'q' to quit.")

    while True:
        print_angle_bar(selected_ch)
        key = get_key()
        if key == '\x1b[A':  # UP arrow
            if angles[selected_ch] + step <= max_angle:
                angles[selected_ch] += step
                kit.servo[selected_ch].angle = angles[selected_ch]
                continue
            else:
                print(f"Max angle {max_angle}° reached.")
                continue

        elif key == '\x1b[B':  # DOWN arrow
            if angles[selected_ch] - step >= min_angle:
                angles[selected_ch] -= step
                kit.servo[selected_ch].angle = angles[selected_ch]
                continue

            else:
                print(f"Min angle {min_angle}° reached.")
                continue

        elif key == 'b':
            break

        elif key == 'q':
            print("Exiting...")
            sys.exit(0)

        time.sleep(0.1)
