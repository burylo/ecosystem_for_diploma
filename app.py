from flask import Flask, render_template, url_for, request, redirect
from flask_apscheduler import APScheduler
from datetime import datetime
import mysql_manager
# import time_checker

app = Flask(__name__)

scheduler = APScheduler()

# Налаштування планувальника
app.config['SCHEDULER_API_ENABLED'] = True
app.config['JOBS'] = [
    {
        'id': 'check_device',
        'func': print("Hello there"), # time_checker.activate_device(),
        'trigger': 'interval',
        'seconds': 60  # Частота виконання функції (у цьому випадку кожну хвилину)
    }
]

@app.route('/', methods=['POST', 'GET'])
def index():
    data = mysql_manager.get_all_data()
    # print(data)
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

@app.route('/previous')
def back_to_main():
    # Використовуємо функцію `redirect` для переадресації на попередню сторінку
    return redirect(url_for('index'))

@app.route('/new_device_config')
def new_device_config():
    data = request.args.get('device') # Отримати значення параметру 'device' з URL
    # print(data)
    return render_template('config_new.html', device=data)

@app.route('/device_config', methods=['POST', 'GET'])
def device_config():
    device_id = request.args.get('device_id') # Отримати значення параметру 'device_id' з URL
    device_info = mysql_manager.get_device_data(device_id)[0]
    # print(device_info)
    name = device_info[1]
    desc = device_info[2]
    conn_type = device_info[3].lower()
    period = str(device_info[4])
    time_start = str(device_info[5])[:-3] # Обрізаємо секунди
    if len(time_start) < 5:
        time_start='0'+time_start 
    time_end = device_info[6]
    weight = device_info[7]
    device = device_info[8]
    status = device_info[9]
    print(name, desc, conn_type, period, time_start, time_end, weight, device, status)
    
    return render_template('config_device.html', 
                           device_id=device_id, 
                           name=name, 
                           desc=desc, 
                           conn_type=conn_type,
                           period=period,
                           time_start=time_start,
                           weight=weight, 
                           device=device)

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
        device = request.form.get('device-type')
        status = request.form.get('device-status')
        # Записуємо дані в базу даних
        
        mysql_manager.incert_into_table(name, desc, conn_type, period, time_start, time_end, weight, device, status)
        print(name, desc, conn_type, period, time_start, time_end, weight, device, status)
        print("DATA WAS SENDED")
        return redirect(url_for('index'))
    else:
        print("DATA NOT SENDED")

@app.route('/replace_data_form', methods=['POST', 'GET'])
def replace_data_form():
    if request.method == "POST":
        device_id = request.form.get('device-id') # Отримати значення параметру 'device_id' з URL
        # Отримуємо дані з форми
        name = request.form.get('device-name')
        desc = request.form.get('device-desc')
        conn_type = request.form.get('connection-type')
        period = int(request.form.get('delay-time').split('_')[1])
        time_start = request.form.get('start-time')
        time_end = ""
        weight = request.form.get('portion-mass')
        device = request.form.get('device-type')
        # Записуємо дані в базу даних
        print(device_id, name, desc, conn_type, period, time_start, time_end, weight)
        mysql_manager.update_data(device_id, name, desc, conn_type, period, time_start, time_end, weight)
        print("DATA WAS SENDED")
        return redirect(url_for('index'))
    else:
        print("DATA NOT SENDED")

@app.route('/toggle_switch', methods=['POST', 'GET'])
def toggle_switch():
    status = request.form.get('status')
    device_id = request.form.get('blockId')
    mysql_manager.device_status(device_id, status)
    print("Device №" + device_id + " is " + status + " now")
    return 'Status is ' + status + ' now'

@app.route('/delete_device', methods=['POST', 'GET'])
def delete_device():
    device_id = request.form.get('blockId')
    mysql_manager.delete_row(device_id)
    print(device_id)
    return 'Block' + device_id + 'was deleted'

if __name__ == "__main__":
    app.run(debug=True)