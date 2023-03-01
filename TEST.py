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