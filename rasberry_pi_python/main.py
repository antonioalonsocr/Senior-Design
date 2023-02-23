import machine as m
import utime

led = machine.Pin(25, machine.Pin.OUT); #By default the LED is pin 25

convertion_factor = 3.3/65535  #The convertion factor of 16 bits

p0 = m.Pin(0, m.Pin.OUT); #This initiallizes the pin #0 as an output pin

adc = m.ADC(26); #variable adc is assigned to the ADC pin 26

while True:

    reading = adc.read_u16(); #reading is equal to the variable adc defined as pin 26
    print("ADC raw value: ", reading);
    voltage = reading*convertion_factor;
    print("Voltage: ", voltage);
    utime.sleep(0.5);
    
    
    
