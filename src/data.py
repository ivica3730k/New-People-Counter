import datetime
import pickle
import time


class Data():
    _data = {}
    _laser_registrations = int(0)
    _lock = False

    def __init__(self):
        self._data = self._load_obj("data.data")

    def _save_obj(self, obj, name):
        """
        Function saves object to data file.

        If the data file is not present it will be created.

        :param obj: Object to be written to the file
        :param name: File name for the object to be written to
        :return: None
        """
        with open(name, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def _load_obj(self, name):
        """
        Function is used to obtain the object from the data file.

        :param name: The name of the file from which to load the object
        :return: Loaded object
        """
        try:
            with open(name, 'rb') as f:
                return pickle.load(f)
        except:
            return {}

    def write_visits(self, visits=0):
        """
        Function is used to write visits to the data file.

        In order to save the visit data the current
        time and date is taken, along with the number of visits and
        based on the previous entry is either updated or added to the data file.
        The function automatically updates the total number of visits for the current day.

        :param visits: Number of visits to write to the data file
        :return: None
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

        self._save_obj(self._data, "data.data")

    def export_csv(self, data):
        """
        The function takes the data object and serializes it to CSV standard.

        The provided data is iterated in order to produce the CSV file
        which can be opened by Excel for viewing the visit statistics.
        For hours where there are no visits the zero value is written.

        :param data: Data to be CSV serialized
        :return: CSV formatted string containing the visit data
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
        Function is used to obtain visit data with the wanted filter parameters.

        This function is used to obtain the data from the data object which can
        later be used to display on the web ui or exported to the CSV file.

        :param start: Start day filter parameter, string in %Y-%m-%d format
        :param end: End day filter parameter, string in %Y-%m-%d format
        :return: Data object containing visit information
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
        Function is used to register the laser interruption coming from Arduino uController.

        :return: None
        """
        self._lock = True
        self._laser_registrations = self._laser_registrations + 1
        self._lock = False

    def obtainVisits(self):
        """
        Function is used to calculate the number of visits from the recorded laser registrations.

        This function waits for all laser registrations to be finished before calculating the
        number of visits.
        The calculation works by taking the number of laser registrations and dividing it by
        2, one laser registration for entry and one for exit.
        After the calculation, the number of laser registrations is set to reminder of dividing the
        current value by 2, in case that the current amount of laser registrations is odd number.

        :return: Number of visits from the last time the function was called.
        """
        while self._lock:
            time.sleep(1)
        value = int(self._laser_registrations / 2)
        self._laser_registrations = int(self._laser_registrations % 2)
        return value


data = Data()
