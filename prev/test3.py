import time
from adafruit_servokit import ServoKit

# Setup PCA9685 servo controller for 16 channels
kit = ServoKit(channels=16)

# Configure servos pulse width ranges:
for ch in [10, 11, 12]:  # MG996R standard servo
    kit.servo[ch].set_pulse_width_range(500, 2500)

for ch in [13, 14]:  # HS-70MG digital servo
    kit.servo[ch].set_pulse_width_range(500, 2500)

# MG90S micro servo
kit.servo[15].set_pulse_width_range(600, 2400)

# Function to test servo movement
def test_servos():
    try:
        print("Moving servos to neutral (90°)")
        for ch in [10, 11, 12, 13, 14, 15]:
            kit.servo[ch].angle = 90
        time.sleep(2)

        print("Sweeping servos to extremes...")
        positions = [0, 180]

        # MG996R (channels 10-12)
        for angle in positions:
            for ch in [10, 11, 12]:
                kit.servo[ch].angle = angle
            time.sleep(1)

        # HS-70MG (channels 13-14)
        for angle in positions[::-1]:  # reversed sweep
            for ch in [13, 14]:
                kit.servo[ch].angle = angle
            time.sleep(1)

        # MG90S (channel 15)
        for angle in positions:
            kit.servo[15].angle = angle
            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        # Disable servo signals to avoid overheating
        for ch in [10, 11, 12, 13, 14, 15]:
            kit.servo[ch].angle = None
        print("Servos disabled. Done.")

# Execute test
if __name__ == "__main__":
    test_servos()
