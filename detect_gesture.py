#!/usr/bin/env python3
# Add myo-python library to Python path
import os
import sys
import datetime
import sfx
sys.path.append(os.path.join(os.getcwd(), 'myo-python'))

# Test Myo stuff
import myo
myo.init()

from myo.six import print_

class Listener(myo.DeviceListener):

    def __init__(self):
        super(Listener, self).__init__()

        self.BUFFER_SIZE = 8

        self.x_gyro_buffer = [0] * self.BUFFER_SIZE
        self.x_gyro_index = 0

        self.x_accel_buffer = [0] * self.BUFFER_SIZE
        self.x_accel_index = 0

        self.pitch_buffer = [0] * self.BUFFER_SIZE
        self.pitch_index = 0

        self.gyroscope = []
        self.acceleration = []
        self.orientation = []
        self.myo = None

    def on_pair(self, myo, timestamp):
        self.myo = myo
        print_("Hello Myo")

    def on_rssi(self, myo, timestamp, rssi):
        print_("RSSI:", rssi)
        return False # Stop the Hub

    def on_event(self, event):
        pass

    def on_orientation_data(self, myo, timestamp, orientation):
        self.orientation = orientation
        
        roll, pitch, yaw, something = orientation

        self.pitch_buffer[self.pitch_index] = pitch
        self.pitch_index = self.pitch_index + 1

        if self.pitch_index == self.BUFFER_SIZE:
            self.pitch_index = 0



    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        self.gyroscope = gyroscope

        x_gyro, y_gyro, z_gyro = gyroscope
        self.x_gyro_buffer[self.x_gyro_index] = x_gyro
        self.x_gyro_index = self.x_gyro_index + 1

        if self.x_gyro_index == self.BUFFER_SIZE:
            self.x_gyro_index = 0

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        self.acceleration = acceleration

        x_accel, y_accel, z_accel = acceleration
        self.x_accel_buffer[self.x_accel_index] = x_accel
        self.x_accel_index = self.x_accel_index + 1

        if self.x_accel_index == self.BUFFER_SIZE:
            self.x_accel_index = 0


def isPointingUp(listener):
    if get_average(listener.pitch_buffer) < -0.45 and get_average(listener.x_gyro_buffer) > 100:
        return True

    return False

def get_average(buf):

    average = 0

    for val in buf:
        average += val

    return average / len(buf)

def printValues(listener):
    for val in listener.gyroscope:
        print("{},\t".format(round(val, 2)), end="")
    # for val in listener.acceleration:
    #     print("{},\t".format(round(val, 2)), end="")
    for val in listener.orientation:
        print("{},\t".format(round(val, 2)), end="")
    print()



def main():
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)

    listener = Listener()
    hub.run(1000, listener)

    time_of_last_vibrate = -1
    time_of_last_print = datetime.datetime.now()
    current_time = datetime.datetime.now()

    try:
        while hub.running:

            # if datetime.datetime.now() - time_of_last_print  > datetime.timedelta(0, 0.1):
            #     time_of_last_print = datetime.datetime.now()
            #     printValues(listener)

            if datetime.datetime.now() - current_time  > datetime.timedelta(0, 0, 10000):
                current_time = datetime.datetime.now()

            if isPointingUp(listener):
                # print ("Point Up!")
                if time_of_last_vibrate == -1 or (current_time - time_of_last_vibrate) > datetime.timedelta(0,1):
                    listener.myo.vibrate("long")
                    sfx.play("button-3.wav")
                    time_of_last_vibrate = current_time

    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)

if __name__ == '__main__':
    main()
