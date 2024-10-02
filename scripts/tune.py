from machine import Pin
from ports_rp2040 import *

_tune  = Pin(TUNE_PIN,Pin.IN)  # tune taste
def get():
    return not _tune()