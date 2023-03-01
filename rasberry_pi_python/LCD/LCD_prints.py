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

        # Determine what the character should look like
        byteList = []
        for pixLevel in range(8):
            if battPercentage/(0.125*(pixLevel+1)) >= 1:
                byteList = [0x1f] + byteList
            else:
                byteList = [(0b1111100000 >> int((battPercentage % 0.125)//0.025)) & 0x1f] + byteList
                for _ in range(7-pixLevel):
                    byteList = [0x00] + byteList
                break

        # set as a custom character
        self.lcd.custom_char(0,bytearray(byteList))

        # print character
        self.lcd.putchar(0)