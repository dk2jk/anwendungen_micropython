#rp2040
from machine import Pin, I2C
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000, timeout=50000)
adr=0x60

def write_byte( register, value):
    value = value & 0xff
    i2c.writeto_mem(  adr, register,  bytes( [value] ))
    return

def read_byte( register):
    buffera = bytearray(1)
    i2c.readfrom_mem_into( adr, register, buffera)
    return buffera[0]

def write_8bytes(baseadr, list8):
    i2c.writeto_mem(adr, baseadr,  bytes(list8))
    return