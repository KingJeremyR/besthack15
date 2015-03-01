#!/usr/bin/env python3
import pyglet
import os.path as path

SOUND_PATH = "assets/sfx"
sounds = dict()

def play_file(fname):
    try:
        if fname not in sounds:
            snd = pyglet.media.load(fname, streaming=False)
            sounds[fname] = snd
        return sounds[fname].play()
    except FileNotFoundError as e:
        print("File not found: %s" % fname)
        return None

def play(sfx):
    return play_file(path.join(SOUND_PATH, sfx))