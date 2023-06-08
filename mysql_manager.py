import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('HOST')
USER = os.getenv('MYSQL_USER')
PASSWORD = os.getenv('MYSQL_PASSWORD')
DATABASE = os.getenv('MYSQL_DATABASE')

def db_connect():
    # Зʼєднання з базою даних
    return mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)

if (db_connect().is_connected()):
    print("Connected")
else:
    print("Not connected")

# Запит INSERT
def incert_into_table(name, desc, conn_type, period, time_start, time_end, weight, device_type):
    db = db_connect()
    # Створення курсора
    cursor = db.cursor()
    query = "INSERT INTO Devices (Name, Description, ConnectionType, Period, TimeCountStart, TimeCountEnd, Weight, device_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    # Значення, які ви хочете записати
    data = (name, desc, conn_type, period, time_start, time_end, weight, device_type)

    # Виконання запиту
    cursor.execute(query, data)

    # Підтвердження змін
    db.commit()
    cursor.close()
    db.close()

def get_all_data():
    db = db_connect()
    # Створення курсора
    cursor = db.cursor()
    # Виконання запиту
    query = "SELECT * FROM Devices"
    cursor.execute(query)

    # Отримання результатів
    results = cursor.fetchall()

    # Закриття курсора та зʼєднання
    cursor.close()
    db.close()
    return results
    for row in results:
    # Опрацьовування кожного рядка
        print(row)
    

def get_device_data(row_id):
    db = db_connect()
    # Створення курсора
    cursor = db.cursor()
    # Виконання запиту
    query = "SELECT * FROM Devices WHERE ID = %s"
    cursor.execute(query, (row_id,))

    # Отримання результатів
    results = cursor.fetchall()

    # Закриття курсора та зʼєднання
    cursor.close()
    db.close()
    return results
    
    for row in results:
    # Опрацьовування кожного рядка. Для тестів
        print(row)

def delete_row(row_id):
    db = db_connect()
    cursor = db.cursor()

    # Видалення рядка з таблиці
    query = "DELETE FROM Devices WHERE ID = %s"

    # Виконання запиту
    cursor.execute(query, (row_id,))

    # Підтвердження змін
    db.commit()
    cursor.close()
    db.close()

def chage_data(row_id, column_name, new_value):
    db = db_connect()
    cursor = db.cursor()

    # SQL запит для зміни значень елементу
    sql = "UPDATE Devices SET {}=%s WHERE id=%s"
    # Виконання SQL запиту з параметрами
    cursor.execute(sql.format(column_name), (new_value, row_id))

    # Підтвердження змін в базі даних
    db.commit()

    # Закриття курсора та з'єднання з базою даних
    cursor.close()
    db.close()


# incert_into_table("Feeder", "Living Room", "GPIO", 0, "", "", 0)
# get_device_data(4)
# get_all_data()
# chage_data(1, "ConnectionType", "GPIO")


