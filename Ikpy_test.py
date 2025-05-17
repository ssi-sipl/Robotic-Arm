from ikpy.chain import Chain
from ikpy.link import URDFLink
import numpy as np
import matplotlib.pyplot as plt
import json

from adafruit_servokit import ServoKit
import time

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)

with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

def initial_positions():
    for key, value in config.items():
        kit.servo[int(key)].angle = value.get('initial')
 
def starting_animation():
    kit.servo[15].angle = 90
    time.sleep(0.5)
    kit.servo[15].angle = 180
    time.sleep(0.5)
    kit.servo[15].angle = 90
    time.sleep(0.5)

initial_positions()
starting_animation()


# Define the robot arm using URDFLink with correct argument names
my_chain = Chain(name='vinith_robot_arm', links=[
    URDFLink(
        name="base",
        origin_translation=[0, 0, 0.065],  # 6.5 cm base height
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1],  # Rotates around Z-axis
        joint_type="revolute"
    ),
    URDFLink(
        name="shoulder",
        origin_translation=[0, 0, 0],
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0],  # Rotates around Y-axis
        joint_type="revolute"
    ),
    URDFLink(
        name="elbow",
        origin_translation=[0, 0, 0.12],  # 12 cm link
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0],  # Rotates around Y-axis
        joint_type="revolute"
    ),
    URDFLink(
        name="wrist_pitch",
        origin_translation=[0, 0, 0.11],  # 11 cm link
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0],  # Rotates around Y-axis
        joint_type="revolute"
    ),
    URDFLink(
        name="wrist_roll",
        origin_translation=[0, 0, 0.05],  # 5 cm link
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1],  # Rotates around Z-axis
        joint_type="revolute"
    )
])

# Define the target position [x, y, z] in meters
target_position = [0.1, 0.05, 0.1]

# Create a transformation matrix for the target position
target_frame = np.eye(4)
target_frame[:3, 3] = target_position

# Solve inverse kinematics
# ik_solution = my_chain.inverse_kinematics(target_frame)
ik_solution = my_chain.inverse_kinematics(target_position)
ik_solution_degrees = np.degrees(ik_solution)


# Print the result
print("Joint angles in radians:", ik_solution)
print("Joint angles in degress:", ik_solution_degrees)

def ik_to_servo_angle(ik_angle_deg, servo_min, servo_max, servo_initial):
    # Offset IK angles by adding the initial angle (neutral)
    servo_angle = ik_angle_deg + servo_initial
    
    # Clamp to servo min and max
    if servo_angle < servo_min:
        servo_angle = servo_min
    elif servo_angle > servo_max:
        servo_angle = servo_max
    return servo_angle



count=0
for key, value in config.items():
    if key == '15':
        continue
    max= value.get('max')
    min= value.get('min')   
    initial= value.get('initial')
    angle=ik_solution_degrees[::-1][count]
    ik_angle=ik_to_servo_angle(angle, min, max, initial)
    kit.servo[int(key)].angle = ik_angle
    print(value.get('name'))
    print(f"Servo {key} angle: {ik_angle}°")

    count+=1


