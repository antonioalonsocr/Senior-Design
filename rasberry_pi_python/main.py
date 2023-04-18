from machine import Pin, I2C
from gpio_lcd import GpioLcd
from LCD_prints import PrintForLCD
from chipClasses import Max17330
import utime

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

while True:
    
    # Battery screen ======================================================================
    for i in range(10):
        A17330.AllowChgB(0x36)
        B17330.AllowChgB(0x76)
        try:
            battAPerc = A17330.readRepSOC(addr=0x36)
            # battPerc = max17330reg_A.readfrom_mem(0x36, 0x06, 2, 8)
        except:
            OnBoardLed = Pin(25, Pin.OUT)
            OnBoardLed.value(1)
            battAPerc = 0.05*i
            
        try:
            battBPerc = B17330.readRepSOC(addr=0x76)
        except:
            battBPerc = 0.05*i
        
        p.printRepSOCScreen(battAPerc = battAPerc, battBPerc = battBPerc)
        
        utime.sleep(1)
    
        
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

