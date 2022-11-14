
from RPi import GPIO
from curses import wrapper
import asyncio
import csv
import curses
import json
import os
import signal
import subprocess
import sys
import time, shlex

current_channel = 0

json_string = """
{ 
    "radio": [ 
        "mplayer -playlist http://www.ndr.de/resources/metadaten/audio/m3u/ndrinfo.m3u"
        , "mplayer https://st01.dlf.de/dlf/01/128/mp3/stream.mp3"
        , "mplayer https://wdr-wdr5-live.icecastssl.wdr.de/wdr/wdr5/live/mp3/128/stream.mp3"
        , "mplayer http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"
    ],
    "amixer": "Headphone",
    "current": 0,
    "volume": 60
} 
"""

data = json.loads(json_string)

CLK = 5
DT = 7
SW = 32

def RotButton(dummy):
    SetRadioChannelUp()

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

def SetRadioChannelIndex(c):
    data["current"] = c
    SetRadioChannel()

def SetRadioChannelUp():
    data["current"] = ( data["current"] + 1 ) % len(data["radio"])
    SetRadioChannel()
    
def SetRadioChannelDown():
    data["current"] = ( data["current"] - 1 + len(data["radio"])) % len(data["radio"])
    SetRadioChannel()

def cleanup():
    os.system("pkill mplayer");
    curses.nocbreak()
    # screen.keypad(0)
    curses.echo()
    curses.endwin()
    GPIO.cleanup()
    sys.exit()

def main():
    SetRadioChannelIndex(data["current"])

    damn = curses.initscr()
    damn.nodelay(1)
    while True:
        c = damn.getch()
        if c > 1:
            print("<" + str(c) + ">")
        if c == 122: # 'z'
            cleanup()
        if c == 109: # 'm'
            SetRadioChannelUp()
        if c == 110: # 'n'
            SetRadioChannelDown()
        if c == 120: # 'x'
            applyVolume(data["volume"] + 4)
        if c == 121: # 'y'
            applyVolume(data["volume"] - 4)

def no_curses_main():
    SetRadioChannelIndex(data["current"])
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
GPIO.add_event_detect(SW, GPIO.FALLING, callback=RotButton, bouncetime=250)

# Clamp value btw 0 and 100
clamp = lambda n: max(min(100, n), 0)

no_curses_main()

