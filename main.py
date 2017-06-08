from flask import Flask, send_from_directory, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import json
import bus
import time
import analyzer
import collector
import sys
import logging
app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

m = None


def fetch():
    global m
    m = analyzer.import_data()


def parse():
    collector.parse()


def daily():
    print("daily job!")
    analyzer.analyze()
    global m
    m = analyzer.import_data()
    collector.clear()


sched = BackgroundScheduler()
sched.add_job(parse, 'interval', seconds=5)
sched.add_job(daily, 'cron', day_of_week='mon-sun', hour=0, minute=0, second=10)
sched.start()
fetch()


@app.route("/")
def hello():
    return send_from_directory("web", "index.html")


@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory("", filename, as_attachment=True)


@app.route("/api")
def test():
    return jsonify(bus.all)


@app.route("/api/from/<int:start>/to/<int:end>/dir/<int:dir>/at/<int:sec>")
def getTime(start, end, dir, sec):
    return jsonify({"duration": m.estimate(start, end, dir, sec)})


@app.route("/api/at/<int:stop>")
def standard(stop):
    return jsonify(m.allEstimate(stop, collector.fakeparse()))


@app.route("/api/exp/at/<int:stop_id>")
def experimental(stop_id):
    if stop_id < 0 or stop_id > 64:
        return jsonify({"current": "wrong stop id"})
    return jsonify(m.allEstimate(stop_id, collector.parse()))


@app.route("/api/location/<string:lat>/<string:lon>")
def getLocation(lat, lon):
    return jsonify(collector.nearestStop(float(lat), float(lon)))


if __name__ == "__main__":
    app.run()
