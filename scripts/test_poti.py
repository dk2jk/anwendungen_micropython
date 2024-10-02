from machine import Pin,ADC
from ports_rp2040 import *

adc   = ADC(Pin(ADC_PIN))

import time

while True:
    y= adc.read_u16()# 0...1
    print(y)
    time.sleep(3)
