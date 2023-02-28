class PrintForLCD:
    def __init__(self, lcd):
        self.lcd = lcd
        self.initChars()
    
    def initChars(self, specChars=0):
        if specChars == 0:
            self.lcd.custom_char(0,bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            self.lcd.custom_char(1,bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1f]))
            self.lcd.custom_char(2,bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x1f,0x1f]))
            self.lcd.custom_char(3,bytearray([0x00,0x00,0x00,0x00,0x00,0x1f,0x1f,0x1f]))
            self.lcd.custom_char(4,bytearray([0x00,0x00,0x00,0x00,0x1f,0x1f,0x1f,0x1f]))
            self.lcd.custom_char(5,bytearray([0x00,0x00,0x00,0x1f,0x1f,0x1f,0x1f,0x1f]))
            self.lcd.custom_char(6,bytearray([0x00,0x00,0x1f,0x1f,0x1f,0x1f,0x1f,0x1f]))
            self.lcd.custom_char(7,bytearray([0x1f,0x1f,0x1f,0x1f,0x1f,0x1f,0x1f,0x1f]))
    
    def printBatteryPercentageChar(self,battPercentage):
        """Prints special character to display battery percentage.
        expects a floating point between 0 and 1"""
        self.initChars(specChars=0)
        if battPercentage < 0.125:   self.lcd.putchar(chr(0))
        elif battPercentage < 0.25:  self.lcd.putchar(chr(1))
        elif battPercentage < 0.375: self.lcd.putchar(chr(2))
        elif battPercentage < 0.50:  self.lcd.putchar(chr(3))
        elif battPercentage < 0.625: self.lcd.putchar(chr(4))
        elif battPercentage < 0.75:  self.lcd.putchar(chr(5))
        elif battPercentage < 0.875: self.lcd.putchar(chr(6))
        else:                        self.lcd.putchar(chr(7))