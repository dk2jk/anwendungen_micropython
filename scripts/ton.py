# MicroPython v1.20.0 on 2023-04-26; Raspberry Pi Pico with RP2040

from machine import Pin,PWM
from ports_rp2040 import *

# mithoerton
pwm   = PWM ( Pin(TON_PIN))
pwm.freq(800)
pwm.duty_u16(0)

def freq(f):
    pwm.freq(f)   
def on():
        pwm.duty_u16(32767)
def off():
        pwm.duty_u16(0)
def set(x=False):
    if x:
        on()
    else:
        off()
