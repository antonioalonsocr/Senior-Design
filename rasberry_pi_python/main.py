from machine import Pin, I2C
from gpio_lcd import GpioLcd
from LCD_prints import PrintForLCD
from chipClasses import Max17330
from buttonCode import get_button
import led_neopix as neopixel
import utime


stripA = neopixel.Neopixel(4, 0, 0, "RGB")
stripB = neopixel.Neopixel(4, 1, 1, "RGB")
stripA.brightness(100)
stripB.brightness(100)

def lightUpLED(battACurr, battBCurr):
    
    if battACurr > 5:
        chgstr = "chg"
        stripA.fill((255,0,0))
    elif battACurr < -5:
        chgstr = "dchg"
        stripA.fill((0,255,0))
    else:
        chgstr = "ntrl"
        stripA.fill((255,255,255))

    stripA.show()
    
    if battBCurr > 5:
        chgstr = "chg"
        stripB.fill((255,0,0))
    elif battBCurr < -5:
        chgstr = "dchg"
        stripB.fill((0,255,0))
    else:
        chgstr = "ntrl"
        stripB.fill((255,255,255))
    
    stripB.show()


#utime.sleep(2)
OnBoardLed = Pin(25, Pin.OUT)
OnBoardLed.value(0)

# Create the LCD object
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=40)

max17330_A = I2C(id=1,scl=Pin(15),sda=Pin(14))
max17330_B = I2C(id=0,scl=Pin(13),sda=Pin(12))
#max2 = I2C(id=1,scl=Pin(13),sda=Pin(12))

'''
in command window:
max17330 = I2C(id=1, scl=Pin(15), sda=Pin(14))
bstring = max17330.readfrom_mem(0x36,0x06,2,addrsize=8)
bstring[0] 
bstring[1]
'''

# utime.sleep(1)
print('A')
print(max17330_A.scan())
print('B')
print(max17330_B.scan())
utime.sleep(1)
#print(max17330.readfrom_mem(0x36,0x06,2))
#max17330reg_A = readRegs(max17330_A)
#max17330reg_B = readRegs(max17330_B)
#max17330reg_B.changeBit()
A17330 = Max17330(max17330_A)
B17330 = Max17330(max17330_B)

p = PrintForLCD(lcd=lcd)

A17330.unlockWP(addr=0x36)
B17330.unlockWP(addr=0x76)

A17330.ParEN(addr=0x36)
B17330.ParEN(addr=0x76)

A17330.AllowChgB(0x36)
B17330.AllowChgB(0x76)

buttonPIN = 16
button = Pin(buttonPIN, Pin.IN, Pin.PULL_UP)

while True:
    
    # Battery screen ======================================================================
    while True:
        A17330.AllowChgB(0x36)
        B17330.AllowChgB(0x76)
        try:
            battAPerc = A17330.readRepSOC(addr=0x36)
            # battPerc = max17330reg_A.readfrom_mem(0x36, 0x06, 2, 8)
        except:
            OnBoardLed = Pin(25, Pin.OUT)
            OnBoardLed.value(1)
            battAPerc = 0.05
            
        try:
            battBPerc = B17330.readRepSOC(addr=0x76)
        except:
            battBPerc = 0.05
        
        p.printRepSOCScreen(battAPerc = battAPerc, battBPerc = battBPerc)

        currA=A17330.readCurrentReg(addr=0x36)
        currB=B17330.readCurrentReg(addr=0x76)
        lightUpLED(currA,currB)
        for _ in range(10):
            utime.sleep(0.1)
            if get_button(button):
                breakwhile = True
                break
        if breakwhile:
            break
        
    
        
    # Charging Current screen ======================================================================
    for i in range(10):
        A17330.AllowChgB(0x36)
        B17330.AllowChgB(0x76)
        try:
            currA = A17330.readCurrentReg(addr=0x36)
            # battPerc = max17330reg_A.readfrom_mem(0x36, 0x06, 2, 8)
        except:  
             OnBoardLed.value(1)
             currA = 0.05*i
        try:
            currB = B17330.readCurrentReg(addr=0x76)
        except:
            currB = 0.05*i
        
        p.printCurrScreen(battACurr = currA, battBCurr = currB)
        
        print("curr----------------")
        print(currA)
        print(currB)
        lightUpLED(currA,currB)
        utime.sleep(1)

    # Charging Voltage screen ======================================================================
    for i in range(10):
        A17330.AllowChgB(0x36)
        B17330.AllowChgB(0x76)
        try:
            voltA = A17330.readCurrentReg(addr=0x36)
            # battPerc = max17330reg_A.readfrom_mem(0x36, 0x06, 2, 8)
        except:  
             OnBoardLed.value(1)
             voltA = 0.05*i
        try:
            voltB = B17330.readCurrentReg(addr=0x76)
        except:
            voltB = 0.05*i
        
        p.printVoltScreen(battAVolt = voltA, battAVolt = voltB)
        
        print("volt----------------")
        print(voltA)
        print(voltB)
        lightUpLED(voltA,voltB)
        utime.sleep(1)

#utime.sleep(2)

OnBoardLed = Pin(25, Pin.OUT)
#OnBoardLed.value(1)

'''
lcd.hide_cursor()
p = PrintForLCD(lcd=lcd)
for i in range(21):
    lcd.move_to(0,1)
    p.printBatteryPercentageChar(i*0.01)
    utime.sleep(0.1)
    
p.printMockScreen()

for i in [0.3, 0.4, 0.8]:
    utime.sleep(1)
    p.assignBatteryChar(i, 0)
'''

