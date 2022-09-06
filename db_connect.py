import pymysql
import requests, xmltodict, json
from flask import Flask, jsonify
import urllib3
import time

urllib3.disable_warnings()

key = "Your Private Key"

bus_db = pymysql.connect(
    user = 'Your Id',
    passwd = 'Your Password',
    host = 'Your DB endpoint',
    db = 'DB Name',
    charset = 'utf8'
    )

def getStationID(busNum, stationName, plateNo):
    stationID = ""
    seq = getSeq(busNum, plateNo)

    cursor = bus_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT routeID FROM bus WHERE busNum = %s;"
    cursor.execute(sql, (busNum))
    result = cursor.fetchone()
    routeID = result['routeID']

    buslocation_url = "https://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList?serviceKey={0}&>
    content = requests.get(buslocation_url, verify=False).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['response']['msgBody']['busRouteStationList'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    for i in range(len(jsonObj)):
        if int(jsonObj[i]['stationSeq']) >= int(seq) and jsonObj[i]['stationName'] == stationName:
            stationID = jsonObj[i]['stationId']
            break

    print("reserve staID : " + stationID)
    return stationID

def getSeq(busNum, plateNo):
    seq = ""

    cursor = bus_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT routeID FROM bus WHERE busNum = %s;"
    cursor.execute(sql, (busNum))
    result = cursor.fetchone()
    routeID = result['routeID']
    buslocation_url = "https://apis.data.go.kr/6410000/buslocationservice/getBusLocationList?serviceKey={0}&r>
    content = requests.get(buslocation_url, verify=False).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['response']['msgBody']['busLocationList'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    for i in range(len(jsonObj)):
        if jsonObj[i]['plateNo'] == plateNo:
            seq = jsonObj[i]['stationSeq']
            break
    print("current seq : " + seq)
    return seq

def wait_bus(stationID, plateNo, reserve_time):
    stationList_url = "http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList?serviceKey={0}&stat>

    content = requests.get(stationList_url).content
    dict = xmltodict.parse(content)

    try:
        jsonString = json.dumps(dict['response']['msgBody']['busArrivalList'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        for i in range(len(jsonObj)):
            if jsonObj[i]['plateNo1'] == plateNo:
                return jsonObj[i]['predictTime1']
            elif jsonObj[i]['plateNo2'] == plateNo:
                return jsonObj[i]['predictTime2']

    except KeyError:
        return "No"

