def turn_on_led_test():
    from gpiozero import LED  # type: ignore

    led = LED(17)
    led.on()
    print("\rLED ON", end="")
