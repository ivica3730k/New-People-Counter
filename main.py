import datetime
import threading
import time
import config as conf
import writer as writer
from flask import Flask, render_template, request
app = Flask(__name__)
 
ARDUINO_COM_PORT = conf.ARDUINO_COM_PORT
ARDUINO_BAUD_RATE = conf.ARDUINO_BAUD_RATE

data = writer.load_obj("data.data")

def write_visits(num_data = 0):
    if num_data == 0:
        return
    current_day = datetime.datetime.now()
    current_day = current_day.replace(hour=0,minute=0, second=0, microsecond=0).date()
    current_time = datetime.datetime.now()
    current_time = current_time.replace(minute=0, second=0, microsecond=0).time()
    try:
        data[current_day]
    except KeyError:
        data[current_day] = {}
        data[current_day]["visit"] = {}
        data[current_day]["total"] = {}
    try:
        old = data[current_day]["visit"][current_time]
        data[current_day]["visit"][current_time] = old + num_data
        total = 0
        for key, value in data[current_day]["visit"].items():
            total += value
        data[current_day]["total"] = total
    except KeyError:
        data[current_day]["visit"][current_time] = num_data
        total = 0
        for key, value in data[current_day]["visit"].items():
            total += value
        data[current_day]["total"] = total
    
    writer.save_obj(data,"data.data")

def export_csv():
    days = []
    for i in data:
        days.append(i)
    hours = []
    for i in days:
        for j in data[i]["visit"]:
            hours.append(j)
    res = [] 
    [res.append(x) for x in hours if x not in res]
    hours = res

    print(days)
    print(hours)


@app.route('/')
def table():
    start = request.args.get('start')
    end = request.args.get('end')
    if start and end:
        print("Filter start and end")

    elif start:
        print("Filter start")
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        res = {}
        workdata = data
        for i in workdata:
            if i.date() >= start_date:
                res[i] = workdata[i]
        return render_template('table.html',data = res)
    elif end:
        print("Filter end")
        pass
    else:
        print("No filter")
    
    return render_template('table.html',data = data)

if __name__ == '__main__':
    app.run(debug=True)