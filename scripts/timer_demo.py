import time

interval=0
tn=0

def timer_start(_interval):
    global tn,c
    interval=_interval
    tn= time.ticks_ms()
    
def timer_overflow():
    global tn
    if  time.ticks_ms() > tn:
        tn=tn+interval
        return True
    else:
        return False

if __name__ == '__main__':
    timer_start(1000)
    while 1:
        if timer_overflow():
            print (time.time())
        time.sleep(.1)