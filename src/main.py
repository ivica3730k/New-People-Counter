import datetime
import threading
import time
import config as conf
import data as data
from flask import Flask, render_template, request, Response
import serial

app = Flask(__name__)
_serial_ok = False


def writeVisits():
    global _times_written
    print("Started writing thread")
    try:
        while True:
            data.write_visits(data.obtainVisits())
            time.sleep(10)
    except KeyboardInterrupt:
        return

def processSerialPort():
    print("Started serial port processing thread")
    global _serial_ok
    ARDUINO_COM_PORT = conf.ARDUINO_COM_PORT
    ARDUINO_BAUD_RATE = conf.ARDUINO_BAUD_RATE
    ser = serial.Serial(ARDUINO_COM_PORT,ARDUINO_BAUD_RATE, timeout=1)
    _serial_ok = True
    try:
        while True:
            ser.readline()
            data.laserRegistration()
    except:
        _serial_ok = False



writingThread = threading.Thread(target=writeVisits)
serialPortProcessingThread = threading.Thread(target=processSerialPort)

@app.route('/')
def table():
    start = request.args.get('start')
    end = request.args.get('end')
    return render_template('table.html', data=data.getAll(start,end),start = start, end = end)

@app.route('/csv')
def csv():
    start = request.args.get('start')
    end = request.args.get('end')
    csv = data.export_csv(data.getAll(start,end))
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=podatci.csv"})

    


if __name__ == '__main__':
    writingThread.start()
    serialPortProcessingThread.start()
    app.run(debug=True)
