import RPi.GPIO as GPIO

servo_pin = 18

def change_servo_pin(s_pin):
    servo_pin = s_pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)

def set_servo_speed(speed):
    # Перетворити відсоток швидкості в duty cycle
    duty = speed / 10.0 + 5.0
    pwm.ChangeDutyCycle(duty)

def servo_start():
    try:
        pwm.start(0)  # Запустити PWM з нульовим відсотком заповнення
        # Рух вперед з середньою швидкістю.
        # Діапазон швидкостей:
        #  5% мінімальна швидкість
        #  10% - максимальна
        #  0% - зупинка
        set_servo_speed(7)  

    except KeyboardInterrupt:
        pass

def servo_stop():
    try:
        set_servo_speed(0)  # Зупинити сервопривід
    finally:
        pwm.stop()
        GPIO.cleanup()