import lgpio  # type: ignore
import time
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from typing import Any, Optional
from picamera2 import Picamera2, Preview, MappedArray

# GPIO Pins
GPIO_PIN_SERVO = 12
TRIGGER_PIN = 17
ECHO_PIN = 27
GPIO_PIN_DT = 2  # Data pin for HX711
GPIO_PIN_SCK = 3  # Clock pin for HX711
PWM_FREQUENCY = 50  # PWM frequency for servo

# Servo pulse width range (Min: 500µs for 0 degrees, Max: 2500µs for 180 degrees)
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500

# Calibration for load sensor
OFFSET = 8358603  # Calibration offset
ACTUAL_WEIGHT = 1  # Known weight for calibration
MEASURED_WEIGHT = 1734  # Measured weight (placeholder)
FACTOR = ACTUAL_WEIGHT / MEASURED_WEIGHT  # Calibration factor
MAX_MEASUREMENTS = 10

normalSize = (2304, 1296)  # Higher resolution with better FPS
lowresSize = (1536, 864)  # Lower resolution for processing speed

# Create a handle for the GPIO
handle = lgpio.gpiochip_open(0)  # type: ignore


# Servo control
def servo_write(angle: int) -> None:
    lgpio.gpio_claim_output(handle, GPIO_PIN_SERVO)  # type: ignore
    pulse_width = int(
        (angle / 90) * (SERVO_MAX_PULSE - SERVO_MIN_PULSE) + SERVO_MIN_PULSE
    )
    duty_cycle = (pulse_width / 20000) * 100
    lgpio.tx_pwm(handle, GPIO_PIN_SERVO, PWM_FREQUENCY, duty_cycle)  # type: ignore


def run_servo() -> None:
    try:
        print("Servo Motor: Rotating...")
        for pos in range(0, 91):
            servo_write(pos)
            time.sleep(0.015)
        for pos in range(90, -1, -1):
            servo_write(pos)
            time.sleep(0.015)
        lgpio.tx_pwm(handle, GPIO_PIN_SERVO, PWM_FREQUENCY, 0)  # type: ignore
    except KeyboardInterrupt:
        print("Servo Stopped")


# Measure Distance
def measure_distance():
    lgpio.gpio_claim_output(handle, TRIGGER_PIN)  # type: ignore
    lgpio.gpio_claim_input(handle, ECHO_PIN)  # type: ignore
    lgpio.gpio_write(handle, TRIGGER_PIN, 1)  # type: ignore
    time.sleep(0.00001)
    lgpio.gpio_write(handle, TRIGGER_PIN, 0)  # type: ignore

    start_time, end_time = None, None
    timeout = time.time() + 0.02  # 20ms timeout

    while lgpio.gpio_read(handle, ECHO_PIN) == 0:  # type: ignore
        start_time = time.time()
        if start_time > timeout:
            return None

    timeout = time.time() + 0.02
    while lgpio.gpio_read(handle, ECHO_PIN) == 1:  # type: ignore
        end_time = time.time()
        if end_time > timeout:
            return None

    if start_time and end_time:
        distance = (end_time - start_time) * 17150  # Convert time to distance
        return round(distance, 2)
    return None


# Read HX711 sensor data
def read_hx711_count() -> int:
    h = lgpio.gpiochip_open(0)  # type: ignore
    lgpio.gpio_claim_output(h, GPIO_PIN_SCK)  # type: ignore
    lgpio.gpio_claim_input(h, GPIO_PIN_DT)  # type: ignore
    lgpio.gpio_write(h, GPIO_PIN_SCK, 0)  # type: ignore

    timeout = time.time() + 1
    while lgpio.gpio_read(h, GPIO_PIN_DT) == 1:  # type: ignore
        if time.time() > timeout:
            lgpio.gpiochip_close(h)  # type: ignore
            raise TimeoutError("HX711 timeout waiting for ready signal")

    count = 0
    for _ in range(24):
        lgpio.gpio_write(h, GPIO_PIN_SCK, 1)  # type: ignore
        count = count << 1
        lgpio.gpio_write(h, GPIO_PIN_SCK, 0)  # type: ignore
        if lgpio.gpio_read(h, GPIO_PIN_DT) == 0:  # type: ignore
            count += 1

    lgpio.gpio_write(h, GPIO_PIN_SCK, 1)  # type: ignore
    count ^= 0x800000
    lgpio.gpio_write(h, GPIO_PIN_SCK, 0)  # type: ignore

    lgpio.gpiochip_close(h)  # type: ignore
    return count


