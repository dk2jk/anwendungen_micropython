'''
Einbindung des dig. Oszillators si5351
das Modul 'i2c.si5351_jk.py' stellt nur die Funktion
    'frequenz(f, clockNr=0)'
zur Verfügung.
Die I2C Routinen sind im Modul 'versteckt'.
Test:
>>> import i2c.si5351_jk as si
>>> si.frequenz(7029500)
>>> si.frequenz(7029600)
>>> si.frequenz(0)
'''
import i2c.si5351_jk as si
import time

while 1:
    try:         
        si.frequenz(7029500) # an
        time.sleep(0.2)
        si.frequenz(0)       #aus
        time.sleep(0.2)
    except KeyboardInterrupt:
        si.frequenz(0)
        break
               

        
