import cv2
from typing import Any
import numpy as np

import tflite_runtime.interpreter as tflite
from picamera2 import Picamera2, Preview

normalSize = (2304, 1296)  # Higher resolution with better FPS
lowresSize = (1536, 864)  # Lower resolution for processing speed

bottle_detected = False
MODEL_PATH = "efficientnet_model.tflite"


def InferenceTensorFlow(image: np.ndarray[Any, Any]) -> None:
    """
    Perform inference using a TensorFlow Lite model on the given image.
    Args:
        image: The input image to perform inference on.
    Returns:
        None
    """
    global bottle_detected

    # Load TFLite model and allocate tensors.
    interpreter = tflite.Interpreter(model_path=MODEL_PATH, num_threads=4)
    interpreter.allocate_tensors()

    # Input details for the model
    input_details = interpreter.get_input_details()

    # Output details for the model
    output_details = interpreter.get_output_details()

    # Resize the image to the input shape of the model
    height = input_details[0]["shape"][1]
    width = input_details[0]["shape"][2]

    # Convert the image to RGB and resize it
    rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    picture = cv2.resize(rgb, (width, height), interpolation=cv2.INTER_AREA)

    # Normalize the image
    input_data = np.expand_dims(picture, axis=0)
    input_data = (np.float32(input_data) - 127.5) / 127.5

    # Set the input tensor
    interpreter.set_tensor(input_details[0]["index"], input_data)

    # Perform inference
    interpreter.invoke()

    # Get the output tensor and detect the class index
    detected_output = interpreter.get_tensor(output_details[0]["index"])
    detected_class_index = np.argmax(detected_output[0])

    print(
        f"Class: {detected_class_index}, Max: {detected_output[0][detected_class_index]}"
    )

    # Check if the detected class is a bottle
    if (
        detected_class_index == 898
        or detected_class_index == 720
        or detected_class_index == 647
    ):
        bottle_detected = True


def classify_image() -> None:
    """
    Perform image classification using a TensorFlow Lite model.
    Returns:
        None
    """
    global bottle_detected

    # Initialize the PiCamera to capture images and start the preview
    camera = Picamera2()
    camera.rotate = 90
    # camera.start_preview(Preview.QTGL)
    config = camera.create_preview_configuration(
        main={"size": normalSize, "format": "XRGB8888"},
        lores={"size": lowresSize, "format": "YUV420"},
    )
    camera.configure(config)
    stride = camera.stream_configuration("lores")["stride"]

    camera.start()

    # Capture images and perform inference, if a bottle is detected, stop the camera and return
    try:
        while True:
            if bottle_detected:
                camera.stop()
                return
            buffer = camera.capture_buffer("lores")
            grey_image = buffer[: stride * lowresSize[1]].reshape(
                (lowresSize[1], stride)
            )
            _ = InferenceTensorFlow(grey_image)
    finally:
        camera.close()


if __name__ == "__main__":
    classify_image()
