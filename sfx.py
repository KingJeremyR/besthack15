#!/usr/bin/env python3
import pyglet
import os.path
import sys

SOUND_PATH = "assets/sfx"
sounds = dict()

def get_sfx_path(sfx):
    return os.path.join(SOUND_PATH, sfx)

def load_file(fname):
    success = True
    try:
        if fname not in sounds:
            print('Loading sound file: {}'.format(fname))
            snd = pyglet.media.load(fname, streaming=False)
            sounds[fname] = snd
    except FileNotFoundError:
        print("File not found: {}".format(fname), file=sys.stderr)
        success = False
    return success


def play_file(fname):
    if load_file(fname):
        return sounds[fname].play()
    else:
        return None

def load(sfx):
    return load_file(get_sfx_path(sfx))

def play(sfx):
    return play_file(get_sfx_path(sfx))