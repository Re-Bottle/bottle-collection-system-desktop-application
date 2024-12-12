def capture_image():
    from picamera2 import Picamera2, Preview  # type: ignore
    import time

    picam2 = Picamera2()  # type: ignore
    camera_config = picam2.create_preview_configuration()  # type: ignore
    picam2.configure(camera_config)  # type: ignore
    picam2.start_preview(Preview.QTGL)  # type: ignore
    picam2.start()  # type: ignore
    time.sleep(2)
    picam2.capture_file("capture.jpg")  # type: ignore
