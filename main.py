import datetime
import threading
import time
import config as conf
import data as data
from flask import Flask, render_template, request, Response

app = Flask(__name__)

ARDUINO_COM_PORT = conf.ARDUINO_COM_PORT
ARDUINO_BAUD_RATE = conf.ARDUINO_BAUD_RATE



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
    app.run(debug=True)
