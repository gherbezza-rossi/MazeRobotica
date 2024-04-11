# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time
import board
import adafruit_tcs34725


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor.integration_time = 500
sensor.gain = 60
# Main loop reading color and printing it every second.
def read_sensor_data(blu,bianco):
    lux = sensor.color_rgb_bytes[0]
    if lux >=(blu-5) and lux <= (blu+5):
        print('blu')
        return 'blu'
    elif lux >=(bianco-5) and lux <= (bianco+5):
        print('bianco')
        return 'bianco'

def read_sensor_color_black(nero):
    while True:
        lux = sensor.color_rgb_bytes[0]
        if nero - 5 <= lux <= nero + 5:
            print('nero')
            return True
        else:
            return False


while True:
    print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
    time.sleep(0.5)