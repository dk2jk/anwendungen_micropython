from machine import Pin, PWM,Timer
from time import sleep,sleep_ms,sleep_us
import micropython
micropython.alloc_emergency_exception_buf(100)
from sintab import genSintab

trigger= Pin(5, Pin.OUT)#

#PWM #################
''' ergibt ca 440 hz
pwm=PWM( Pin(4) )
TAKT =const(32000)
NULLINIE= 0x8000
pwm.freq(TAKT)
pwm.duty_u16(NULLINIE)
MAX = const (0x1_00_00_00)
STEP= const ( 0x_12_80_00)
'''
pwm=PWM( Pin(4) )
TAKT =const(32000)
NULLINIE= 0x8000
pwm.freq(TAKT)
pwm.duty_u16(NULLINIE)
MAX = const (0x1_00_00_00)
STEP= const ( 0x_12_80_00)

class dds:
    acc     = MAX-1    # 0..1
    timer  = None
    index  = 0
    en     = 0

sintab =genSintab(n=256,ampl=0x8000,rand=0x100)

def dds_nextstep(t):
    if dds.en:
        x=sintab[dds.index]
        pwm.duty_u16(x)
        dds.acc = (dds.acc + STEP)%MAX
        if dds.acc >= MAX:    # ueberlauf 
             dds.acc = dds.acc - MAX  # 0x1_00_12_34 =>  0x00_00_12_34
        dds.index = dds.acc >>16      # 0x0_ff_12_34 =>  0xff
        trigger( x> NULLINIE)
    else:
       pwm.duty_u16(NULLINIE)
        
def dds_begin():   
    pwm.duty_u16(NULLINIE) # mitte
    dds.timer = Timer()
    dds.timer.init(freq =TAKT, mode = Timer.PERIODIC, callback =dds_nextstep)
    
dds.en=1    
dds_begin()

