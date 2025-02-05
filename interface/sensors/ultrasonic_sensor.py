import lgpio # type: ignore
import time

# Define the GPIO pins connected to the ultrasonic sensor, Trigger and Echo
TRIGGER_PIN = 17  
ECHO_PIN = 27    

handle = lgpio.gpiochip_open(0) # type: ignore
lgpio.gpio_claim_output(handle, TRIGGER_PIN) # type: ignore
lgpio.gpio_claim_input(handle, ECHO_PIN) # type: ignore

# Function to measure the distance using the HC-SR04
def measure_distance():
    """
    Measure the distance using the HC-SR04 ultrasonic sensor.
    Send a trigger signal, measure the time taken for the echo signal to return,
    and calculate the distance based on the speed of sound (time * speed of sound).
    """
    lgpio.gpio_write(handle, TRIGGER_PIN, 0)  # type: ignore
    time.sleep(0.000002)  
    lgpio.gpio_write(handle, TRIGGER_PIN, 1)  # type: ignore
    time.sleep(0.00001)   
    lgpio.gpio_write(handle, TRIGGER_PIN, 0)  # type: ignore

    # Measure the time it takes for the Echo pin to go HIGH
    pulse_start = time.time()
    pulse_end = time.time()

    while lgpio.gpio_read(handle, ECHO_PIN) == 0: # type: ignore
        pulse_start = time.time()  

    while lgpio.gpio_read(handle, ECHO_PIN) == 1: # type: ignore
        pulse_end = time.time()  

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 343 m/s, so multiply by 17150 (cm/s)

    return distance

def run_ultrasonic_sensor():
    try:
        print("Ultrasonic Sensor: Starting...")
        while True:
            distance = measure_distance()  
            print(f"Distance: {distance:.2f} cm")
            time.sleep(1)  # Delay before taking the next measurement

    except KeyboardInterrupt:
        print("\nExiting gracefully...")

    finally:
        # Clean up and release the GPIO resources
        lgpio.gpiochip_close(handle) # type: ignore
        print("GPIO resources released.")


if __name__ == "__main__":
    run_ultrasonic_sensor()
    