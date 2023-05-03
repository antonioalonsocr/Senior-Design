from machine import Pin

def get_button(buttonPin):
    return not buttonPin.value()


if __name__=="__main__":
    buttonPIN = 16

    button = Pin(buttonPIN, Pin.IN, Pin.PULL_UP)
    led = Pin("LED", Pin.OUT)

    while True:
        if get_button(button):
            led.on()
        else:
            led.off()