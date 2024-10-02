from time    import sleep_ms
warte_millisekunden =sleep_ms

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
                ton.on()
                led(0)
                warte_millisekunden(dit_time_ms)
                ton.off()
                led(1)
                warte_millisekunden(dit_time_ms)
            if element=='-':
                ton.on()
                led(0)
                warte_millisekunden(dit_time_ms*3)
                ton.off()
                led(1)
                warte_millisekunden(dit_time_ms)
        warte_millisekunden(dit_time_ms*3)

''' hauptprogramm'''
def main():
    morse(text='de dk2jk = swt 2024 = bake +', dit_time_ms = poti.read(), freq=600)
 
def run():   
    while 1:
        main()
        sleep_ms(1000) # jede sekunde wiederholen

