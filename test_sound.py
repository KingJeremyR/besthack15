#!/usr/bin/env python3
import pyglet
import time
# try:
#     snd = pyglet.media.load("assets/sfx/button-3.wav", streaming=False)
#     snd.play()
#     time.sleep(1)
# except FileNotFoundError as e:
#     print(e)
import sfx
sfx.play_file("assets/sfx/button-3.wav") # full path
time.sleep(1)
sfx.play("zoom.wav") # just filename (if in assets/sfx)
time.sleep(2)