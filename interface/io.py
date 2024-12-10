# Devices:
# - Load Cell
# - SERVO: red - power, brown - ground,
# - IR Sensor

# Load Cell
DT = 17  # Change based on your wiring
SCK = 27  # Change based on your wiring
# RED VCC 5V, BLACK GROUND

# Servo
SERVO = 13
# BROWN GROUND, RED 5V


def turn_on_led_test():
    from gpiozero import LED  # type: ignore

    led = LED(17)  # type: ignore in windows
    led.on()  # type: ignore in windows
    print("\rLED ON", end="")


def read_load_cell_data():
    import RPi.GPIO as GPIO  # type: ignore
    from hx711 import HX711  # type: ignore

    # Setup HX711
    hx = HX711(dout_pin=DT, pd_sck_pin=SCK)  # type: ignore

    def clean_and_exit():
        print("Cleaning up...")
        GPIO.cleanup()
        print("Bye!")
        exit()

    try:
        # Start HX711 and calibrate
        print("Initializing...")
        hx.reset()  # type: ignore
        hx.set_scale_ratio(1)  # type: ignore
        hx.tare()  # type: ignore

        while True:
            value = hx.get_weight_mean(10)  # type: ignore Read average of 10 samples
            print(f"Weight: {value} grams")
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()


def control_servo():
    from gpiozero import Servo  # type: ignore
    from time import sleep
    from gpiozero.pins.rpigpio import RPiGPIOFactory  # type: ignore
    import RPi.GPIO as GPIO  # type: ignore

    # Set up GPIO pin for the servo
    GPIO.setmode(GPIO.BCM)
    factory = RPiGPIOFactory()  # type: ignore
    servo = Servo(SERVO, pin_factory=factory)  # type: ignore

    # Sweep the servo back and forth
    while True:
        for position in range(
            -100, 101, 10
        ):  # Move from -100 (full left) to 100 (full right)
            servo.value = (
                position / 100.0
            )  # Map -100 to 100 range to -1 to 1 for servo control
            sleep(0.5)
