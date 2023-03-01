def printBatt(batt): 
    byteList = [] 
    for pixLevel in range(8):
        if batt/(0.125*(pixLevel+1)) >= 1:
            byteList = [0x1f] + byteList
        else:
            byteList = [(0b1111100000 >> int((batt % 0.125)//0.025)) & 0x1f] + byteList
            for i in range(7-pixLevel):
                byteList = [0x00] + byteList
            break
    print(byteList)
    for elem in byteList:
        print(bin(elem))

if __name__ == "__main__":
    printBatt(0.87)