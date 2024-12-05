def turn_on_led_test():
    from gpiozero import LED  # type: ignore

    led = LED(17)  # type: ignore in windows
    led.on()  # type: ignore in windows
    print("\rLED ON", end="")
