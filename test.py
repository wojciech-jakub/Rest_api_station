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
def write_file(value):
    f = open('time.txt','w')
    f.write(value+"\n")
    f.close;
    #print("\n------ MEASUREMENT ------")
    #print("TEMP Analog: ", values[1],"\n")
    #print("BMP Atlitude: ", values[1:2],"\n")
    #print("Humidity 22: ", values[1:3],"\n")
    #print("temp22: ", values[3:4],"\n")
    #print("BMP TEMP: ", values[3:5],"\n")
    #print("LUX: ", values[3:6], "\n")
   # print(values[0:3])
   # print(values[3:6])
#    print(values[6:9])


class ReadFromArduino(object):
    """A class to read the serial messages from Arduino. The code running on Arduino
    can for example be the ArduinoSide_LSM9DS0 sketch."""

    def __init__(self, port, SIZE_STRUCT=28, verbose=0):
        self.port = port
        self.millis = get_time_millis()
        self.SIZE_STRUCT = SIZE_STRUCT
        self.verbose = verbose
        self.latest_values = -1
        self.t_init = get_time_millis()
        self.t = 0

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

                    # is  a valid message struct
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


################################################################################
# use is:
ports = look_for_available_ports()
usb_port = serial.Serial('/dev/ttyUSB0', baudrate=9600)
read_from_Arduino_instance = ReadFromArduino(usb_port, verbose=6)
read_from_Arduino_instance.read_one_value()
np.array(read_from_Arduino_instance.latest_values)
while True:
    read_from_Arduino_instance.read_one_value()


"""
################################################################################
# measure noise of sensor (for LSM9DS0)
ports = look_for_available_ports()
usb_port = serial.Serial(ports[0], baudrate=115200, timeout=0.5)
read_from_Arduino_instance = ReadFromArduino(usb_port, verbose=0)
nbr_measurements = 1000
matrix_measurements = np.zeros((nbr_measurements, 6))
for ind in range(nbr_measurements):
    read_from_Arduino_instance.read_one_value()
    matrix_measurements[ind, :] = read_from_Arduino_instance.latest_values
for ind in range(6):
    crrt_array = matrix_measurements[:, ind]
    print(np.std(crrt_array)**2)
for ind in range(6):
    crrt_array = matrix_measurements[:, ind]
    print(np.std(crrt_array))
"""