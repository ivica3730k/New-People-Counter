import datetime
import threading
import time
import config as conf
import writer as writer
from flask import Flask, render_template, request

app = Flask(__name__)

ARDUINO_COM_PORT = conf.ARDUINO_COM_PORT
ARDUINO_BAUD_RATE = conf.ARDUINO_BAUD_RATE

_data = writer.load_obj("data.data")


def write_visits(num_data=0):
    if num_data == 0:
        return
    current_day = datetime.datetime.now()
    current_day = current_day.replace(hour=0, minute=0, second=0, microsecond=0).date()
    current_time = datetime.datetime.now()
    current_time = current_time.replace(minute=0, second=0, microsecond=0).time()
    try:
        _data[current_day]
    except KeyError:
        _data[current_day] = {}
        _data[current_day]["visit"] = {}
        _data[current_day]["total"] = {}
    try:
        old = _data[current_day]["visit"][current_time]
        _data[current_day]["visit"][current_time] = old + num_data
        total = 0
        for key, value in _data[current_day]["visit"].items():
            total += value
        _data[current_day]["total"] = total
    except KeyError:
        _data[current_day]["visit"][current_time] = num_data
        total = 0
        for key, value in _data[current_day]["visit"].items():
            total += value
        _data[current_day]["total"] = total

    writer.save_obj(_data, "data.data")


def export_csv(data):
    csv = ""
    days = []
    for i in data:
        days.append(i)
    hours = []
    for i in days:
        for j in data[i]["visit"]:
            hours.append(j)
    res = []
    [res.append(x) for x in hours if x not in res]
    res.sort()
    hours = res

    csv += "Datum,"
    for i in hours:
        csv += str(i)
        csv += ","
    csv += "Ukupno"
    csv += "\n"

    for i in days:
        csv += str(i) + ","
        for j in hours:
            try:
                csv += str(data[i]["visit"][j])
            except KeyError:
                csv += str(0)
            csv += ","
        csv += str(data[i]["total"])
        csv += "\n"

    return csv


@app.route('/')
def table():
    start = request.args.get('start')
    end = request.args.get('end')
    if start and end:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        res = {}
        workdata = _data
        for i in workdata:
            if start_date <= i.date() <= end_date:
                res[i] = workdata[i]
        return render_template('table.html', data=res)

    elif start:
        print("Filter start")
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        res = {}
        workdata = _data
        for i in workdata:
            if i.date() >= start_date:
                res[i] = workdata[i]
        return render_template('table.html', data=res)
    elif end:
        print("Filter end")
        pass
    else:
        return render_template('table.html', data=_data)


if __name__ == '__main__':
    app.run(debug=True)
