import smbus2 as smbus
import time
import machine as m
import inspect

bus=smbus.SMBus(1)
#sa = 0x36 slave address
class MAX17330(object):     #object):   #Gpib in raspberry pi

    def __init__(self,sa=0x36,rsns=10,verbose=True):       #Schematic has Pin 13 for MAX17330_1, 15 for MAX17330_2
        self.verbose=verbose
        self.sa=sa
        self.sa2={0x36:0x0b,0x72:0x4f,0x32:0x0f,0x76:0x4b}[sa]
        self.rsns=rsns
        try:
            bus.write_quick(sa)
            print("Received ACK at {}".format(hex(sa)))
        except:
            print("Did not receive ACK at {}".format(hex(sa)))
        try:
            bus.write_quick(self.sa2)
            print("Received ACK at {}".format(hex(self.sa2)))
        except:
            print("Did not receive ACK at {}".format(hex(self.sa2)))

    def r(self,reg,sa,h=True):
        data=bus.read_byte_data(sa,reg)
        if h:
            return hex(data)
        else:
            return data

    def w(self,reg,data,sa):
        return bus.write_byte_data(sa,reg,data)

    def rw(self,reg,sa,l=1):
        if l==1:
            data=bus.read_word_data(sa,reg)
        else:
            data=[]
            temp_data=bus.read_i2c_block_data(sa,reg,l*2)
            for i in range(len(temp_data)):
                if i % 2 == 1:
                    data.append(temp_data[i]<<8 | temp_data[i-1])
        return data

    def ww(self,reg,data,sa):
        return bus.write_word_data(sa,reg,data)

    def unlock_WP(self):
        self.ww(0x61,0x0,self.sa)
        self.ww(0x61,0x0,self.sa)
    def lock_WP(self):
        prev_val = self.rw(0x61,self.sa)
        val = (prev_val & 0xFF07) | 0xF8
        self.ww(0x61,val,self.sa)
    
    def get_vcell(self):
        data=self.rw(0x1A,self.sa)
        return data * 0.000078125
    
    def get_vpckp(self):
        data = self.rw(0xdb,self.sa)
        return data * 0.0003125
    def get_ibatt(self):
        return self.twos_comp(self.rw(0x1C,self.sa))*0.15625*10/self.rsns
    def get_ichg(self):
        return self.twos_comp(self.rw(0x28,self.sa))*0.15625*10/self.rsns

    def is_dropout(self):
        if (self.rw(0xa3,self.sa) & 0x8000) >0:
            return True
        else:
            return False
    def set_VChg(self,VChg):
        self.unlock_WP()
        if type(VChg)==float:
            VChg=min(127,max(-128,int(round((VChg- 4.2)/0.005,0))))
            print("VChg = {}".format(hex(VChg)))
        prev_val = self.rw(0xD9,self.sa2)
        self.ww(0xd9,((prev_val & 0xFF)|(VChg <<8)),self.sa2)
        self.lock_WP()
        return self.rw(0xD8,self.sa2)

    def set_IChg(self,IChg):
        self.unlock_WP()
        self.ww(0xdb,0xff00,self.sa2)       #Disable Step Charge
        prev_val = self.rw(0xD8,self.sa2)
        self.ww(0xd8,((prev_val & 0xFF)|((IChg-1) <<8)),self.sa2)           #fix 10 mA offset issue
        return self.rw(0xD8,self.sa2)
        self.lock_WP()
    def read_hchg_regs(self):
        data=self.rw(0x75,self.sa,l=8)
        return data


    def twos_comp(self,data):
        if data>0x7FFF:
            return data - 0xffff
        else:
            return data
    def reg_list(self):
        reg_arr=[]
        for x in range(256):
            reg_arr.append("{}:{}".format(hex(self.sa),hex(x)))
        for x in range(256):
            reg_arr.append("{}:{}".format(hex(self.sa2),hex(x)))
        return reg_arr
    def read_line(self):
        data = []
        for x in range(256):
            data.append(self.rw(x,self.sa))
        for x in range(256):
            data.append(self.rw(x,self.sa2))
        return data
    def load_RAM_ini(self,fname):
        data_arr=[]
        with open(fname,'r') as f:
            for line in f:
                if "//" in line:
                    data=line.split(" = ")
                    reg=int(data[0],16)-256
                    val=int(data[1].split("\t")[0],16)
                    if not (reg in [0xb5,0xbc,0xbd,0xbe,0xbf]):
                        self.ww(reg,val,self.sa2)
            self.ww(0xAB,self.rw(0xab,self.sa)|0x8000,self.sa)
            while(self.rw(0xab,self.sa)&0x8000 == 0x8000):
                time.sleep(0.010)


###############################################################


chg=MAX17330(0x36)
tstart = time.time()
reads=0
# for x in range(300):
#     print(",".join(map(str,[chg.rw(0x79,chg.sa),chg.rw(0x7c,chg.sa)]+chg.read_hchg_regs()))+"\n")
#     reads +=1
#     if time.time() - 1 > tstart:
#         print("{} Reads in 1 second".format(reads))
#         reads=0
#         tstart = time.time()
chg.rw(0x79,chg.sa)