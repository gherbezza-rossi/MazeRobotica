import time
import board
from digitalio import DigitalInOut
from adafruit_vl53l0x import VL53L0X

# declare the singleton variable for the default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# declare the digital output pins connected to the "SHDN" pin on each VL53L0X sensor
xshut = [
    DigitalInOut(board.D26),
    DigitalInOut(board.D19),
    DigitalInOut(board.D16),
    DigitalInOut(board.D20),
    # add more VL53L0X sensors by defining their SHDN pins here
]

for power_pin in xshut:
    # make sure these pins are a digital output, not a digital input
    power_pin.switch_to_output(value=False)
    time.sleep(0.1)
    # These pins are active when Low, meaning:
    #   if the output signal is LOW, then the VL53L0X sensor is off.
    #   if the output signal is HIGH, then the VL53L0X sensor is on.
# all VL53L0X sensors are now off

# initialize a list to be used for the array of VL53L0X sensors
vl53 = []

# now change the addresses of the VL53L0X sensors


for i, power_pin in enumerate(xshut):
power_pin.value = True
time.sleep(0.1)  # Aggiungi un ritardo prima di inizializzare il sensore
vl53.insert(i, VL53L0X(i2c))
if i < len(xshut):
    vl53[i].set_address(i + 0x30)  # Indirizzo del sensore
    time.sleep(0.1)  # Aggiungi un breve ritardo dopo aver cambiato l'indirizzo

def detect_range():
        # Read three measurements
        ranges_1 = [sensor.range for sensor in vl53]
        time.sleep(0.1)  # Add a small delay between measurements
        ranges_2 = [sensor.range for sensor in vl53]
        time.sleep(0.1)
        ranges_3 = [sensor.range for sensor in vl53]

        processed_ranges = []

        for index in range(len(vl53)):
            # Check if the three measurements are consistent
            if 50 <= ranges_1[index] <= 5000 and \
               50 <= ranges_2[index] <= 5000 and \
               50 <= ranges_3[index] <= 5000 and \
               abs(ranges_1[index] - ranges_2[index]) < 100 and \
               abs(ranges_1[index] - ranges_3[index]) < 100 and \
               abs(ranges_2[index] - ranges_3[index]) < 100:
                processed_ranges.append("{}".format(ranges_1[index]))
            else:
                processed_ranges.append("0")

        sensor_ranges_str = " ".join(processed_ranges)
        return sensor_ranges_str

def detect_walls():
        # Read three measurements
        ranges_1 = [sensor.range for sensor in vl53]
        time.sleep(0.1)  # Add a small delay between measurements
        ranges_2 = [sensor.range for sensor in vl53]
        time.sleep(0.1)
        ranges_3 = [sensor.range for sensor in vl53]

        processed_ranges = []

        for index in range(len(vl53)):
            # Check if the three measurements are consistent and within range
            if 20 <= ranges_1[index] <= 5000 and \
            20 <= ranges_2[index] <= 5000 and \
            20 <= ranges_3[index] <= 5000 and \
            abs(ranges_1[index] - ranges_2[index]) < 100 and \
            abs(ranges_1[index] - ranges_3[index]) < 100 and \
            abs(ranges_2[index] - ranges_3[index]) < 100:
                
                # Check if the distance is less than or equal to 200
                if ranges_1[index] <= 200:
                    processed_ranges.append("1")
                else:
                    processed_ranges.append("0")
            else:
                processed_ranges.append("0")

        
        if ranges_1[0] > 450:
            processed_ranges.append("1")
        else:
            processed_ranges.append("0")
        
        # Check if the distance measured by the last sensor is greater than 500
        if ranges_3[-1] > 450:
            processed_ranges.append("1")
        else:
            processed_ranges.append("0")
        
        sensor_ranges_str = " ".join(processed_ranges)
        return sensor_ranges_str
