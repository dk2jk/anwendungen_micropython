from machine import Pin,ADC
from ports_rp2040 import *

adc   = ADC(Pin(ADC_PIN))

#speed poti 
def read():
    y= adc.read_u16()/ 65535  # 0...1
    tdit=int(1200/(10+30*y))
    return tdit