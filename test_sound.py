#!/usr/bin/env python3
import pyglet
import time
snd = pyglet.media.load("assets/sfx/button-3.wav", streaming=False)
snd.play()
time.sleep(1)