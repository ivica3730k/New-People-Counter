import datetime
import threading
import time
from bottle import route, run, template, HTTPResponse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config as conf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Visits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    count = db.Column(db.Integer)


def write_visits(num_visits = 0):
    if num_visits == 0:
        return
    if not Visits.query.order_by(Visits.id.desc()).first():
        # This is a first record in the database 
        dt = datetime.datetime.now()
        dt = dt.replace(minute=0, second=0, microsecond=0)
        x = Visits(timestamp = dt,count = num_visits)
        db.session.add(x)
        db.session.commit()
        print("Written first record")
    else:
        # This is not a first record in the database, but we need to compare it
        # with the current time. If it is in same hour period update the previous record.
        # If it is not, create a new record
        previous = Visits.query.order_by(Visits.id.desc()).first()
        dt = datetime.datetime.now()
        dt = dt.replace(minute=0, second=0, microsecond=0)
        if previous.timestamp == dt:
            # The new record would have the same timestamp, update the old one
            previous.count = previous.count + num_visits
            db.session.add(previous)
            db.session.commit()
            print("Updated old record")
        else:
            # The new recourd would have the different timestamp, create a new one
            dt = datetime.datetime.now()
            dt = dt.replace(minute=0, second=0, microsecond=0)
            new = Visits(timestamp = dt, count = num_visits)
            db.session.add(new)
            db.session.commit()
            print("Created new record")




        
    

ARDUINO_COM_PORT = conf.ARDUINO_COM_PORT
ARDUINO_BAUD_RATE = conf.ARDUINO_BAUD_RATE


def web_server():
    @route('/')
    def table():
        obtained = Visits.query.order_by(Visits.id.desc()).all()
        data = {}
        for i in obtained:
            data[i.]
        print(data)
        return template('templates/table.html',data)

    run(host='localhost', port=8080, debug=True)

def serial_listener():
    while True:
        print("2")
        time.sleep(1)


t1 = threading.Thread(target=web_server)
# t2 = threading.Thread(target=serial_listener)
t1.start()
# t2.start()
