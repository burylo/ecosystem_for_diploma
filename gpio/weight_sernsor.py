import RPi.GPIO as GPIO
import time
from .hx711 import HX711 as HX711

# Ініціалізація GPIO
GPIO.setmode(GPIO.BCM)

# Конфігурація пінів HX711
HX711_DAT_PIN = 23
HX711_CLK_PIN = 24

def change_dat_pin(d_pin):
    HX711_DAT_PIN = d_pin

def change_clk_pin(c_pin):
    HX711_clk_PIN = c_pin

# Створення об'єкту HX711
hx711 = HX711(HX711_DAT_PIN, HX711_CLK_PIN)
hx711.set_reading_format("MSB", "MSB")

# Калібрування
hx711.set_reference_unit(92)  # Встановлення одиниці виміру 1 грам
def get_weight():
    # Запуск HX711
    hx711.power_down()
    hx711.power_up()
    # Відтарування
    hx711.tare()
    # Зчитування ваги
    weight = hx711.get_weight()
    # Затримка
    time.sleep(0.1)
    hx711.power_down()
    # Повернення значення ваги
    return(weight)