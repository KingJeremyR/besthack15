# besthack15
Our HackUVA 2015 Project

## Setup
1. Download the Myo SDK: https://developer.thalmic.com/downloads
2. Add the Myo SDK to your path. Instructions adapted from: https://github.com/juharris/myo-python
    * Windows: Add the **full absolute path** of the folder containing myo32.dll and myo64.dll (for example "C:\Program Files\Thalmic Labs\myo-sdk-win-0.8.0\bin" without quotes) to your `PATH`.
    * Mac: Add the **full absolute path** for myo.framework/ (for example "/Library/frameworks/myo.framework" without quotes) to `DYLD_LIBRARY_PATH`.
    * Linux: Good luck, soldier.
3. Install Python 3: https://www.python.org/downloads/
4. Install Pyglet: http://www.pyglet.org/
    * With Pip3: `pip3 install pyglet`
5. Test with: `python test_myo.py`