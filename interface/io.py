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
    import RPi.GPIO as GPIO
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
    import pigpio  # type: ignore
    import time

    # Initialize pigpio
    pi = pigpio.pi()  # type: ignore

    if not pi.connected:  # type: ignore
        print("Failed to connect to pigpio daemon.")
        exit()

    # Set the servo pulse range (500 to 2500 microseconds for MG995)
    pi.set_servo_pulsewidth(SERVO, 0)  # type: ignore Initialize to 0 (servo off)

    try:
        while True:
            # Move to 0 degrees (1 ms pulse)
            pi.set_servo_pulsewidth(SERVO, 1000)  # type: ignore
            time.sleep(2)

            # Move to 90 degrees (1.5 ms pulse)
            pi.set_servo_pulsewidth(SERVO, 1500)  # type: ignore
            time.sleep(2)

            # Move to 180 degrees (2 ms pulse)
            pi.set_servo_pulsewidth(SERVO, 2000)  # type: ignore
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Turn off the servo
        pi.set_servo_pulsewidth(SERVO, 0)  # type: ignore
        pi.stop()  # type: ignore
