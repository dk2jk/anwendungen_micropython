from machine import Pin
from ports_rp2040 import *

_ptt   = Pin(PTT_PIN,Pin.OUT,value=1)  # ptt ausgang , hier als led low aktiv
def set(x=False):
    if x:
        _ptt(0)
    else:
        _ptt(1)