from time import sleep
from machine import Pin
LED_BLAU_PIN  = const(7)
led  = Pin(LED_BLAU_PIN,Pin.OUT,value=1)

def blink():
    while True:
        x= not led()
        led(x)
        sleep(.33)
        


