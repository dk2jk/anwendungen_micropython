from machine import Pin
from ports_rp2040 import *

#paddle pins
_dit   = Pin(PADDLE_PIN_2,Pin.IN)
_dah   = Pin(PADDLE_PIN_1,Pin.IN)

def dah():
    return  not _dah()  
def dit():
    return  not _dit()