def calculate_weight() -> float:
    total = 0
    try:
        for measure in range(1, MAX_MEASUREMENTS + 1):
            reading = read_hx711_count()
            total += reading
            weight = (reading - OFFSET) * FACTOR
            print(f"Measurement {measure}: Reading = {reading}, Weight = {weight:.2f}g")
            time.sleep(0.05)

        average = total / MAX_MEASUREMENTS
        avg_weight = (average - OFFSET) * FACTOR
        print(f"Average Measurement: {average}, Average Weight = {avg_weight:.2f}g")

        return avg_weight
    except TimeoutError as e:
        print(f"Error: {e}")
        return 0


# Object detection (TensorFlow Lite)
rectangles = []


def ReadLabelFile(file_path: str) -> dict[int, str]:
    with open(file_path, "r") as f:
        lines = f.readlines()
    ret = dict[int, str]()
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret


def DrawRectangles(request: str):
    with MappedArray(request, "main") as m:
        for rect in rectangles:
            print(rect)
            rect_start = (int(rect[0] * 2) - 5, int(rect[1] * 2) - 5)
            rect_end = (int(rect[2] * 2) + 5, int(rect[3] * 2) + 5)
            cv2.rectangle(m.array, rect_start, rect_end, (0, 255, 0, 0))
            if len(rect) == 5:
                text = rect[4]
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(
                    m.array,
                    str(text),
                    (int(rect[0] * 2) + 10, int(rect[1] * 2) + 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )


def InferenceTensorFlow(
    image: np.ndarray[Any, Any], model: str, label: Optional[str] = None
) -> None:
    global rectangles
    if label:
        labels = ReadLabelFile(label)
    else:
        labels = None

    interpreter = tflite.Interpreter(model_path=model, num_threads=4)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    height = input_details[0]["shape"][1]
    width = input_details[0]["shape"][2]
    floating_model = input_details[0]["dtype"] == np.float32

    rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    picture = cv2.resize(rgb, (width, height), interpolation=cv2.INTER_AREA)
    input_data = np.expand_dims(picture, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]["index"])
    class_id = int(output_data[0][0])  # Class ID
    confidence = output_data[0][1]  # Confidence score

    rectangles.append([0, 0, 0, 0, f"{class_id}: {confidence:.2f}"])
    return rectangles


def object_detection(
    label_file: str = "labels_custom.txt",
    model: str = "model_custom.tflite",
) -> None:
    picam2 = Picamera2()
    picam2.rotate = 90
    config = picam2.create_preview_configuration(
        main={"size": normalSize, "format": "XRGB8888"},
        lores={"size": lowresSize, "format": "YUV420"},
    )
    picam2.configure(config)
    picam2.start()

    stride = picam2.stream_configuration("lores")["stride"]

    while True:
        buffer = picam2.capture_buffer("lores")
        grey = buffer[: stride * lowresSize[1]].reshape((lowresSize[1], stride))

        rectangles = InferenceTensorFlow(grey, model, label_file)
        if rectangles and rectangles[0][4] == "no_bottle":
            print("No bottle detected in the image. Activating servo.")
            run_servo()
        time.sleep(1)

    picam2.stop()


# Main system logic
def run_system() -> None:
    try:
        print("System started...")
        while True:
            distance = measure_distance()
            load_weight = calculate_weight()

            print(
                f"Ultrasonic Distance: {distance} cm | Load Weight: {load_weight:.2f}g"
            )

            if distance is not None and distance < 10 and load_weight > 0:
                print("Bottle detected! Triggering object detection...")
                object_detection()  # Run object detection if bottle is detected
                time.sleep(1)
            else:
                print("No bottle detected or insufficient weight.")
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting gracefully...")
    finally:
        lgpio.gpiochip_close(handle)  # type: ignore
        print("GPIO resources released.")


if __name__ == "__main__":
    run_system()
