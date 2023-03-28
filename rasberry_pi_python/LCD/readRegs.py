class readRegs:
    def __init__(self, i2c):
        """Initialize object"""
        self.i2c = i2c
    
    def readfrom_mem(self,addr,memaddr,nbytes,addrsize):
        """Reads defined register and returns list with 8bit-ints of size nbytes"""
        bstring = self.i2c.readfrom_mem(addr,memaddr,nbytes,addrsize=addrsize)
        return [bstring[i] for i in range(nbytes)]
    
    def readRepSOC(self,addr=0x36,memaddr=0x06,nbytes=2,addrsize=8):
        data = self.readfrom_mem(addr,memaddr,nbytes,addrsize)
        return ((data[1] << 8) + data[0])/256
