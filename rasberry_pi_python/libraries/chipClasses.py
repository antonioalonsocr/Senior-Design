class Chip:
    def __init__(self, i2c):
        """Initialize object"""
        self.i2c = i2c

    def readfrom_mem(self,addr,memaddr,nbytes,addrsize=8):
        """Reads defined register and returns list with 8bit-ints of size nbytes"""
        # If address starts with 0, addr=0x36 if 1 then addr=0x0B
        bstring = self.i2c.readfrom_mem(addr,memaddr,nbytes,addrsize=addrsize)
        return [bstring[i] for i in range(nbytes)]
    
    def twos_comp(self,data):
        if data > 0x7FFF:
            return (data - 0xFFFF)
        else:
            return data
        

class Max17330(Chip):
    def __init__(self,i2c):
        super().__init__(i2c)
    
    def readRepSOC(self,addr=0x36):
        data = self.readfrom_mem(addr=addr,memaddr=0x06,nbytes=2)
        return ((data[1] << 8) + data[0])/256
    
    def readCurrentReg(self,addr=0x36):
        data = self.readfrom_mem(addr=addr,memaddr=0x1C,nbytes=2) #0x1C
        data = self.twos_comp((data[1] << 8) + data[0])
        return data*0.15625
    
    def readAvgVolt(self,addr=0x36):
        data = self.readfrom_mem(addr=addr,memaddr=0xDB,nbytes=2) #0x1A Vcell reg, 0x2A avg, 0x19 avgVcell
        #print(data)
        #return ((data[1] << 8) + data[0])*(7.8125*1e-5)
        return ((data[1] << 8) + data[0])*(0.0003125)
    
    def readAvgCurr(self,addr=0x36):
        data = self.readfrom_mem(addr=addr,memaddr=0x1D,nbytes=2) #0x28 chgcurr reg
        data = self.twos_comp((data[1] << 8) + data[0])
        return data*0.15625
    
    def unlockWP(self,addr=0x36):
        data = self.readfrom_mem(addr=addr,memaddr=0x61,nbytes=2)
        bstring = bytearray()
        bstring.extend(chr(0x0) + chr(0x0))
        self.i2c.writeto_mem(addr,0x61,bstring)
        self.i2c.writeto_mem(addr,0x61,bstring)
        
    def ParEN(self,addr=0x36):
        #print("ParEN")
        data = self.readfrom_mem(addr=addr,memaddr=0xB5,nbytes=2)
        #print(data)
        bstring = bytearray()
        bstring.extend(chr(data[0]|0x2) + chr(data[1]))   # original data[0]&0x5
        #print(bstring)
        self.i2c.writeto_mem(addr,0xB5,bstring)
        #print(self.readfrom_mem(addr=addr,memaddr=0xB5,nbytes=2))
        
    def AllowChgB(self,addr=0x36):
        #print("protAlrt")
        bstring1 = bytearray()
        bstring1.extend(chr(0x0) + chr(0x0))
        #print(bstring1)
        self.i2c.writeto_mem(addr,0xAF,bstring1)
        #print(self.readfrom_mem(addr=addr,memaddr=0xAF,nbytes=2))
        
        #print("chgB")
        data = self.readfrom_mem(addr=addr,memaddr=0x0,nbytes=2)
        #print(data)
        bstring2 = bytearray()
        bstring2.extend(chr(data[0]&0xDF) + chr(data[1]&0x0))
        #print(bstring2)
        self.i2c.writeto_mem(addr,0x0,bstring2)
        #print(self.readfrom_mem(addr=addr,memaddr=0x0,nbytes=2))
    
class Max77958(Chip):
    def __init__(self,i2c):
        super().__init__(i2c)
