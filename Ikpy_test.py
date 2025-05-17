from ikpy.chain import Chain
from ikpy.link import URDFLink
import numpy as np
import matplotlib.pyplot as plt
import json

from adafruit_servokit import ServoKit
import time

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)


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

def ik_to_servo_angle(ik_angle_deg, servo_min, servo_max, servo_initial):
    # Offset IK angles by adding the initial angle (neutral)
    servo_angle = ik_angle_deg + servo_initial
    
    # Clamp to servo min and max
    if servo_angle < servo_min:
        servo_angle = servo_min
    elif servo_angle > servo_max:
        servo_angle = servo_max
    return servo_angle

def angle_to_servo_motion(x,y,z):
    target_position = [x, y, z]

    # Solve inverse kinematics
    ik_solution = my_chain.inverse_kinematics(target_position)
    ik_solution_degrees = np.degrees(ik_solution)

    print("Joint angles in radians:", ik_solution)
    print("Joint angles in degress:", ik_solution_degrees)

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
        print(f"Servo {value.get('name')}({key}) angle: {ik_angle}°")

        count+=1

print("Starting initial positions and animation...")
initial_positions()
starting_animation()

print("Add Coordinates to move the arm to the desired position:")
x = float(input("X: "))
y = float(input("Y: "))
z = float(input("Z: "))

angle_to_servo_motion(x,y,z)