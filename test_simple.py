#!/usr/bin/env python3
# Add myo-python library to Python path
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'myo-python'))

# Test Myo stuff
import myo
myo.init()

# recording data
capture = list()
capture_ranges = None
DO_RECORD = False

# comparing data
import time
Infinity = float("inf")
DO_COMPARE = False
window = list()

# exiting
DO_QUIT = False

def normalize(value, tuple_range):
    lit, big = tuple_range
    return (value - lit) / (big - lit)

def compare_frames(ref, cur, ranges):
    sum = 0
    for i, (xa, xb) in enumerate(zip(ref, cur)):
        rng = ranges[i]
        na = normalize(xa, rng)
        nb = normalize(xb, rng)
        sum += (na - nb) ** 2
    return sum

def compare_recordings(ref, cur, ranges):
    max_tups = \
        max(zip(ref, cur), key=lambda tup: compare_frames(tup[0], tup[1], ranges))
    return compare_frames(max_tups[0], max_tups[1], ranges)


class Listener(myo.DeviceListener):

    def on_pose(self, myo, timestamp, pose):
        print(pose)

    def on_event(self, event):
        global capture, capture_ranges, window
        if not hasattr(event, 'acceleration'): return
        # print(event.orientation)
        # print(event.acceleration)
        # print(event.gyroscope)
        data = []
        data += event.orientation
        data += event.acceleration
        # data += event.gyroscope
        if DO_RECORD:
            capture.append(data)
        elif capture_ranges is None and DO_COMPARE:
            num_features = len(capture[0])
            capture_ranges = [(Infinity, -Infinity)] * num_features
            for i in range(len(capture[0])):
                for frame in capture:
                    rng = capture_ranges[i]
                    capture_ranges[i] = (
                        min(frame[i], rng[0]),
                        max(frame[i], rng[1])
                    )
            # print(capture_ranges)
            return True
        elif DO_COMPARE:
            window.append(data)
            while len(window) > len(capture):
                window.pop(0)
            if len(window) == len(capture):
                diff = compare_recordings(capture, window, capture_ranges)
                if diff < 2.5:
                    print("GOT A MATCH: {}".format(time.time()))
        return not DO_QUIT

def main():
    global DO_QUIT, DO_RECORD, DO_COMPARE
    print("Starting main")
    hub = myo.Hub()
    print("Got hub")
    hub.set_locking_policy(myo.locking_policy.none)
    print("Set locking policy")
    lis = Listener()
    hub.run(1000, lis)
    print("Running listener")
    print("Possible listener methods: ")
    print('\n'.join("* " + att for att in dir(lis) if not att.startswith("__")))
    input("Enter to start recording...")
    DO_RECORD = True
    input("RECORDING :: Enter to stop...")
    DO_RECORD = False
    DO_COMPARE = True
    # DO_QUIT = True

if __name__ == '__main__':
    main()