import threading
import time

import config as conf
import serial
from data import data
from flask import Flask, render_template, request, Response

app = Flask(__name__)
_serial_ok = False


def writeVisits():
    """

    :return:
    """
    try:
        while True:
            visits = data.obtainVisits()
            data.write_visits(visits)
            time.sleep(1)
    except KeyboardInterrupt:
        return


def processSerialPort():
    """

    :return:
    """
    global _serial_ok
    global _reset_serial
    while True:
        try:
            while True:
                conf.read_config_file()
                ARDUINO_COM_PORT = conf.ARDUINO_COM_PORT
                ARDUINO_BAUD_RATE = conf.ARDUINO_BAUD_RATE
                ser = serial.Serial(ARDUINO_COM_PORT, ARDUINO_BAUD_RATE)
                _serial_ok = True
                while True:
                    result = (int(ser.readline()))
                    if result == 1:
                        data.laserRegistration()
        except KeyboardInterrupt:
            return
        except:
            time.sleep(1)
            _serial_ok = False


@app.route('/')
def table():
    """

    :return:
    """
    start = request.args.get('start')
    end = request.args.get('end')
    return render_template('table.html', data=data.getAll(start, end), start=start, end=end, ser_ok=_serial_ok)


@app.route('/csv')
def csv():
    """

    :return:
    """
    start = request.args.get('start')
    end = request.args.get('end')
    csv = data.export_csv(data.getAll(start, end))
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                     "attachment; filename=podatci.csv"})


def flask():
    """

    :return:
    """
    app.run(debug=True, use_reloader=False)


writingThread = threading.Thread(target=writeVisits)
serialPortProcessingThread = threading.Thread(target=processSerialPort)
webServerThread = threading.Thread(target=flask)

if __name__ == '__main__':
    serialPortProcessingThread.start()
    writingThread.start()
    webServerThread.start()
