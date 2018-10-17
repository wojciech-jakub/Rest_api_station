from __future__ import print_function
import glob
import struct
import time
import numpy as np
import serial

def look_for_available_ports():
    '''
    find available serial ports to Arduino
    '''
    available_ports = glob.glob('/dev/ttyUSB0')
    print("Available porst: ")
    print(available_ports)

    return available_ports


def get_time_millis():
    return(int(round(time.time() * 1000)))


def get_time_seconds():
    return(int(round(time.time() * 1000000)))


def print_values(values):
    for x in values:
    	print(x)



class ReadFromArduino(object):

    def __init__(self, port, SIZE_STRUCT=4, verbose=0):
        self.port = port
        self.millis = get_time_millis()
        self.SIZE_STRUCT = SIZE_STRUCT
        self.verbose = verbose
        self.latest_values = -1
        self.t_init = get_time_millis()
        self.t = 0

        self.port.flushInput()


    def read_one_value(self):

        read = False

        while not read:
            myByte = self.port.read(1)
            if myByte == 'S':
                data = self.port.read(self.SIZE_STRUCT)
                myByte = self.port.read(1)
                if myByte == 'E':
                    self.t = (get_time_millis() - self.t_init) / 1000.0

                    # is  a valid message struct
                    new_values = struct.unpack('<f', data)

                    current_time = get_time_millis()
                    time_elapsed = current_time - self.millis
                    self.millis = current_time

                    read = True

                    self.latest_values = np.array(new_values)

                    if self.verbose > 1:
                        print("Time elapsed since last (ms): " + str(time_elapsed))
                        print_values(new_values)
            			f = open("time_system.txt","a+")
            			f.write("%d\n" % new_values)
            			f.close
                    return(True)
        return(False)


ports = look_for_available_ports()
usb_port = serial.Serial('/dev/ttyUSB0', baudrate=9600)
read_from_Arduino_instance = ReadFromArduino(usb_port, verbose=6)
read_from_Arduino_instance.read_one_value()
np.array(read_from_Arduino_instance.latest_values)
i = 0
while True:
    read_from_Arduino_instance.read_one_value()
    i = i + 1
    if i > 1000:
	exit()
