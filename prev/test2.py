import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Create I2C bus interface
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize PCA9685 with address 0x40 (default)
pca = PCA9685(i2c)
pca.frequency = 100  # Typical servo frequency (50Hz)

# Servo pulse-width calibration (adjusted for each servo type)
MG996R_pulse = (500, 2500)    # in microseconds (standard servo)     #500,2500
HS70MG_pulse = (500, 2500)    # typically standard range as well
MG90S_pulse = (600, 2400)     # micro servo usually slightly narrower

# Initialize servos on specified channels
servo_MG996R_10 = servo.Servo(pca.channels[10], min_pulse=MG996R_pulse[0], max_pulse=MG996R_pulse[1])
servo_MG996R_11 = servo.Servo(pca.channels[11], min_pulse=MG996R_pulse[0], max_pulse=MG996R_pulse[1])
servo_MG996R_12 = servo.Servo(pca.channels[12], min_pulse=MG996R_pulse[0], max_pulse=MG996R_pulse[1])

servo_HS70MG_13 = servo.Servo(pca.channels[13], min_pulse=HS70MG_pulse[0], max_pulse=HS70MG_pulse[1])
servo_HS70MG_14 = servo.Servo(pca.channels[14], min_pulse=HS70MG_pulse[0], max_pulse=HS70MG_pulse[1])

servo_MG90S_15 = servo.Servo(pca.channels[15], min_pulse=MG90S_pulse[0], max_pulse=MG90S_pulse[1])

# Example Servo Test Function
def test_servos():
    try:
        while True:
            
        #    print("Moving MG996R servos...")
        # servo_MG996R_10.angle =90
        # servo_MG996R_11.angle = 90
        # servo_MG996R_12.angle = 90

        #print("Moving HS-70MG servos...")
        #servo_HS70MG_14.angle = 180
        # servo_HS70MG_14.angle = 90

        # print("Moving MG90S servo...")
        # servo_MG90S_15.angle = 90

        # time.sleep(2)

        # print("Moving to extreme positions...")

        # # MG996R Servos
        # servo_MG996R_10.angle = 0
        # servo_MG996R_11.angle = 180
        # servo_MG996R_12.angle = 0

        # # HS-70MG Servos
        # servo_HS70MG_13.angle = 180
        # servo_HS70MG_14.angle = 0

        # # MG90S Servo
            print("Moving MG996R servos...")
            servo_MG90S_15.angle = 50

        time.sleep(2)
        

    except KeyboardInterrupt:
        print("Test interrupted by user.")

    finally:
        # Disable servo signals to avoid overheating
        servo_MG996R_10.angle = None
        servo_MG996R_11.angle = None
        servo_MG996R_12.angle = None
        servo_HS70MG_13.angle = None
        servo_HS70MG_14.angle = None
        servo_MG90S_15.angle = None

        pca.deinit()
        print("All servos disabled.")

# Run servo test
if __name__ == "__main__":
    test_servos()
