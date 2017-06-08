import timeline
import datetime


class Map:
    def __init__(self):
        self.school = []
        for i in range(65):
            tl = timeline.timeline()
            self.school.append(tl)

    # insert two locationObjs into their correct position in the map
    def insert(self, location_A, location_B):
        # info about two locations
        start = location_A.getLocationId()
        end = location_B.getLocationId()
        location_difference = abs(start - end)
        if location_difference > 60:
            location_difference = abs(64 - location_difference)
        # find duration
        time_A = location_A.getTime()
        time_B = location_B.getTime()
        time_num_A = datetime.datetime.strptime(time_A, "%H:%M:%S")
        time_num_B = datetime.datetime.strptime(time_B, "%H:%M:%S")
        duration = (time_num_B - time_num_A).seconds
        duration /= location_difference
        if duration > 8 * 60:
            return 0
        # find the timeslot
        second = (time_num_B - datetime.datetime(1970, 1, 1)).seconds
        # find the direction
        direction = location_B.getDirection()
        # insert!
        #print(second, duration, direction)
        if direction != 0:
            for i in range(location_difference):
                if direction == 1:
                    offset = end + i
                    if offset > 64:
                        offset -= 64
                    self.school[offset].insert(second, duration, direction)
                    second += duration
                elif direction == 2:
                    offset = start - i
                    if offset < 1:
                        offset += 64
                    self.school[offset].insert(second, duration, direction)
                    second += duration
                else:
                    pass

    # the estimate time from "start_id" to "end_id" at "second"
    def estimate(self, start_id, end_id, direction, second=None):
        est = 0
        duration = 0
        if second == None:
            second = datetime.datetime.now(
            ).hour * 60 * 60 + datetime.datetime.now(
            ).minute * 60 + datetime.datetime.now().second
        #difference = abs(start_id - end_id)
        #if difference > 60:
        #difference = abs(64 - difference)
        while start_id != end_id:
            i = 0
            if direction == 1:
                duration = self.school[start_id - 1].count(second, direction)
                while duration == 0:
                    duration = self.school[start_id - 1].count(
                        second + (15 * 60) * i, direction)
                    i += 1
                    if second + (15 * 60) * i > 86400:
                        continue
                est += duration
                second += duration
                start_id -= 1
                if start_id < 1:
                    start_id = 64
            elif direction == 2:
                duration = self.school[start_id].count(second, direction)
                while duration == 0:
                    duration = self.school[start_id].count(
                        second - (15 * 60) * i, direction)
                    i += 1
                est += duration
                second += duration
                start_id += 1
                if start_id > 64:
                    start_id = 1
        return est

    # the estimate time for each buses to arrive at "stop_id"
    # if second != None, then use current time
    def allEstimate(self, stop_id, running_buses, second=None):
        loops = []
        if second == None:
            second = datetime.datetime.now(
            ).hour * 60 * 60 + datetime.datetime.now(
            ).minute * 60 + datetime.datetime.now().second
        for location in running_buses:
            direction = location.getDirection()
            id = location.getLocationId()
            if stop_id == id:
                loops.append({
                    "location": id,
                    "type": location.getStatus(),
                    "duration": -1,
                    "direction": direction
                })
                continue
            elif id == 999:
                continue
            if direction == 1 and stop_id > id:
                continue
            elif direction == 2 and stop_id < id:
                continue
            elif direction == 0:
                continue
            duration = self.estimate(id, stop_id, direction, second)
            loops.append({
                "location": id,
                "type": location.getStatus(),
                "duration": duration,
                "direction": direction
            })
        loops = sorted(loops, key=lambda k: k["duration"])
        result = {"current": loops}
        return result

    def clear(self):
        self.school = []
        for i in range(65):
            tl = timeline.timeline()
            self.school.append(tl)