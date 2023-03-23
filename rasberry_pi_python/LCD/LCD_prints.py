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
    
    def assignBatteryChar(self, battPercentage, charAddr):
        """Assigns special character to a given character address"""

        # Determine what the character should look like
        byteList = []
        for pixLevel in range(8):
            if battPercentage/(0.125*(pixLevel+1)) >= 1:
                byteList = [0x1f] + byteList
            else:
                # Determined shift by knowing how many pixels need light
                # One pixel is 2.5% (0.025) and one line is 12.5% (0.125)
                shiftBy = int((battPercentage % 0.125)//0.025)

                # shiftBy is the number of pixels to turn on
                # then bitwise & to only get last 5 bits
                byteList = [(0b1111100000 >> shiftBy) & 0x1f] + byteList
                for _ in range(7-pixLevel):
                    byteList = [0x00] + byteList
                break

        # set as a custom character
        self.lcd.custom_char(charAddr%8,bytearray(byteList))

    def printBatteryPercentageChar(self,battPercentage, charAddr=0):
        """Prints special character to display battery percentage.
        expects a floating point between 0 and 1"""

        self.assignBatteryChar(battPercentage,charAddr)

        # print character
        self.lcd.putchar(chr(charAddr%8))

    def printMockScreen(self,battAPerc=0.3,battBPerc=0.8):
        """Prints a mock screen of what the real screen will look like
        once all registers are properly connected."""
        self.lcd.clear()
        self.lcd.hide_cursor()
        self.lcd.move_to(0,0)

        self.assignBatteryChar(battAPerc,0)
        self.lcd.putstr(f"Battery A: {battAPerc*100}% {chr(0)}")

        self.lcd.move_to(0,1)
        self.assignBatteryChar(battBPerc,1)
        self.lcd.putstr(f"Battery B: {battBPerc*100}% {chr(1)}")

