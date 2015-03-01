#!/usr/bin/env python3
import pyglet # installed via pip3
import time # Python built-in
import sfx # sfx.py
sfx.play_file("assets/sfx/button-3.wav") # full path
time.sleep(1)
sfx.play("zoom.wav") # just filename (if in assets/sfx)
time.sleep(2)