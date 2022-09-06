import RPi.GPIO as GPIO
from flask import Flask, jsonify
import test, time
import requests, xmltodict, json
import urllib3
import db

urllib3.disable_warnings()

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

GPIO.setup(40, GPIO.OUT, initial = GPIO.LOW)

@app.route('/controlBell/<number>', methods=['GET', 'POST'])
def controlBell(number):
    if number == '1':
        GPIO.output(40, GPIO.HIGH)
    else:
        GPIO.output(40, GPIO.LOW)
    return jsonify(current_Bus)

@app.route('/getBusInfo', methods=['GET', 'POST'])
def get_busInfo():
    return jsonify(current_Bus)

@app.route('/waitBus/<stationName>/<reserveTime>', methods=['GET', 'POST'])
def wait_bus(stationName, reserveTime):
    stationID = db.getStationID(current_Bus['busNum'], stationName, current_Bus['plateNo'])
    reserve = db.wait_bus(stationID, current_Bus['plateNo'], reserveTime)
    print(reserve)

    if reserve == 'No':
        return "NULL"
    else:
        return jsonify(reserve)

if __name__ == '__main__':
    current_Bus = test.get_busInfo()
    #if test.read_Tag() == 'Tag':
    app.run(host = 'Your IP', port = 55443, debug = True)
