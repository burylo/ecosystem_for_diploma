import RPi.GPIO as GPIO
import time

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

def servo_start(t):
    try:
        pwm.start(0)  # Запустити PWM з нульовим відсотком заповнення
        # Рух вперед з середньою швидкістю.
        # Діапазон швидкостей:
        #  5% мінімальна швидкість
        #  10% - максимальна
        #  0% - зупинка
        set_servo_speed(7)  
        while t != 0:
            time.sleep(1)  # Затримка на 1 секунду
            t -= 1
        else:
            set_servo_speed(0)  # Зупинити сервопривід

    except KeyboardInterrupt:
        pass

    finally:
        pwm.stop()
        GPIO.cleanup()