'''
# Trying to print battery perc
def printBatt(batt): 
    byteList = [] 
    for pixLevel in range(8):
        if batt/(0.125*(pixLevel+1)) >= 1:
            byteList = [0x1f] + byteList
        else:
            # Determined shift by knowing how many pixels need light
            # One pixel is 2.5% (0.025) and one line is 12.5% (0.125)
            shiftBy = int((batt % 0.125)//0.025)

            # shiftBy is the number of pixels to turn on
            # then bitwise & to only get last 5 bits
            byteList = [(0b1111100000 >> shiftBy) & 0x1f] + byteList
            for _ in range(7-pixLevel):
                byteList = [0x00] + byteList
            break
        
    for elem in byteList:
        print(bin(elem))

if __name__ == "__main__":
    printBatt(0.55)
'''


from machine import Pin, I2C
from gpio_lcd import GpioLcd
from LCD_prints import PrintForLCD
from readRegs import readRegs
import utime


max1 = I2C(id=1,scl=Pin(15),sda=Pin(14))
utime.sleep(1)
max2 = I2C(id=1,scl=Pin(11),sda=Pin(10))

utime.sleep(1)

'''
print(max1.scan())
print(max2.scan())
'''

'''
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=40)
p = PrintForLCD(lcd=lcd)
max1reg = readRegs(max1)
print(max1.scan())
print(max1reg.readRepSOC())
'''
temp = []
while temp == []:
    max1 = I2C(id=1,scl=Pin(15),sda=Pin(14))
    utime.sleep(1)

    temp = max1.scan()
    print(temp)
    utime.sleep()
