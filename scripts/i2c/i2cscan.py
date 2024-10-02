
"""
#rp2040
Folgende Python-Code-Zeilen scannen den I2C1 (nicht I2C0)
Anzahl und Adressen von gefundenen Bus-Teilnemern werden
anschliessend angezeigt
"""

from  machine import Pin, I2C

i2c=I2C(1,sda=Pin(2), scl=Pin(3), freq=100000)

print('I2C1 Datenbus wird gescannt')
devices = i2c.scan() # eine Liste aller I2C1-Bus-Teilnehmer wird erzeugt

device_count = len(devices) #Anzahl Bus-Teilnehmer

if device_count == 0:
    print('Kein I2C-Busteilnehmer erkannt')
else:
    print(device_count, 'Bus-Teilnehmer gefunden ')

for device in devices:
    print('Adresse Dezimal:', device, ", Adresse Hexadez. : ", hex(device))
	
	