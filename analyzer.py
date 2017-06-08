import bus
import glob
import collector
import map
import os.path
import datetime

m = map.Map()


# analyze logs of a specific mode
def batch_analyze(mode):
    list_of_data = glob.glob("data/mode/" + str(mode) + "/*")
    print(list_of_data)
    for name in list_of_data:
        split = name.split("/")
        file_name = split[len(split) - 1]
        input_file = open(os.path.dirname(__file__) + name, "r")
        output_file = open(
            os.path.dirname(__file__) + "data/processed/" + str(mode) + "/" +
            file_name, "a")
        buses = {}
        for line in input_file:
            data = line.split(" ")
            if data[0] not in buses:
                new = bus.Bus(data[0])
                buses.update({data[0]: new})
            if "Home" not in data[1] and data[1] != buses[data[0]].getMostRecentLocation(
            ):
                buses[data[0]].addLog(data[1], data[2], data[3], data[4])
                buses[data[0]].checkDirection()
                buses[data[0]].getMostRecentLocationObj().direction = buses[
                    data[0]].getDirection()

        for key, loop in buses.items():
            output_file.write("Bus ID " + str(key) + "\n")
            for location in loop.locations:
                output_file.write(str(location))
                output_file.write("\n")


# analyze yesterday's log
def analyze():
    yesterday = datetime.date.fromordinal(datetime.date.today().toordinal() -
                                          1)
    if yesterday.isoweekday() in [1, 3, 5]:
        mode = 1
    elif yesterday.isoweekday() in [2, 4]:
        mode = 2
    else:
        mode = 3
    log_name = "loop_log_" + yesterday.strftime("%Y_%m_%d")
    input_file = open(
        os.path.dirname(__file__) + "/data/mode/" + str(mode) + "/" + log_name,
        "r")
    output_file = open(
        os.path.dirname(__file__) + "/data/processed/" + str(mode) + "/" +
        log_name, "a")
    buses = {}
    for line in input_file:
        data = line.split(" ")
        if data[0] not in buses:
            new = bus.Bus(data[0])
            buses.update({data[0]: new})
        if "Home" not in data[1] and data[1] != buses[data[0]].getMostRecentLocation(
        ):
            buses[data[0]].addLog(data[1], data[2], data[3], data[4])
            buses[data[0]].checkDirection()
            buses[data[0]].getMostRecentLocationObj().direction = buses[data[
                0]].getDirection()

    for key, loop in buses.items():
        output_file.write("Bus ID " + str(key) + "\n")
        for location in loop.locations:
            output_file.write(str(location))
            output_file.write("\n")


# get all the processed data together
def import_data():
    mode = 0
    now = datetime.datetime.now()
    if now.isoweekday() in [1, 3, 5]:
        mode = 1
    elif now.isoweekday() in [2, 4]:
        mode = 2
    else:
        mode = 3
    buses = {}
    m.clear()
    list_of_data = glob.glob("data/processed/" + str(mode) + "/*")
    print(list_of_data)
    for name in list_of_data:
        file = open(os.path.dirname(__file__) + "/" + name, "r")
        #file = open(name, 'r')
        for line in file:
            splited = line.split(" ")
            if "Bus ID" in line:
                bus_id = splited[2]
                new_bus = bus.Bus(bus_id)
                buses.update({bus_id: new_bus})
            else:
                if len(buses[bus_id].locations) >= 1:
                    prev_location = buses[bus_id].getMostRecentLocationObj()
                buses[bus_id].addLog(splited[0], splited[1], splited[2],
                                     int(splited[3]))
                current_location = buses[bus_id].getMostRecentLocationObj()
                if len(buses[bus_id].locations) > 1:
                    m.insert(prev_location, current_location)
        buses.clear()
    for i in range(1, len(m.school)):
        print(i)
        print(m.school[i])
    return m