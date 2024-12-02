import RPi.GPIO as GPIO  # import RPi.GPIO module

LED = 11  # pin no. as per BOARD, GPIO18 as per BCM

GPIO.setwarnings(False)  # disable warnings
GPIO.setmode(GPIO.BOARD)  # set pin numbering format
GPIO.setup(LED, GPIO.OUT)  # set GPIO as output


# Turn ON LED
def turn_on_led_test():
    GPIO.output(LED, GPIO.HIGH)
