import board

i2c = board.I2C()
if i2c.try_lock():
    addresses = [hex(x) for x in i2c.scan()]
    print("I2C Addresses:", addresses)
    i2c.unlock()