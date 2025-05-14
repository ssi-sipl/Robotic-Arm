import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Create I2C bus
i2c = busio.I2C(SCL, SDA)

# Create PCA9685 instance
pca = PCA9685(i2c)
pca.frequency = 100  # Typical servo frequency

# Create a servo object on channel 0
my_servo = servo.Servo(pca.channels[10])

# Move servo
print("Moving servo...")
my_servo.angle = 0
print("servo at 0 deg")
time.sleep(1)
my_servo.angle = 90
print("servo at 90 deg")
time.sleep(1)
my_servo.angle = 180
print("servo at 180 deg")
time.sleep(1)

# def set_servo_angle(channel, angle):
    # pulse_min = 100  # ~500µs
    # pulse_max = 500  # ~2500µs
    # pulse = int(pulse_min + (angle / 180.0) * (pulse_max - pulse_min))
    # pca.channels[10].duty_cycle = int(pulse / 4096 * 65535)

# # Example use
# for angle in [0, 40, 80]:
    # print(f"Moving to {angle}°")
    # set_servo_angle(0, angle)
    # time.sleep(1)

# Cleanup

