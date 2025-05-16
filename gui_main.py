import json
import time
import threading
from adafruit_servokit import ServoKit
import tkinter as tk
from tkinter import messagebox

# --- Load Servo Configuration ---
with open('./config.json', 'r') as f:
    config = json.load(f)

kit = ServoKit(channels=16)
angles = {int(k): config[k]["initial"] for k in config}

# Apply initial positions and pulse ranges
for ch in angles:
    min_pw = config[str(ch)].get("min_pulse", 600)
    max_pw = config[str(ch)].get("max_pulse", 2400)
    kit.servo[ch].set_pulse_width_range(min_pw, max_pw)
    kit.servo[ch].angle = angles[ch]

# --- GUI Setup ---
root = tk.Tk()
root.title("Robotic Arm Controller")

selected_servo = tk.IntVar(value=list(angles.keys())[0])

# --- Functions ---
def update_servo_display():
    display_label.config(text=f"Servo {selected_servo.get()}  |  Angle: {angles[selected_servo.get()]} °")

def move_servo(delta):
    ch = selected_servo.get()
    min_angle = config[str(ch)]["min"]
    max_angle = config[str(ch)]["max"]
    new_angle = angles[ch] + delta

    if new_angle > max_angle:
        angles[ch] = max_angle
        kit.servo[ch].angle = max_angle
        messagebox.showwarning("Limit Reached", f"Servo {ch} has reached its MAX limit of {max_angle}°")
    elif new_angle < min_angle:
        angles[ch] = min_angle
        kit.servo[ch].angle = min_angle
        messagebox.showwarning("Limit Reached", f"Servo {ch} has reached its MIN limit of {min_angle}°")
    else:
        angles[ch] = new_angle
        kit.servo[ch].angle = new_angle

    update_servo_display()

def on_key(event):
    if event.keysym == "Up":
        move_servo(5)
    elif event.keysym == "Down":
        move_servo(-5)

def save_pose():
    with open("pose.json", "w") as f:
        json.dump(angles, f, indent=4)
    messagebox.showinfo("Pose Saved", "Current servo angles saved to pose.json")

def load_pose():
    try:
        with open("pose.json", "r") as f:
            pose = json.load(f)
            for ch, angle in pose.items():
                ch = int(ch)
                angles[ch] = angle
                kit.servo[ch].angle = angle
            update_servo_display()
    except FileNotFoundError:
        messagebox.showwarning("Pose Not Found", "No saved pose file found.")

def create_servo_buttons():
    for ch in sorted(angles.keys()):
        tk.Radiobutton(root, text=config[str(ch)]["name"], variable=selected_servo, value=ch, command=update_servo_display).pack(anchor=tk.W)

# --- UI Layout ---
display_label = tk.Label(root, text="", font=("Helvetica", 14))
display_label.pack(pady=10)

create_servo_buttons()

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

up_button = tk.Button(control_frame, text="↑ Up", command=lambda: move_servo(5), width=10)
up_button.grid(row=0, column=1)

down_button = tk.Button(control_frame, text="↓ Down", command=lambda: move_servo(-5), width=10)
down_button.grid(row=1, column=1)

save_button = tk.Button(root, text="💾 Save Pose", command=save_pose)
save_button.pack(pady=5)

load_button = tk.Button(root, text="📂 Load Pose", command=load_pose)
load_button.pack(pady=5)

update_servo_display()
root.bind("<Key>", on_key)
root.mainloop()
