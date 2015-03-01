#!/usr/bin/env python3
# Add myo-python library to Python path
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'myo-python'))

# Test Myo stuff
import myo
myo.init()

class Listener(myo.DeviceListener):

    def on_event(self, event):
        if not hasattr(event, 'acceleration'): return
        # print(event.orientation)
        # print(event.acceleration)
        # print(event.gyroscope)
        data = event.orientation + event.acceleration + event.gyroscope
        print(data)

def main():
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

if __name__ == '__main__':
    main()