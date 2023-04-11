class Chip:
    def __init__(self, i2c):
        """Initialize object"""
        self.i2c = i2c

    def readfrom_mem(self,addr,memaddr,nbytes,addrsize=8):
        """Reads defined register and returns list with 8bit-ints of size nbytes"""
        # If address starts with 0, addr=0x36 if 1 then addr=0x0B
        bstring = self.i2c.readfrom_mem(addr,memaddr,nbytes,addrsize=addrsize)
        return [bstring[i] for i in range(nbytes)]

class Max17330(Chip):
    def __init__(self,i2c):
        super().__init__(self,i2c)
    
    def readRepSOC(self,addr=0x36):
        data = self.readfrom_mem(addr=addr,memaddr=0x06,nbytes=2,addrsize=8)
        return ((data[1] << 8) + data[0])/256
    
    def readCurrentReg(self,addr=0x36):
        data = self.readfrom_mem(addr=addr,memaddr=0x1C,nbytes=2,addrsize=8)
        return data

        
    
class Max77958(Chip):
    def __init__(self,i2c):
        super().__init__(self,i2c)