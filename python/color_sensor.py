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

# Main loop reading color and printing it every second.
def read_sensor_data(blu,nero,bianco,specchio):
    lux = sensor.lux
    if lux >=(blu-10) and lux <= (blu+10):
        print('blu')
    elif lux >=(nero-10) and lux <= (nero+10):
        print('nero')
    elif lux >=(bianco-10) and lux <= (bianco+10):
        print('bianco')
    elif lux >=(specchio-10) and lux <= (specchio+10):
        print('specchio')

def read_sensor_color_black(nero):
    lux = sensor.lux
    if lux >=(nero-10) and lux <= (nero+10):
        print('nero')
        return True
    else:
        return False