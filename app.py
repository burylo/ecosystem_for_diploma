from flask import Flask, render_template, url_for, request, redirect
import configparser
from datetime import datetime
# My Libs
import mysql_manager

app = Flask(__name__)

def edit_config(section_name, key, value):
    edit = configparser.ConfigParser()
    edit.read('configfile.ini')
    edit[section_name][key] = value
     # Write the new structure to the new file
    with open("configfile.ini", 'w') as configfile:
        edit.write(configfile)


# Read config.ini file
def get_data(value):
    config_obj = configparser.ConfigParser()
    config_obj.read("configfile.ini")
    return config_obj["test"][value]

@app.route('/', methods=['POST', 'GET'])
def index():
    data = mysql_manager.get_all_data()
    print(data)
    return render_template("index.html", data=data)

# Перехід на сторінку додавання пристрою
@app.route('/add_devices', methods=['POST', 'GET'])
def add_devices():
    return render_template("add_device.html")

# Опрацювання сторінки 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/previous')
def back_to_device_list():
    # Використовуємо функцію `redirect` для переадресації на попередню сторінку
    return redirect(url_for('add_devices'))

@app.route('/device_config')
def device_config():
    data = request.args.get('device') # Отримати значення параметру 'paragraph' з URL
    print(data)
    return render_template('config_new.html', data=data)

@app.route('/process_form', methods=['POST', 'GET'])
def process_form():
    if request.method == "POST":
        # Отримуємо дані з форми
        name = request.form.get('device-name')
        desc = request.form.get('device-desc')
        conn_type = request.form.get('connection-type')
        period = int(request.form.get('delay-time').split('_')[1])
        time_start = request.form.get('start-time')
        time_end = ""
        weight = request.form.get('portion-mass')
        # Записуємо дані в базу даних
        
        mysql_manager.incert_into_table(name, desc, conn_type, period, time_start, time_end, weight)
        print(name, desc, conn_type, period, time_start, time_end, weight)
        print("DATA WAS SENDED")
        return redirect(url_for('index'))
    else:
        print("DATA NOT SENDED")

@app.route('/delete_device', methods=['POST', 'GET'])
def delete_device():
    device_id = request.form.get('blockId')
    mysql_manager.delete_row(device_id)
    print(device_id)
    return 'Block' + device_id + 'was deleted'

@app.route('/config', methods=['POST', 'GET'])
def config():
    if request.method == "POST":
        user_name =  request.form["user"]
        edit_config('test', 'user', user_name) 
        return render_template("config.html", usr=get_data("user"), host=get_data("host"))
    else:
        return render_template("config.html", usr=get_data("user"), host=get_data("host"))

if __name__ == "__main__":
    app.run(debug=True)