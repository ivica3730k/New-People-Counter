import datetime
import pickle
import time


class Data():
    _data = {}
    _laser_registrations = int(0)
    _lock = False

    def __init__(self):
        """

        """
        self._data = self.load_obj("data.data")

    def save_obj(self, obj, name):
        """

        :param obj:
        :param name:
        :return:
        """
        with open(name, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, name):
        """

        :param name:
        :return:
        """
        try:
            with open(name, 'rb') as f:
                return pickle.load(f)
        except:
            return {}

    def write_visits(self, visits=0):
        """

        :param visits:
        :return:
        """
        if visits == 0:
            return
        current_day = datetime.datetime.now()
        current_day = current_day.replace(hour=0, minute=0, second=0, microsecond=0).date()
        current_time = datetime.datetime.now()
        current_time = current_time.replace(minute=0, second=0, microsecond=0).time()
        try:
            self._data[current_day]
        except KeyError:
            self._data[current_day] = {}
            self._data[current_day]["visit"] = {}
            self._data[current_day]["total"] = {}
        try:
            old = self._data[current_day]["visit"][current_time]
            self._data[current_day]["visit"][current_time] = old + visits
            total = 0
            for key, value in self._data[current_day]["visit"].items():
                total += value
            self._data[current_day]["total"] = total
        except KeyError:
            self._data[current_day]["visit"][current_time] = visits
            total = 0
            for key, value in self._data[current_day]["visit"].items():
                total += value
            self._data[current_day]["total"] = total

        self.save_obj(self._data, "data.data")

    def export_csv(self, data):
        """

        :param data:
        :return:
        """
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

    def getAll(self, start=None, end=None):
        """

        :param start:
        :param end:
        :return:
        """
        if start and end:
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
            res = {}
            workdata = self._data
            for i in workdata:
                if start_date <= i <= end_date:
                    res[i] = workdata[i]
            return res

        elif start:
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            res = {}
            workdata = self._data
            for i in workdata:
                if i >= start_date:
                    res[i] = workdata[i]
            return res
        elif end:
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
            res = {}
            workdata = self._data
            for i in workdata:
                if i <= end_date:
                    res[i] = workdata[i]
            return res
        else:
            return self._data

    def laserRegistration(self):
        """

        :return:
        """
        self._lock = True
        self._laser_registrations = self._laser_registrations + 1
        self._lock = False

    def obtainVisits(self):
        """

        :return:
        """
        while self._lock:
            time.sleep(1)
        value = int(self._laser_registrations / 2)
        self._laser_registrations = int(self._laser_registrations % 2)
        return value


data = Data()
