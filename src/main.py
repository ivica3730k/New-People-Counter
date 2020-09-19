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
    This function writes visits to the file every second.

    The function obtains visit number from data module and passes
    it back for writing to file.
    This function is meant to be run in thread.
    :return: None
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
    This function handles serial port and listens for data arriving from Arduino uController.

    The function reads configuration file to obtain configuration for opening the serial port.
    Once serial port is opened it listens for incoming messages. When incoming message is 1
    that means that Arduino detected laser interruption.
    This function then notifies the data module via the laserRegistration() function.
    If serial port is down for some reason (i.e. unplugged cable) the function attempts to
    re-read the config file and reopen serial connection, notifying the user in the web ui.
    This function is meant to be run in thread.
    :return: None
    """
    global _serial_ok
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
    This function is used to display visit data to the user in the web ui.

    This function is triggered when user visits the root page of the application.
    The data is then obtained from the data module with appropriate filtering parameters
    and displayed to the user by filling the table.html template and returning it to the user.
    :return: Web response containing visit data
    """
    start = request.args.get('start')
    end = request.args.get('end')
    return render_template('table.html', data=data.getAll(start, end), start=start, end=end, ser_ok=_serial_ok)


@app.route('/csv')
def csv():
    """
    This function is used to export visit data to the user in csv(excel) format.

    This function is triggered when user visits the /csv page of the application.
    The data is then obtained from the data module with appropriate filtering parameters
    and exported to the user by opening an download dialog.
    :return: CSV file containing the visit data
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
    This function is running the web ui of the application.

    This function is meant to be run in thread.
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
