import i2c.my_i2c as i2c
import math

# die tausender duerfen mit '_' getrennt werden
NENNER_MAX =   1_048_574  # 2**20-2
# vorgabe  und pll frequenz in hertz
FXTAL   =  25_000_000  # quarzfrequenz in Hertz
FPLL    = 750_000_000  # PLLA und PLLB frequenzin Hertz, mitte zwischen 600 und 900
PLL     = { 'A': 26, 'B' : 34}        # register basis adressen
MS      = { 0 : 42, 1 : 50, 2 : 58}   # register basis adressen
mA      = { '2mA' : 0  , '4mA' : 1 , '6mA' : 2, '8mA' : 3}
                                      # driver 2,4,6,8 mA

def abc_berechnen( f):
    ## [a+ (b/c)]  soll zwischen 8 und 254 sein.
    a,rest = divmod(FPLL, f)
    b      = int(NENNER_MAX*rest/f)
    c      = NENNER_MAX
    return a, b, c
    
def p123_berechnen(a,b,c):
    p1 = int(128 * a + math.floor(128*(b/c) )-512 )    #[7:0]
    p2 = int(128 * b - c * math.floor (128 *(b/c)))    #[19:0]
    p3 = c                                             #[19:0]
    return p1, p2, p3

def register_berechnen(p1,p2,p3):
    reg= [0]*8   
    reg[0]   = (p3 & 0xff00) >> 8 # p3_15_8
    reg[1]   = p3 & 0xff  #p3_7_0
    reg[2]   = (p1 & 0x3_00_00 ) >>16  #p1_17_16
    reg[3]   = (p1 & 0xff00) >>8 #p1_15_8
    reg[4]   = p1 & 0xff #p1_7_0        
    p3_19_16 = (p3 & 0xf0000 ) >>12
    p2_19_16 = (p2 & 0xf0000 ) >>16
    reg[5]   = p3_19_16 + p2_19_16
    reg[6]   = (p2 & 0xff00) >>8  #p2_15_8
    reg[7]   = p2 & 0xff  #p2_7_0
    return reg

def drive( clockNr,mA):
    adr = 16 + clockNr
    y= i2c.read_byte(adr)
    x   = i2c.read_byte(adr) & 0b111111_00
    y   = x | mA
    i2c.write_byte(adr, y)

def startup():
    i2c.write_byte(183, 0b11_010010)        # 10pF
    i2c.write_byte(  3, 0x07)               # alle clk sperren
    i2c.write_byte( 16, 0b_0_0_0_0_11_11)   # CLK0 Control
    i2c.write_byte( 17, 0b_0_0_0_0_11_11)   # dito fuer clock1  MultiSynth 1
    i2c.write_byte( 18, 0b_0_0_0_0_11_11)   # dito fuer clock2  MultiSynth 2
    
    #        7 -------------0_ CLK0 is powered up.
    #          6------------1_ MS0 operates in integer mode. 0 fractional mode
    #            5----------0_ Select PLLA as the source for MultiSynth0. 1_ waere PLLB                       
    #              4--------0_ Output Clock 0 is not inverted.
    #                32----11_ Select MultiSynth 0 as the source for CLK0; falls 00_ fpll , fxtal
    #                   10-11_ 8 mA drive
    i2c.write_byte( 24, 0b_10_10_10_10)      # aus -> high impedance
    for clockNr in range (3):
        drive( clockNr, mA['2mA'])

def frequenz(f, clockNr=0):
    dis_clock(clockNr)
    if f==0:
        pass    # clock aus
    else:
        a,b,c    = abc_berechnen( f)
        p1,p2,p3 = p123_berechnen(a,b,c)
        reg      = register_berechnen(p1,p2,p3)
        i2c.write_8bytes(MS[clockNr],  reg)
        en_clock(clockNr)
        
def init():
    startup() # allgemeines
    #PLL:
    a,b,c    = abc_berechnen(FXTAL)
    p1,p2,p3 = p123_berechnen( a,b,c)
    reg      = register_berechnen(p1,p2,p3)
    i2c.write_8bytes(PLL['A'], reg)
    i2c.write_8bytes(PLL['B'], reg)
    i2c.write_byte(177, 0xa0) # reset plla und b


def en_clock(clock_nr):
    x = i2c.read_byte(3)
    y = ~(1<<clock_nr) & x
    i2c.write_byte( 3, y) 
    
def dis_clock(clock_nr):
    x = i2c.read_byte(3)
    y = (1<<clock_nr) | x
    i2c.write_byte( 3, y) 

def off():
    for clockNr in range (3):
        dis_clock(clockNr)   
 
if __name__ == '__main__':  
    #init()
    frequenz(7e6, 0)
    frequenz(7e6+10000,  1)
    frequenz(7e6+20000,  2)
