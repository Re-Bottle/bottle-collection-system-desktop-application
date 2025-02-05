import lgpio # type: ignore
import time

# Define the GPIO pin connected to the IR sensor signal
GPIO_PIN = 17 

# Create a handle for the GPIO chip (handle 0 is the first GPIO chip)
handle = lgpio.gpiochip_open(0) # type: ignore

# Set the GPIO pin as input (IR sensor output is digital HIGH/LOW)
lgpio.gpio_claim_input(handle, GPIO_PIN)  # type: ignore

# Function to read the IR sensor value
def read_ir_sensor() -> int:
    '''
    Read the value of the IR sensor (HIGH or LOW) and return it
    '''
    value = lgpio.gpio_read(handle, GPIO_PIN) # type: ignore
    return value # type: ignore

def run_ir_sensor():
    try:
        print("IR Sensor Reader: Starting...")
        while True:
            sensor_value = read_ir_sensor()  # Read the sensor
            if sensor_value == 0:
                print(f"IR Sensor: Object detected")
            else:
                print(f"IR Sensor: No object detected")
            
            time.sleep(0.5)  # Delay before reading again
            
    except KeyboardInterrupt:
        print("Exiting Gracefully...")
        
    finally:
        # Clean up and release the GPIO resources
        lgpio.gpiochip_close(handle) # type: ignore

if __name__ == "__main__":
    run_ir_sensor()