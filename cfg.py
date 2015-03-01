#!/usr/bin/env python3
import os.path
import sys
import sfx

CONFIG_PATH = "assets/cfg"

def get_cfg_path(cfg):
    return os.path.join(CONFIG_PATH, cfg)

def load(cfg):
    return load_cfg_file(get_cfg_path(cfg))

def load_cfg_file(fname):
    try:
        conf = __load_cfg_file_unsafe(fname)
        for gesture, sf in conf.items():
            sfx.load(sf)
        return conf
    except FileNotFoundError:
        print("Config file not found: {}".format(fname), file=sys.stderr)
    except e:
        print("Error loading config file: {}".format(e), file=sys.stderr)

def __load_cfg_file_unsafe(fname):
    cfg = dict()
    with open(fname) as f:
        for raw_line in f:
            line = raw_line.strip()
            if line.startswith("#") or ":" not in line: continue
            gesture, sf = map(lambda s: s.strip(), line.split(":", 1))
            cfg[gesture] = sf
    return cfg