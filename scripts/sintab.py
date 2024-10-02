import math


def genSintab(*,n=256,ampl=0x8000,rand=0x10):
    '''
    es wird eine sinustabelle mit 256 stuetzstellen ueber 2pi erzeugt.
    der offset ist 0x8000; mit der amplitude 0x7f00 werden 256 werte
    von 0x100 bis 0xff00 erzeugt
        '''
    sintab=[]
    step= math.pi*2/n 
    for i in range (0,n+4):
        y = int(ampl+(ampl-rand)*math.sin(i*step))
        sintab.append(y)
    return sintab


if __name__=='__main__':   
    sintab = genSintab()
    print( 'sinustabelle')
    for i in sintab:
        print(f"0x{i:04x}")
        try:
            print(genSintab.__doc__)
        except:
            pass
    