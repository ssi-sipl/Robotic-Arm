from adafruit_servokit import ServoKit
import time
import json

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

# initial_positions()
# starting_animation()

for i in range(0, 180, 10):
    kit.servo[11].angle = i
    print(f"Servo 11 angle: {i}")
    time.sleep(1)




