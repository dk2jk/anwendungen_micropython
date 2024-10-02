#### MicroPython v1.23.0 on 2024-06-02; ESP module with ESP8266
from timer import Timer

#diverse objekte
timer = Timer(0) # Timer fuer dit und dah
timer_poti_lesen = Timer(200,repeat=True)  # alle 200ms wird speed poti gelesen

# folgende objekte wurde einzeln getestet,
# sie stehen daher in separaten modulen
import ptt    # ptt ausgang , hier als led low aktiv
import key    # tast ausgang
import tune   # tune taste
import paddle # paddle pins
import poti   # speed poti
import ton    # mithoerton

# Konstanten state machine
STANDBY      =const(0) # ruhezustand
DELAY1       =const(1) # anfangsverzoegerung, ptt ist schon an
DIT_ON       =const(2) # kurzes zeichen
DAH_ON       =const(3) # langes zeichen
DIT_PAUSE    =const(4) # element pause fuer kurzes zeichen
DAH_PAUSE    =const(5) # element pause fuer langes zeichen
DELAY2       =const(6) # end verzoegerung , ptt ist noch an
TUNE_DELAY1  =const(7)# Tune: anfangsverzoegerung, ptt ist schon an
TUNE_ON      =const(8)# Tune: key on, solange tune taste gedrueckt ist
TUNE_DELAY2  =const(9)# Tune: end verzoegerung , ptt ist noch an

#  Konstanten verzoegerungen
TDELAY1= const(10) # millisec  anfangsverzoegerung
TDELAY2= const(200) # millisec end verzoegerung


#variablen
state = None # zustand des keyers ( Statemachine)
wpm   = None # wird nur fuer anzeige benoetigt
tdit  = None # zeit fuer dit

#function neuen zustand einstellen
def start_state(next, ms=1 , key_on=False, ptt_on=False ):
    global state
    state=next        # naechster zustand
    timer.start(ms)   # zeitpunkt fuer ende des naechsten zustands
    key.set(key_on)   # tasten ausgang ein oder aus
    ptt.set(ptt_on)   # ptt ausgang ein oder aus
    ton.set(key_on)   # mithörton ein oder aus
    

start_state(STANDBY, ms=1 , key_on=0,ptt_on=0) # start mit STANDBY

# word per minute und zeit für kurzes element einstellen
def update_wpm():
    global wpm,tdit
    tdit=poti.read()
    wpm = int(1200 / tdit)

update_wpm()  # speed lesen


# die state machine
# es wird nur gewartet, bis etwas passiert (event)
# meist nur eine abfolge von nicht erfüllter if's
def run():
    if timer_poti_lesen():  # von zeit zu zeit speed lesen
        update_wpm()
           
    if state==STANDBY:       
        if tune.get():                       # tune taste gedrueckt ?
            start_state(TUNE_DELAY1, ms=10 , key_on=0,ptt_on=1)
        if paddle.dit() or paddle.dah(): # oder eines der paddles?
            start_state(DELAY1, ms=TDELAY1 , key_on=0,ptt_on=1)
         
    elif state==DELAY1:  # anfangsverzoegerung, ptt ist schon an
        if timer():
            if paddle.dit():
                start_state(DIT_ON, ms=tdit , key_on=1,ptt_on=1)
            elif paddle.dah():
                start_state(DAH_ON, ms=tdit*3 , key_on=1,ptt_on=1)
            else:
                 # war nix
                start_state(STANDBY, ms=1 , key_on=0,ptt_on=0)
           
    elif state==DIT_ON:    # kurzes element laeuft 
        if timer():
            start_state(DIT_PAUSE, ms=tdit , key_on=0,ptt_on=1)
            
    elif state==DIT_PAUSE:   # pausenelement nach kurz laeuft
        if timer():
            if paddle.dah():  # dah paddle hat vorrang
                start_state(DAH_ON, ms=tdit*3 , key_on=1,ptt_on=1)
            elif paddle.dit():
                start_state(DIT_ON, ms=tdit , key_on=1,ptt_on=1)
            else:
                #kein paddle
                start_state(DELAY2, ms=TDELAY2 , key_on=0,ptt_on=1) 
                
    elif state==DELAY2:  # verzoegerung am ende laeuft      
            if paddle.dit():       # paddle wurde doch noch betaetigt 
                start_state(DIT_ON, ms=tdit , key_on=1,ptt_on=1)
            elif paddle.dah():
                start_state(DAH_ON, ms=tdit*3 , key_on=1,ptt_on=1)
            elif timer():    
                start_state(STANDBY, ms=1 , key_on=0,ptt_on=0)
            
    elif state==DAH_ON:  # lang element laeuft
        if timer():
            start_state(DAH_PAUSE, ms=tdit , key_on=0,ptt_on=1)
            
    elif state==DAH_PAUSE:  # pausenelement nach lang laeuft
        if timer():
            if paddle.dit():  # dit paddle hat vorrang
                start_state(DIT_ON, ms=tdit , key_on=1,ptt_on=1)
            elif paddle.dah():
                start_state(DAH_ON, ms=tdit*3 , key_on=1,ptt_on=1)
            else:
                #kein paddle
                start_state(DELAY2, ms=TDELAY2 , key_on=0,ptt_on=1)
                
    elif state==TUNE_DELAY1: 
        if timer(): # nach 100 ms
            if tune.get(): # noch
                start_state(TUNE_ON, ms=1 , key_on=1,ptt_on=1)
            else:
                start_state(STANDBY, ms=1 , key_on=0,ptt_on=0)

    elif state==TUNE_ON:   # ptt und key sind an
        if tune.get(): # noch tune taste gedrueckt
            pass
        else:
            start_state(TUNE_DELAY2, ms=400 , key_on=0,ptt_on=1)
            
    elif state==TUNE_DELAY2: # nach verzoegerung ptt aus
        if tune.get():
            start_state(TUNE_ON, ms=1 , key_on=1,ptt_on=1)
        if timer():
            start_state(STANDBY, ms=1 , key_on=0,ptt_on=0)

# hier gehts los...
     

if __name__=='__main__':
    ton.freq(650)
    while 1:
        run()






