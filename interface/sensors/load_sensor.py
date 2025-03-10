import lgpio  # type: ignore
import time


def read_hx711_count(gpio_pin_dt=2, gpio_pin_sck=3):  # type: ignore
    """
    Reads raw data from the HX711 ADC.
    Args:
        gpio_pin_dt: Data pin (DT) for the HX711
        gpio_pin_sck: Clock pin (SCK) for the HX711

    Returns:
        A raw count value from the HX711
    """
    h = lgpio.gpiochip_open(0)  # type: ignore # Open GPIO chip 0

    # Configure pins
    lgpio.gpio_claim_output(h, gpio_pin_sck)  # type: ignore
    lgpio.gpio_claim_input(h, gpio_pin_dt)  # type: ignore
    lgpio.gpio_write(h, gpio_pin_sck, 0)  # type: ignore

    # Wait until DT pin is low (HX711 ready signal)
    timeout = time.time() + 1  # Timeout after 1 second
    while lgpio.gpio_read(h, gpio_pin_dt) == 1:  # type: ignore
        if time.time() > timeout:
            lgpio.gpiochip_close(h)  # type: ignore
            raise TimeoutError("HX711 timeout waiting for ready signal")

    count = 0
    for _ in range(24):
        lgpio.gpio_write(h, gpio_pin_sck, 1)  # type: ignore
        count = count << 1
        lgpio.gpio_write(h, gpio_pin_sck, 0)  # type: ignore
        if lgpio.gpio_read(h, gpio_pin_dt) == 0:  # type: ignore
            count += 1

    # Set the gain and prepare for next conversion
    lgpio.gpio_write(h, gpio_pin_sck, 1)  # type: ignore
    count ^= 0x800000  # Apply two's complement for 24-bit signed value
    lgpio.gpio_write(h, gpio_pin_sck, 0)  # type: ignore

    lgpio.gpiochip_close(h)  # Close the GPIO chip # type: ignore
    return count


def run_load_sensor():
    offset = 8358603  # Offset for calibration
    actual_weight = 1  # Known weight for calibration
    measured_weight = 1734  # Placeholder for measured weight
    factor = actual_weight / measured_weight  # Calibration factor
    max_measurements = 10
    total = 0

    try:
        for measure in range(1, max_measurements + 1):
            reading = read_hx711_count()
            total += reading
            weight = (reading - offset) * factor
            print(f"{measure}\tMeasure\t{reading}\tWeight\t{weight:.2f}")
            time.sleep(0.05)  # 50ms delay

        average = total / max_measurements
        avg_weight = (average - offset) * factor
        print(f"Average\tMeasure\t{average}\tWeight\t{avg_weight:.2f}")

    except TimeoutError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_load_sensor()
