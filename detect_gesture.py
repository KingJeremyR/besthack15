#!/usr/bin/env python3
# Add myo-python library to Python path
import os
import sys
import datetime
import sfx
from enum import Enum
import math
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
        self.y_gyro_buffer = [0] * self.BUFFER_SIZE
        self.y_gyro_index = 0
        self.z_gyro_buffer = [0] * self.BUFFER_SIZE
        self.z_gyro_index = 0

        self.x_accel_buffer = [0] * self.BUFFER_SIZE
        self.x_accel_index = 0
        self.y_accel_buffer = [0] * self.BUFFER_SIZE
        self.y_accel_index = 0
        self.z_accel_buffer = [0] * self.BUFFER_SIZE
        self.z_accel_index = 0

        self.pitch_buffer = [0] * self.BUFFER_SIZE
        self.pitch_index = 0

        self.gyroscope = []
        self.acceleration = []
        self.orientation = [0,0,0,0]
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

        self.y_gyro_buffer[self.y_gyro_index] = y_gyro
        self.y_gyro_index = self.y_gyro_index + 1

        if self.y_gyro_index == self.BUFFER_SIZE:
            self.y_gyro_index = 0

        self.z_gyro_buffer[self.z_gyro_index] = z_gyro
        self.z_gyro_index = self.z_gyro_index + 1

        if self.z_gyro_index == self.BUFFER_SIZE:
            self.z_gyro_index = 0

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        self.acceleration = acceleration

        x_accel, y_accel, z_accel = acceleration
        self.x_accel_buffer[self.x_accel_index] = x_accel
        self.x_accel_index = self.x_accel_index + 1

        if self.x_accel_index == self.BUFFER_SIZE:
            self.x_accel_index = 0

        self.y_accel_buffer[self.y_accel_index] = y_accel
        self.y_accel_index = self.y_accel_index + 1

        if self.y_accel_index == self.BUFFER_SIZE:
            self.y_accel_index = 0

        self.z_accel_buffer[self.z_accel_index] = z_accel
        self.z_accel_index = self.z_accel_index + 1

        if self.z_accel_index == self.BUFFER_SIZE:
            self.z_accel_index = 0

# START MAIN

Direction = Enum("Direction", "left right up down forward back")

direction = 0
roll = 0
pitch = 0
yaw = 0

time_of_last_vibrate = datetime.datetime.now()
time_of_last_print = datetime.datetime.now()
current_time = datetime.datetime.now()

def get_average(buf):

    average = 0

    for val in buf:
        average += val

    return average / len(buf)

def printValues(listener):
    global direction, time_of_last_print

    if datetime.datetime.now() - time_of_last_print  > datetime.timedelta(0, 0.25):
        time_of_last_print = datetime.datetime.now()
        # for val in listener.gyroscope:
        #     print("{},\t".format(round(val, 2)), end="")
        # for val in listener.acceleration:
        #     print("{},\t".format(round(val, 2)), end="")
        # for val in listener.orientation:
        #     print("{},\t".format(round(val, 2)), end="")
        # print(get_average(listener.pitch_buffer), end="")
        # print("\t", end="")
        # print(get_average(listener.x_gyro_buffer), end="")
        print(str(roll) + ", " + str(pitch) + ", " + str(yaw))
        print(direction)
        # print()

def update_direction(listener):
    global roll, pitch, yaw, direction
    # http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    x,y,z,w = listener.orientation
    try:
        roll  = float(math.atan2(2.0 * (float(w * x) + float(y * z)), 1.0 - 2.0 * (float(x * x) + float(y * y))))
        pitch = float(math.asin(-2.0 * (float(y * w) - float(z * x))))
        yaw   = float(math.atan2(-2.0 * (float(w * z) + float(x * y)), 1.0 - 2.0 * (float(y * y) + float(z * z))))
    except ValueError: 
        pass

    # TODO: Calibrate forward directions? 

    if pitch < -0.75:
        direction = Direction.up
    elif pitch > 0.75:
        direction = Direction.down
    elif yaw > 2:
        direction = Direction.left
    elif yaw < -2:
        direction = Direction.forward
    elif yaw > 0:
        direction = Direction.back
    elif yaw < 0:
        direction = Direction.right

def long_vibrate(listener, action):
    global current_time, time_of_last_vibrate
    if current_time - time_of_last_vibrate > datetime.timedelta(0,1):
        listener.myo.vibrate("long")
        time_of_last_vibrate = current_time
        action()

def moving_up(listener):
    global direction

    if direction == Direction.up and get_average(listener.x_gyro_buffer) > 75:
        return True

    return False

def moving_forward(listener):
    global direction

    if direction == Direction.forward and get_average(listener.x_gyro_buffer) > 75:
        return True

    return False

def up_action():
    sfx.play("button-3.wav")

def forward_action():
    sfx.play("punch.wav") 

def main():
    global current_time
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)

    listener = Listener()
    hub.run(1000, listener)

    try:
        while hub.running:

            printValues(listener)

            if datetime.datetime.now() - current_time  > datetime.timedelta(0, 0, 10000):
                current_time = datetime.datetime.now()
                update_direction(listener)        

            if moving_up(listener):
                long_vibrate(listener, up_action)

            elif moving_forward(listener):
                long_vibrate(listener, forward_action)
                
                    


    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)

if __name__ == '__main__':
    main()
