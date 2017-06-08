import json
import datetime
import os.path

with open(
        os.path.dirname(__file__) + "/stops.json",
        encoding="utf-8") as stops_info:
    json = json.loads(stops_info.read())

all = json["Stops"]
all.update(json["Sections"])


class Location:
    def __init__(self, location, status, time, direction):
        self.location = location
        self.status = status
        self.time = time
        self.direction = direction

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.location, self.status, self.time,
                                        self.direction)

    def getLocation(self):
        return self.location

    def getLocationId(self):
        return all[self.location]["id"]

    def getStatus(self):
        return self.status

    def getTime(self):
        return self.time

    def getDirection(self):
        return self.direction


class Bus:
    CW = 1
    CCW = 2

    def __init__(self, id):
        self.id = id
        self.locations = []
        self.direction = 0

    def getId(self):
        return self.id

    def getDirection(self):
        return self.direction

    def getMostRecentLocation(self):
        if len(self.locations) != 0:
            return self.locations[len(self.locations) - 1].getLocation()
        return ""

    def getMostRecentLocationObj(self):
        if len(self.locations) != 0:
            return self.locations[len(self.locations) - 1]

    def getLocationLog(self):
        return self.locations

    def addLog(self, location, status=None, time=None, direction=None):
        if (status == None):
            self.locations.append(location)
        else:
            log = Location(location, status, time, direction)
            self.locations.append(log)

    # CW = 1
    # CCW = 2
    def checkDirection(self):
        if len(self.locations) > 1:
            most_recent_location = self.locations[len(self.locations) -
                                                  1].getLocationId()
            second_most_recent_location = self.locations[len(self.locations) -
                                                         2].getLocationId()
            if most_recent_location == 64 and second_most_recent_location == 1:
                self.direction = 1
            elif most_recent_location == 1 and second_most_recent_location == 64:
                self.direction = 2
            elif most_recent_location - second_most_recent_location > 0:
                self.direction = 2
            elif most_recent_location - second_most_recent_location < 0:
                self.direction = 1
            else:
                pass

    def getDuration(self):
        if len(self.locations) > 1:
            most_recent_time = self.locations[len(self.locations) -
                                              1].getTime()
            second_most_recent_time = self.locations[len(self.locations) -
                                                     2].getTime()
            most_recent_time_num = datetime.strptime(most_recent_time,
                                                     "%H:%M:%S")
            second_most_recent_time_num = datetime.strptime(
                second_most_recent_time, "%H:%M:%S")
            return (most_recent_time_num - second_most_recent_time_num).seconds
        return -1

    def printReport(self):
        print("Bus ID " + str(self.id))
        for location in self.locations:
            print(location)

    def printLogs(self):
        for location in self.locations:
            print(location, end="")
