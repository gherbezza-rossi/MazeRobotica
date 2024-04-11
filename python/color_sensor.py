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

def read_sensor_color_black(nero, times=10):
    black_count = 0
    while True:
        lux = sensor.lux
        print(lux)
        if nero - 2 <= lux <= nero + 2:
            print('nero')
            black_count += 1
            if black_count >= times:
                return True
        else:
            black_count = 0  # Reset the count if color is not black
        if black_count < times:
            return False


while True:
    print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
    print('Temperature: {0}K'.format(sensor.color_temperature))
    print('Lux: {0}'.format(sensor.lux))
    time.sleep(2)