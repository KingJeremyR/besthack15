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
DO_RECORD = False

# comparing data
DO_COMPARE = False
window = list()

# learning
import numpy as np
from sklearn import mixture
clf = mixture.GMM()
LEARNED = False

# exiting
DO_QUIT = False

class Listener(myo.DeviceListener):

    def on_event(self, event):
        global capture, window
        if not hasattr(event, 'acceleration'): return
        # print(event.orientation)
        # print(event.acceleration)
        # print(event.gyroscope)
        data = event.orientation + event.acceleration + event.gyroscope
        if DO_RECORD:
            capture += data
        if DO_COMPARE:
            window += data
            while len(window) > len(capture):
                window.pop(0) # TODO this is slow!!
            if LEARNED and len(window) == len(capture):
                print(clf.predict_proba(window))
        return not DO_QUIT

def main():
    global DO_QUIT, DO_RECORD, LEARNED, DO_COMPARE
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
    # learn!
    X = capture
    print("fitting...")
    clf.fit(X)
    print("fit!")
    LEARNED = True
    # DO_QUIT = True

if __name__ == '__main__':
    main()