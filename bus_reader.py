#!/usr/bin/env python

import signal
import time
import sys
from pirc522 import RFID

busNum = 'Bus Number'
plateNo = u'Bus Plate Info'

info = {'busNum' : busNum, 'plateNo' : plateNo}

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def get_busInfo():
    return info

def read_Tag():
    while run:
        rdr.wait_for_tag
        (error, data) = rdr.request()
        if not error:
            (error, uid) = rdr.anticoll()
            if not error and str(uid[0]) != "35" and str(uid[0]) != "195":
                print("\nDetected!!!!\n")
                rdr.stop_crypto()
                return "Tag"

    time.sleep(1)
