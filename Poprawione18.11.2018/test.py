from __future__ import print_function
import glob
import struct
import time
import numpy as np
import serial
import time
import json
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

def look_for_available_ports():
    available_ports = glob.glob('/dev/ttyUSB0')
    print("Available porst: ")
    print(available_ports)

    return available_ports


def get_time_millis():
    return(int(round(time.time() * 1000)))


def get_time_seconds():
    return(int(round(time.time() * 1000000)))

def save_db(data,timestamp):
    ref = db.reference('data/')
    users_ref = ref.child(str(timestamp))
    users_ref.set(data)

def print_values(values):
    timee = int(time.time())
    x = {
            "analog":{
                    "temperature" : values[0]
                },
            "bm280" :{
                    "atlitude": values[1],
                    "temperature": values[4],
                    "pressure": values[6]
                },
            "dht22" :{
                    "temperature":values[3],
                    "humidity":values[2]
                },
            "gy30" :{
                    "lux": values[5]
                },
            "timestamp" : timee

    }
    save_db(x,timee)
    print(values)

class ReadFromArduino(object):

    def __init__(self, port, SIZE_STRUCT=28, verbose=0):
        self.port = port
        self.millis = get_time_millis()
        self.SIZE_STRUCT = SIZE_STRUCT
        self.verbose = verbose
        self.latest_values = -1
        self.t_init = get_time_millis()
        self.t = 0
	cred = credentials.Certificate("first_app.json")
	firebase_admin.initialize_app(cred, {'databaseURL': 'https://first-app-84b8e.firebaseio.com'})
        self.port.flushInput()

    def read_one_value(self):
        """Wait for next serial message from the Arduino, and read the whole
        message as a structure."""
        read = False

        while not read:
            myByte = self.port.read(1)
            if myByte == 'S':
                data = self.port.read(self.SIZE_STRUCT)
                myByte = self.port.read(1)
                if myByte == 'E':
                    self.t = (get_time_millis() - self.t_init) / 1000.0

                    new_values = struct.unpack('<fffffff', data)

                    current_time = get_time_millis()
                    time_elapsed = current_time - self.millis
                    self.millis = current_time

                    read = True

                    self.latest_values = np.array(new_values)

                    if self.verbose > 1:
                        print("Time elapsed since last (ms): " + str(time_elapsed))
                        print_values(new_values)
                    return(True)

        return(False)


ports = look_for_available_ports()
usb_port = serial.Serial('/dev/ttyUSB0', baudrate=9600)
read_from_Arduino_instance = ReadFromArduino(usb_port, verbose=6)
read_from_Arduino_instance.read_one_value()
np.array(read_from_Arduino_instance.latest_values)
while True:
    read_from_Arduino_instance.read_one_value()
