from adafruit_servokit import ServoKit
import time
import json

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)

with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

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
    # angle = set_max_limits(index,angle)
    if index == 5:
        kit.servo[channel].angle = angle
        # kit.servo[15].angle = 180 - angle  # index 6 → channel 15
    else:
        kit.servo[channel].angle = angle

    print(f"Moved servo {index} (channel {channel}) to {angle}°")

def initial_positions():
    for key, value in config.items():
        kit.servo[int(key)].angle = value.get('initial')

initial_positions()

# kit.servo[15].angle = 90
# time.sleep(0.5)
# kit.servo[15].angle = 180
# time.sleep(0.5)
# kit.servo[15].angle = 90
# time.sleep(0.5)

# kit.continuous_servo[11].throttle = 1
# time.sleep(2)
# kit.continuous_servo[11].throttle = 0
# time.sleep(2)
# kit.continuous_servo[11].throttle = 1
# time.sleep(2)


# kit.servo[11].angle = 90
# print("Servo 11 set to 90 degrees")
# time.sleep(2)
# kit.servo[11].angle = 180
# print("Servo 11 set to 180 degrees")
# time.sleep(2)
# kit.servo[11].angle = 0
# print("Servo 11 set to 90 degrees")
# time.sleep(2)

# kit.continuous_servo[10].set_pulse_width_range(min_pulse=1000, max_pulse=2000)

# print("Spinning forward")
# kit.continuous_servo[11].throttle = 1
# time.sleep(2)

# print("Spinning backward")
# kit.continuous_servo[11].throttle = -1
# time.sleep(2)

# print("Stopping")
# kit.continuous_servo[11].throttle = 0
# time.sleep(2)

# kit.continuous_servo[11].set_pulse_width_range(min_pulse=990, max_pulse=2010)

# # Set throttle to 0 to stop the motor at startup
# kit.continuous_servo[11].throttle = 0.0

# kit.continuous_servo[10].set_pulse_width_range(min_pulse=990, max_pulse=2010)
