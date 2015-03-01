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

    #def on_rssi(self, myo, timestamp, rssi):
        #print_("RSSI:", rssi)
        #return False # Stop the Hub

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

yaw_calibrated = 0
YAW_INTERVAL = 0.75

BUFFER_SIZE = 32
yaw_buffer = [0] * BUFFER_SIZE
yaw_buffer_index = 0

forward_left, forward_right, left_left, left_right, back_left, back_right, right_left, right_right = 0, 0, 0, 0, 0, 0, 0, 0

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

def update_orientation(listener):
    global roll, pitch, yaw
    # http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    x,y,z,w = listener.orientation
    try:
        roll  = float(math.atan2(2.0 * (float(w * x) + float(y * z)), 1.0 - 2.0 * (float(x * x) + float(y * y))))
        pitch = float(math.asin(-2.0 * (float(y * w) - float(z * x))))
        yaw   = float(math.atan2(-2.0 * (float(w * z) + float(x * y)), 1.0 - 2.0 * (float(y * y) + float(z * z))))
    except ValueError: 
        pass

def update_direction(listener):
    global roll, pitch, yaw, direction, yaw_calibrated, YAW_INTERVAL 
    global forward_left, forward_right, left_left, left_right, back_left, back_right, right_left, right_right

    update_orientation(listener)

    if pitch < -0.75:
        direction = Direction.up
    elif pitch > 0.75:
        direction = Direction.down
    else:

        if (yaw > forward_left and yaw < forward_left + (2 * YAW_INTERVAL)) or (forward_left + (2 * YAW_INTERVAL) > 3 and yaw < forward_right):
            direction = Direction.forward
        elif (yaw > left_left and yaw < left_left + (2 * YAW_INTERVAL)) or (left_left + (2 * YAW_INTERVAL) > 3 and yaw < left_right):
            direction = Direction.left
        elif (yaw > back_left and yaw < back_left + (2 * YAW_INTERVAL)) or (back_left + (2 * YAW_INTERVAL) > 3 and yaw < back_right):
            direction = Direction.back
        elif (yaw > right_left and yaw < right_left + (2 * YAW_INTERVAL)) or (right_left + (2 * YAW_INTERVAL) > 3 and yaw < right_right):
            direction = Direction.right
        

def long_vibrate(listener, action):
    global current_time, time_of_last_vibrate
    if current_time - time_of_last_vibrate > datetime.timedelta(0,1):
        listener.myo.vibrate("long")
        time_of_last_vibrate = current_time
        action()

def moving_up(listener):
    global direction

    if direction == Direction.up and get_average(listener.x_gyro_buffer) > 100:
        return True

    return False

def moving_forward(listener):
    global direction

    if direction == Direction.forward and get_average(listener.x_gyro_buffer) > 100:
        return True

    return False

def moving_leftToRight(listener):
    global direction
    if direction == Direction.left and get_average(listener.z_gyro_buffer) < -100:
        return True

    return False

def up_action():
    sfx.play("button-3.wav")

def forward_action():
    sfx.play("punch.wav") 

def leftToRight_action():
    sfx.play("zoom.wav")

def main():
    global current_time, yaw_calibrated, yaw, BUFFER_SIZE, yaw_buffer, yaw_buffer_index
    global forward_left, forward_right, left_left, left_right, back_left, back_right, right_left, right_right
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)

    listener = Listener()
    hub.run(1000, listener)

    try:
        print("Calibrating...")
        print("Hold your arm out in front of you for a short while.")

        current_time = datetime.datetime.now()

        while(datetime.datetime.now() - current_time < datetime.timedelta(0, 3)):
            update_orientation(listener)
            yaw_buffer[yaw_buffer_index] = yaw
            yaw_buffer_index += 1

            if yaw_buffer_index == BUFFER_SIZE:
                yaw_buffer_index = 0

        yaw_calibrated = get_average(yaw_buffer)

        forward_left = yaw_calibrated - YAW_INTERVAL if yaw_calibrated - YAW_INTERVAL > -3 else yaw_calibrated - YAW_INTERVAL + 6
        forward_right = yaw_calibrated + YAW_INTERVAL if yaw_calibrated + YAW_INTERVAL < 3 else yaw_calibrated + YAW_INTERVAL - 6
        left_left = yaw_calibrated - (YAW_INTERVAL * 3) if yaw_calibrated - (YAW_INTERVAL * 3) > -3 else yaw_calibrated - (YAW_INTERVAL * 3) + 6
        left_right = forward_left
        back_left = yaw_calibrated - (YAW_INTERVAL * 5) if yaw_calibrated - (YAW_INTERVAL * 5) > -3 else yaw_calibrated - (YAW_INTERVAL * 5) + 6
        back_right = left_left
        right_left = forward_right
        right_right = back_left

        print(forward_left)
        print(forward_right)

        print(left_left)
        print(left_right)

        listener.myo.vibrate("short")

        print(yaw_calibrated)

        while hub.running:

            printValues(listener)

            if datetime.datetime.now() - current_time  > datetime.timedelta(0, 0, 10000):
                current_time = datetime.datetime.now()
                update_direction(listener)        

            if moving_up(listener):
                long_vibrate(listener, up_action)

            elif moving_forward(listener):
                long_vibrate(listener, forward_action)

            elif moving_leftToRight(listener):
                long_vibrate(listener, leftToRight_action)
                
                    


    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)

if __name__ == '__main__':
    main()
