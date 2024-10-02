from machine import Pin
from ports_rp2040 import *

_key   = Pin(KEY_PIN,Pin.OUT,value=1)  # key ausgang , hier als led low aktiv

def set(x=False):
    if x:
        _key(0)
    else:
        _key(1)