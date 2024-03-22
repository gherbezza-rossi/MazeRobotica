import time
import busio
import board
import adafruit_bno055

# Define the offsets
offsets_magnetometer = (489, 370, 1373)
offsets_gyroscope = (-1, 0, 3)
offsets_accelerometer = (-44, 6, -47)

i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the BNO055 sensor with the specified I2C bus
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Calibrate the sensor with the offsets
sensor.offsets_accelerometer = offsets_accelerometer
sensor.offsets_gyroscope = offsets_gyroscope
sensor.offsets_magnetometer = offsets_magnetometer

def giro():
    data = sensor.euler
    data = str(data)
    values_str = data[1:-1].split(',')
    first_value = float(values_str[0])
    time.sleep(0.2)
    return first_value


