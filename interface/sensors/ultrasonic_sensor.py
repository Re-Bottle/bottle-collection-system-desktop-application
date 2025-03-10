import lgpio  # type: ignore
import time

# Define GPIO pins
TRIGGER_PIN = 17
ECHO_PIN = 27

# Initialize GPIO
handle = lgpio.gpiochip_open(0)  # type: ignore
lgpio.gpio_claim_output(handle, TRIGGER_PIN)  # type: ignore
lgpio.gpio_claim_input(handle, ECHO_PIN)  # type: ignore


def measure_distance():
    """
    Measure the distance using the HC-SR04 ultrasonic sensor.
    """
    # Send a 10µs pulse to trigger the sensor
    lgpio.gpio_write(handle, TRIGGER_PIN, 1)  # type: ignore
    time.sleep(0.00001)
    lgpio.gpio_write(handle, TRIGGER_PIN, 0)  # type: ignore

    # Measure the time for the echo signal
    start_time, end_time = None, None

    timeout = time.time() + 0.02  # 20ms timeout
    while lgpio.gpio_read(handle, ECHO_PIN) == 0:  # type: ignore
        start_time = time.time()
        if start_time > timeout:
            return None  # Timeout handling

    timeout = time.time() + 0.02
    while lgpio.gpio_read(handle, ECHO_PIN) == 1:  # type: ignore
        end_time = time.time()
        if end_time > timeout:
            return None  # Timeout handling

    if start_time and end_time:
        distance = (end_time - start_time) * 17150  # Speed of sound calculation
        return round(distance, 2)  # Return rounded distance
    return None  # Return None if measurement failed


def run_ultrasonic_sensor():
    print("Ultrasonic Sensor: Starting...")
    try:
        while True:
            distance = measure_distance()
            if distance is not None:
                print(f"Distance: {distance:.2f} cm")
                if distance < 100:
                    print("Object detected!")
            else:
                print("Measurement timeout or failed.")

            time.sleep(0.5)  # Adjustable delay for measurement frequency

    except KeyboardInterrupt:
        print("\nExiting gracefully...")

    finally:
        # Ensure GPIO is released
        lgpio.gpiochip_close(handle)  # type: ignore
        print("GPIO resources released.")


if __name__ == "__main__":
    run_ultrasonic_sensor()
