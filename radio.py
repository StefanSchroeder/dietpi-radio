
import asyncio
import csv
import curses
import json
import os
import signal
import subprocess
import sys
import time, shlex

from RPi import GPIO
from curses import wrapper
from pathlib import Path

jsondir = Path(__file__).parent

with open(str(jsondir) + "/" + "radio.json", 'r') as f:
    data = json.load(f)

CLK = 5
DT = 7
SW = 32

def CLKClicked(channel):
    CLKState = GPIO.input(CLK)
    DTState = GPIO.input(DT)
    if CLKState == 0 and DTState == 1:
        applyVolume(data["volume"] - 4)

def DTClicked(channel):
    CLKState = GPIO.input(CLK)
    DTState = GPIO.input(DT)
    if CLKState == 1 and DTState == 0:
        applyVolume(data["volume"] + 4)

def applyVolume(volume):
    data["volume"] = clamp(volume)
    subprocess.Popen(shlex.split("amixer sset '"+data["amixer"]+"' "+str(data["volume"])+"%"))

def SetRadioChannel():
    os.system("pkill mplayer");
    chan = data["current"]
    args = shlex.split(data["radio"][chan]+" &")
    my_env = os.environ.copy()
    my_env["MPLAYER_VERBOSE"] = "-1"
    subprocess.Popen(args, env=my_env)

def SetRadioChannelUp(dummy):
    data["current"] = ( data["current"] + 1 ) % len(data["radio"])
    SetRadioChannel()

def no_curses_main():
    SetRadioChannel()
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except:
        loop.close()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(CLK, GPIO.IN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(CLK, GPIO.FALLING, callback=CLKClicked, bouncetime=300)
GPIO.add_event_detect(DT, GPIO.FALLING, callback=DTClicked, bouncetime=300)
GPIO.add_event_detect(SW, GPIO.FALLING, callback=SetRadioChannelUp, bouncetime=250)

clamp = lambda n: max(min(100, n), 0)

no_curses_main()

