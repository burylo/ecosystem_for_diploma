from datetime import datetime, timedelta
import mysql_manager
from gpio import weight_sernsor
from gpio import servo

def activate_device():
    all_devices = mysql_manager.get_all_data()
    for data in all_devices:
        if (data[-1] == "on"):
            if isinstance(data[5], timedelta):
                current_time = datetime.now().replace(second=0, microsecond=0)
                if current_time == data[5]:
                    if data[8].lower == "feeder":
                        portion_weight = weight_sernsor()
                        servo.servo_start()
                        while portion_weight <= data[7]-30: # -30 Поправка на затримку
                            continue
                        else:
                            servo.servo_stop()  # Зупинити сервопривід
                else:
                    print("Not Now")
            else:
                print("Значення часу не є timedelta або час не вставнолено")
        else:
            print("Пристрій вимкнено")