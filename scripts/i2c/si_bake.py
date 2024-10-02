from time    import sleep_ms
import i2c.si5351_jk as si

#aus unserem baukasten
import ton    # 'freq', 'off', 'on'
import poti   # 'read'

#die blaue led:
from machine import Pin
LED_BLAU_PIN  = const(7)
led   = Pin(LED_BLAU_PIN,Pin.OUT,value=1) # low aktiv

''' einem buchstaben wird eine kurz-lang folge zugeordnet
    {} ist ein dictionary
    Aufruf zum Beispiel:  lookup['F']   ---> '..-.'
'''
lookup = {'!': '-.-.--',
          "'": '.----.',
          '"': '.-..-.',
          '$': '...-..-',
          '&': '.-...',
          '(': '-.--.',
          ')': '-.--.-',
          '+': '.-.-.',
          ',': '--..--',
          '-': '-....-',
          '.': '.-.-.-',
          '/': '-..-.',
          '0': '-----',
          '1': '.----',
          '2': '..---',
          '3': '...--',
          '4': '....-',
          '5': '.....',
          '6': '-....',
          '7': '--...',
          '8': '---..',
          '9': '----.',
          ':': '---...',
          ';': '-.-.-.',
          '=': '-...-',
          '?': '..--..',
          '@': '.--.-.',
          'A': '.-',
          'B': '-...',
          'C': '-.-.',
          'D': '-..',
          'E': '.',
          'F': '..-.',
          'G': '--.',
          'H': '....',
          'I': '..',
          'J': '.---',
          'K': '-.-',
          'L': '.-..',
          'M': '--',
          'N': '-.',
          'O': '---',
          'P': '.--.',
          'Q': '--.-',
          'R': '.-.',
          'S': '...',
          'T': '-',
          'U': '..-',
          'V': '...-',
          'W': '.--',
          'X': '-..-',
          'Y': '-.--',
          'Z': '--..',
          '_': '..--.-',
          ' ': ' ',
          }

''' aus einem text wird eine liste von eine kurz-lang folgen
    'test'  -->   liste    ['-', '.', '...', '-']
'''
def text_to_morse(text='test'):
    liste=[ lookup[ char.upper() ] for char in text ]
    return liste

#text senden
def morse(text = 'test', dit_time_ms=80, freq=550):
    print(f'sende Text: {text}')
    ton.freq(freq)
    kurz_lang_liste=text_to_morse(text)
    #'test'  -->   kurz_lang_liste =    ['-', '.', '...', '-'] '''
    print(kurz_lang_liste)
    for morsezeichen in kurz_lang_liste:
        print(morsezeichen, end='   ')
        for element in morsezeichen:
            if element=='.':
                tx(on=1)
                led(0)
                sleep_ms(dit_time_ms)
                tx(on=0)
                led(1)
                sleep_ms(dit_time_ms)
            if element=='-':
                tx(on=1)
                led(0)
                sleep_ms(dit_time_ms*3)
                tx(on=0)
                led(1)
                sleep_ms(dit_time_ms)
        sleep_ms(dit_time_ms*3)


def tx(freq=7030000, on= False):
    if on:
        si.frequenz (freq, 0)
    else:
        si.frequenz (0, 0)
        
si.init()

''' hauptprogramm'''
def main():
    morse(text='vvv de dk2jk = bake mit raspi pico und si5351 +', dit_time_ms = poti.read(), freq=600)
 
def run():   
    while 1:
        main()
        sleep_ms(1000) # jede sekunde wiederholen

if __name__ == '__main__':
    run()