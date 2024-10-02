import i2c.si5351_jk as si
import time

si.init()

fs=[7030000,7030100,7030200,7030300]

t=100
# tonfolgen fs  mit 100 hz abstand ausgeben
while True:
    for count,val in enumerate(fs,0):
        print(count,val)
        time.sleep_ms(100)
        si.frequenz (val, 0)


