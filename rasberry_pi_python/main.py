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

max1 = I2C(id=1,scl=Pin(15),sda=Pin(14))
#max2 = I2C(id=1,scl=Pin(13),sda=Pin(12))

'''
in command window:
max17330 = I2C(id=1, scl=Pin(15), sda=Pin(14))
bstring = max17330.readfrom_mem(0x36,0x06,2,addrsize=8)
bstring[0] 
bstring[1]
'''

# utime.sleep(1)
# print(max17330.scan())
utime.sleep(1)
#print(max17330.readfrom_mem(0x36,0x06,2))
max17330reg = readRegs(max17330)

p = PrintForLCD(lcd=lcd)
while True:
    for i in range(20):
        try:
            battPerc = max17330reg.readRepSOC()/100
        except:
            OnBoardLed = Pin(25, Pin.OUT)
            OnBoardLed.value(1)
        
        p.printMockScreen(battAPerc = battPerc, battBPerc = 0.05*i)
        utime.sleep(1)
    
#utime.sleep(2)

OnBoardLed = Pin(25, Pin.OUT)
#OnBoardLed.value(1)


# a = 56
# 
# lcd.clear()
# a_string = (hex(a))
# lcd.putstr(a_string)


# #The following line of codes should be tested one by one according to your needs
#
# #1. To print a string to the LCD, you can use
#lcd.clear()
#lcd.putstr('hello world')
#utime.sleep(1)
# #2. Now, to clear the display.
#lcd.clear()
#utime.sleep(1)
# #3. and to exactly position the cursor location
lcd.move_to(0,1)
# lcd.putstr('LCD16x2display')
# # If you do not set the cursor position,
# # the character will be displayed in the
# # default cursor position starting from
# # 0, x and 0, y location which is the top left-hand side.
# # There are other useful functions we can use in using the LCD.
# #4. Show the cursor
lcd.show_cursor()
# #5. Hide the cursor
# lcd.hide_cursor()
# #6. Turn ON blinking cursor
lcd.blink_cursor_on()
# #7. Turn OFF blinking cursor
# lcd.blink_cursor_off()
# #8. Disable display
# lcd.display_off()
# this will only hide the characters
# #9. Enable display
# lcd.display_on()
# #10. Turn backlight OFF
# lcd.backlight_off()
# #11. Turn backlight ON
# lcd.backlight_on()
# # 12. Print a single character
# lcd.putchar('x')
# but this will only print 1 character
# #13. Display a custom characters using hex codes, you can create the character from <a href="https://maxpromer.github.io/LCD-Character-Creator/">here.</a>
# happy_face = bytearray([0x00,0x0A,0x00,0x04,0x00,0x11,0x0E,0x00])
# lcd.custom_char(0, happy_face)
# lcd.putchar(chr(0))
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

