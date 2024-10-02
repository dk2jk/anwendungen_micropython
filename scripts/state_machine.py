#### MicroPython v1.23.0 on 2024-06-02; ESP module with ESP8266
from timer import Timer
from time import sleep

#diverse objekte
timer = Timer(0) # Timer fuer dit und dah
timer_poti_lesen = Timer(200,repeat=True)  # alle 200ms wird speed poti gelesen
#  Konstanten verzoegerungen
TDELAY1= const(10) # millisec  anfangsverzoegerung
TDELAY2= const(200) # millisec end verzoegerung


# folgende objekte wurde einzeln getestet,
# sie stehen daher in separaten modulen
import ptt    # ptt ausgang , hier als led low aktiv
import key    # tast ausgang
import tune   # tune taste
import paddle # paddle pins
import poti   # speed poti
import ton    # mithoerton

tdit     = None              # zeit fuer dit
wpm      = None # wird nur fuer anzeige benoetigt

class State():
    def __init__(self):
        self.next = 'standby'
    def set(self,new_state,interval, _key,_ptt):
        self.next=new_state
        timer.start(interval)   # zeitpunkt fuer ende des naechsten zustands
        key.set(_key)   # tasten ausgang ein oder aus
        ptt.set(_ptt)   # ptt ausgang ein oder aus
        ton.set(_key)   # mithörton ein oder aus
state=State()        

#funktionen
# word per minute und zeit für kurzes element einstellen
def update_wpm():
    global wpm,tdit
    tdit=poti.read()
    wpm = int(1200 / tdit)
    
   
def standby():
    if tune.get():
        state.set('tune_delay1',10 , 0, 1)
    if paddle.dit() or paddle.dah():
        state.set( 'delay1', 10 , 0,1)

def delay1():
    if timer():
        if paddle.dit():  
            state.set('dit_on',tdit , 1,1)
        elif paddle.dah():  
            state.set('dah_on', tdit*3 , 1,1)
        else:
             # war nix
            state.set('standby',1 , 0,0)

def dit_on():
    if timer():
        state.set('dit_pause',tdit , 0,1)

def dah_on():  
    if timer():  
        state.set( 'dah_pause',tdit , 0,1)

def dit_pause():
    if timer():
        if paddle.dah():  # dah paddle hat vorrang
            state.set( 'dah_on',tdit*3 , 1,1)
        elif paddle.dit():
            state.set('dit_on',tdit , 1,1)
        else:
            #kein paddle
            state.set( 'delay2', TDELAY2 , 0,1) 

def dah_pause():
    if timer():
        if paddle.dit():  # dit paddle hat vorrang
            state.set('dit_on', tdit , 1,1)
        elif paddle.dah():    
            state.set( 'dah_on', tdit*3 , 1,1)
        else:
            #kein paddle   
            state.set('delay2', TDELAY2 , 0,1)

def delay2():   
    if paddle.dit():       # paddle wurde doch noch betaetigt
        state.set('dit_on',tdit , 1,1)
    elif paddle.dah():
        state.set('dah_on', tdit*3 , 1,1)
    elif timer():
        state.set('standby', 1 , 0,0)

def tune_delay1():
    if tune.get():    
        state.set('tune_on',1 , 1,1)
    if timer(): 
        state.set('standby',1 , 0,0)

def tune_on(): 
    if tune.get(): # noch tune taste gedrueckt
        pass
    else:   
        state.set('tune_delay2',400 , 0,1)

def tune_delay2():
    if tune.get():       
        state.set('tune_on',1 , 1,1)
    if timer(): 
        state.set( 'standby', 1 , 0,0)


doState={
'standby'     : standby ,
'delay1'      : delay1,
'dit_on'      : dit_on,
'dah_on'      : dah_on,
'dit_pause'   : dit_pause,
'dah_pause'   : dah_pause,
'delay2'      : delay2,
'tune_delay1' : tune_delay1,
'tune_on'     : tune_on,
'tune_delay2' : tune_delay2}


def run():
    if timer_poti_lesen():  # von zeit zu zeit speed lesen
        update_wpm()     
    doState[state.next]()
    print(state.next)
    sleep(.3)
   
while 1:
    run()