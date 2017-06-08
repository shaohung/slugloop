import datetime
from collections import OrderedDict

class timeline:
    def __init__(self):
        self.timetable = OrderedDict()
        second = 0
        while second < 86400:
            t = timeslot()
            self.timetable.update({second: t})
            second += 10 * 60

    def insert(self, second, duration, direction):
        prevtime = 0
        for time in self.timetable.keys():
            if time > second:
                if direction == 1:
                    self.timetable[prevtime].addCW(duration)
                    return 1
                else:
                    self.timetable[prevtime].addCCW(duration)
                    return 1
            prevtime = time
        if direction == 1:
            self.timetable[time].addCW(duration)
            return 1
        else:
            self.timetable[time].addCCW(duration)
            return 1
        return 0

    def current(self, direction):
        prevtime = 0
        now = datetime.datetime.now()
        now_in_seconds = now.hour * 60 * 60 + now.minute * 60 + now.second
        for time, timeslot in self.timetable.items():
            if time > now_in_seconds:
                if direction == 1:
                    return self.timetable[prevtime].getAverage_CW()
                else:
                    return self.timetable[prevtime].getAverage_CCW()
            prevtime = time
        return -1

    def count(self, second, direction):
        prevtime = 0
        for time, timeslot in self.timetable.items():
            if time > second:
                if direction == 1:
                    return self.timetable[prevtime].getAverage_CW()
                else:
                    return self.timetable[prevtime].getAverage_CCW()
            prevtime = time
        return -1

    def __str__(self):
        str1 = "{:5} {:6} {:6}".format("Time", "CW(s)", "CCW(s)")
        for time, timeslot in self.timetable.items():
            m, s = divmod(time, 60)
            h, m = divmod(m, 60)
            str1 += "\n{:02d}:{:02d} {}".format(h, m, timeslot)
        return str1


class timeslot:
    def __init__(self):  # CW = 1 CCW = 2
        self.CW = []
        self.CCW = []

    def __str__(self):
        return "{:06.2f} {:06.2f}".format(self.getAverage_CW(),
                                          self.getAverage_CCW())

    def addCW(self, value):
        self.CW.append(value)

    def addCCW(self, value):
        self.CCW.append(value)

    def getAverage_CW(self):
        if len(self.CW) == 0:
            return 0
        return sum(self.CW) / len(self.CW)

    def getAverage_CCW(self):
        if len(self.CCW) == 0:
            return 0
        return sum(self.CCW) / len(self.CCW)