from machine import Pin, I2C
from gpio_lcd import GpioLcd
from LCD_prints import PrintForLCD
from readRegs import readRegs
import utime


#utime.sleep(2)

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
max17330reg_A = readRegs(max17330_A)
max17330reg_B = readRegs(max17330_B)

p = PrintForLCD(lcd=lcd)

while True:
    for i in range(20):
        try:
            battAPerc = max17330reg_A.readRepSOC(addr=0x36,memaddr=0x06,nbytes=2)/100
            # battPerc = max17330reg_A.readfrom_mem(0x36, 0x06, 2, 8)
        except:
            OnBoardLed = Pin(25, Pin.OUT)
            OnBoardLed.value(1)
            battAPerc = 0.05*i
            
        try:
            battBPerc = max17330reg_B.readRepSOC(addr=0x76,memaddr=0x06,nbytes=2)/100
        except:
            battBPerc = 0.05*i
            
        
        p.printMockScreen(battAPerc = round(battAPerc,4), battBPerc = round(battBPerc,4))
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

