# timer...

import time
MAX= const(2**16-1)
class Timer:
    def __init__(self,ms, repeat=False):
        self.start(ms)
        self.repeat=repeat
    def start(self,ms):
        if ms==0:
            ms= MAX  
        self.interval=int(ms)
        self.deadline = time.ticks_add(time.ticks_ms(), self.interval)
    def __call__(self):    
        if  time.ticks_diff(self.deadline, time.ticks_ms()) < 0:
            if self.repeat:
                self.start(self.interval)
            else:
                self.start(0)
            return True
        else:
            return False

if __name__ == '__main__':
    timer= Timer(1000,1)
    while 1:
        if timer():
            print (time.time())