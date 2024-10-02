#aus unserem baukasten:
from ports_rp2040 import *
from machine import Pin,PWM

tunetaste  = Pin(TUNE_PIN,Pin.IN) 

# mithoerton
ton   = PWM ( Pin(TON_PIN))
ton.freq(600)
ton.duty_u16(0)

while True:
    if tunetaste()==0:
        ton.duty_u16(32767)
    else:
        ton.duty_u16(0)
    #sleep(.01)





