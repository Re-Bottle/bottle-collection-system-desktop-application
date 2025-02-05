import lgpio # type: ignore
import time

# Initialize the GPIO and the servo control pin
GPIO_PIN = 12 
PWM_FREQUENCY = 50         # PWM frequency in Hz

# Servo pulse width range (Min: 500µs for 0 degrees, Max: 2500µs for 180 degrees)
SERVO_MIN_PULSE = 500      
SERVO_MAX_PULSE = 2500 

# Create a handle for the GPIO and set the pin as output
handle = lgpio.gpiochip_open(0) # type: ignore
lgpio.gpio_claim_output(handle, GPIO_PIN) # type: ignore

# Function to generate PWM signal using tx_pwm
def servo_write(angle: int) -> None:
    """
    Generate a PWM signal to control the servo motor position.
    Map the angle (0-90) to a pulse width (500 to 2500 microseconds).
    Calculate the duty cycle based on 20ms period as a percentage and generate the PWM signal.
    """
    pulse_width = int((angle / 90) * (SERVO_MAX_PULSE - SERVO_MIN_PULSE) + SERVO_MIN_PULSE)
    duty_cycle = (pulse_width / 20000) * 100
    lgpio.tx_pwm(handle, GPIO_PIN, PWM_FREQUENCY, duty_cycle) # type: ignore

def run_servo():
    try:
        print("Servo Motor: Starting...")
        # Rotate from 0° to 90° and back to 0° 2 times with small delay
        for _ in range(2):  
            for pos in range(0, 91):
                servo_write(pos)
                time.sleep(0.015)
            
            for pos in range(90, -1, -1):
                servo_write(pos)
                time.sleep(0.015)

    except KeyboardInterrupt:
        print("\nExiting gracefully...")

    finally:
        # Clean up and release the GPIO resources
        lgpio.gpiochip_close(handle) # type: ignore


if __name__ == "__main__":
    run_servo()