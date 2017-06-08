import json
import requests
import datetime
import bus
import os.path


def findLocation(lat, lon):
    for area in all:
        if (all[area]["north_bound"] > lat):
            if (all[area]["west_bound"] < lon):
                if (all[area]["south_bound"] < lat):
                    if (all[area]["east_bound"] > lon):
                        return area


def nearestStop(lat, lon):
    nearest_value = 9999
    nearest_stop_name = None
    nearest_stop_id = None
    for stop in stops:
        x = (stops[stop]["east_bound"] + stops[stop]["west_bound"]) / 2
        y = (stops[stop]["north_bound"] + stops[stop]["south_bound"]) / 2
        diff_x = abs(lon - x)
        diff_y = abs(lat - y)
        diff_total = diff_x + diff_y
        if diff_total < nearest_value:
            nearest_value = diff_total
            nearest_stop_name = stop
            nearest_stop_id = stops[stop]["id"]
    return {"location": [nearest_stop_name, nearest_stop_id]}


with open(
        os.path.dirname(__file__) + "/stops.json",
        encoding="utf-8") as stops_info:
    json_file = json.loads(stops_info.read())

stops = json_file["Stops"].copy()
all = json_file["Stops"]
all.update(json_file["Sections"])
buses = {}

#locations = []


def parse():
    try:
        now = datetime.datetime.now()
        if now.isoweekday() in [1, 3, 5]:
            mode = 1
        elif now.isoweekday() in [2, 4]:
            mode = 2
        else:
            mode = 3
        log_name = "/data/mode/" + str(mode) + "/loop_log_" + now.strftime(
            "%Y_%m_%d")
        log = open(os.path.dirname(__file__) + log_name, "a")
        r = requests.get("http://bts.ucsc.edu:8081/location/get")
        #r = requests.get("http://73.70.251.146:2580/bus.json")
        real_time_data = r.json()
        locations = []

        for data in real_time_data:
            location = findLocation(data["lat"], data["lon"])
            if location != None:
                id = data["id"]
                type = data["type"].replace(" ", "_")
                if id not in buses:
                    new = bus.Bus(id)
                    buses.update({id: new})
                if location != buses[id].getMostRecentLocation():
                    checkDir = True
                else:
                    checkDir = False
                locationObj = bus.Location(
                    location, type,
                    datetime.datetime.now().strftime("%H:%M:%S"),
                    buses[id].getDirection())
                buses[id].addLog(locationObj)
                locations.append(locationObj)
                if checkDir:
                    buses[id].checkDirection()
                out = "{} {}".format(id, buses[id].getMostRecentLocationObj())
                log.write(out)
                log.write("\n")
                print(out)
        log.closed
    except Exception as e:
        print(e)
        print("Network Error")
        pass
    return locations


def clear():
    buses.clear()


def fakeparse():
    l = []
    r = requests.get("http://bts.ucsc.edu:8081/location/get")
    real_time_data = r.json()
    for data in real_time_data:
        location = findLocation(data["lat"], data["lon"])
        if location != None:
            id = data["id"]
            type = data["type"].replace(" ", "_")
            locationObj = bus.Location(
                location, type, datetime.datetime.now().strftime("%H:%M:%S"),
                1)
            l.append(locationObj)
    return l