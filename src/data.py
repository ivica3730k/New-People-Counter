import datetime
import pickle

def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    try:
        with open(name, 'rb') as f:
            return pickle.load(f)
    except:
        return {}

_data = load_obj("data.data")
_visits = 0
_laser_registrations = 0


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

    save_obj(_data, "data.data")


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

def getAll(start = None, end = None):
    if start and end:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        res = {}
        workdata = _data
        for i in workdata:
            if start_date <= i <= end_date:
                res[i] = workdata[i]
        return res

    elif start:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        res = {}
        workdata = _data
        for i in workdata:
            if i >= start_date:
                res[i] = workdata[i]
        return res
    elif end:
        print("End")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        res = {}
        workdata = _data
        for i in workdata:
            if i <= end_date:
                res[i] = workdata[i]
        return res
    else:
        return _data
    
def laserRegistration():
    global _laser_registrations
    global _visits
    _laser_registrations += 1
    if _laser_registrations % 2 == 0:
        _visits += 1

def obtainVisits():
    global _visits
    value = _visits
    _visits = 0
    return value