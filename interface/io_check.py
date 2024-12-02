from gpiozero import LED  # type: ignore
from time import sleep

led = LED(17)

while True:
    led.on()
    print("\rLED ON", end="")
    sleep(1)
    led.off()
    print("\rLED OFF", end="")
    sleep(1)
