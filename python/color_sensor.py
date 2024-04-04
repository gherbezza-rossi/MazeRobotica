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

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

# Main loop reading color and printing it every second.
def read_color():
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)
    sensor.integration_time = 200
    sensor.gain = 60
    color_rgb=sensor.color_rgb_bytes
    print(color_rgb)

    if color_rgb[0]==2:
        print("bianco")
    elif color_rgb[1]>12 and color_rgb[1]<20:
        print("blu")
    elif color_rgb[1]>8 and color_rgb[1]<11:
        print("nero")
    elif color_rgb[2]>200:
        print("specchio")

while True:
    read_color()