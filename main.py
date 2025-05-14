from adafruit_servokit import ServoKit
import time

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)

def set_servo_angle(index, angle):
    """
    Maps your logical servo index (1 to 6) to PCA9685 channels (10 to 15)
    and moves the servo to the given angle.
    """
    # Validate input
    if index < 1 or index > 6 or angle < 0 or angle > 180:
        print("Invalid servo index or angle")
        return

    # Map servo index 1-6 to PCA9685 channels 10-15
    channel = 9 + index  # so index 1 maps to channel 10, 2 → 11 ... 6 → 15

    # Handle mirrored movement for servo index 5 (like in your Arduino code)
    angle = set_max_limits(index,angle)
    if index == 5:
        kit.servo[channel].angle = angle
        # kit.servo[15].angle = 180 - angle  # index 6 → channel 15
    else:
        kit.servo[channel].angle = angle

    print(f"Moved servo {index} (channel {channel}) to {angle}°")

def set_max_limits(index, angle):
    if index==6:
        if angle>=90:
            exit()

    return angle

safe_angles = {
    # 10: 45,  # Base (example)
    # 11: 60,  # Shoulder
    # 12: 60,  # Elbow
    # 14: 30,  # Wrist Pitch
    # 13: 30,  # Wrist Roll
    15: 30    # Gripper
}

# # Set custom ranges if needed
# for ch in safe_angles:
#     kit.servo[ch].set_pulse_width_range(600, 2100)

# # Gradually move each servo
# for ch, angle in safe_angles.items():
#     print(f"Initializing servo {ch} to {angle}°")
#     kit.servo[ch].angle = angle
    
#     time.sleep(0.3)  # Small delay between each servo

# Motor - 5
# print("Initial 160")
# kit.servo[14].angle = 160

# time.sleep(2)

# for i in range(50,160,10):
#     print("Moving Up at ",i) 
#     kit.servo[14].angle = i
#     time.sleep(1)

# for i in range(160,40,-10):
#     print("Moving Down at ",i)
#     kit.servo[14].angle = i
#     time.sleep(1)

print("Servo 5 at 160")
kit.servo[14].angle = 80

time.sleep(2)

print("Servo 4 at 0")
kit.servo[13].angle = 0

time.sleep(2)

# kit.servo[12].angle = 0
# print("Servo 3 at 0")
# time.sleep(2)
# kit.servo[12].angle = 45
# print("Servo 3 at 45")
# time.sleep(2)
# kit.servo[12].angle = 90
# print("Servo 3 at 90")

for i in range(0,170,10):
    print("Moving Up at ",i) 
    kit.servo[12].angle = i
    time.sleep(1)

for i in range(160,0,-10):
    print("Moving Down at ",i)
    kit.servo[12].angle = i
    time.sleep(1)



# Example usage
# set_servo_angle(1, 90)
# set_servo_angle(5, 0)  # Will move servo 5 and mirror 6

# Optional: keep the program running
while True:
    # Add your control logic here or interface with input   
    # set_servo_angle
    # set_servo_angle(6,0)
    # time.sleep(1)
    # set_servo_angle(6,10)
    # time.sleep(1)
    # set_servo_angle(6,20)
    # time.sleep(1)
    # set_servo_angle(6,30)
    # time.sleep(1)
    # set_servo_angle(6,40)

    # set_servo_angle(5, 40)

    # kit.servo[15].angle = 30
    pass