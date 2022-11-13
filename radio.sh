#!/usr/bin/bash

while true; do
	p=$(pidof mplayer)
	if [ -z "$p" ]; then
		/usr/bin/python3 /root/dietpi-radio/radio.py
	fi
	sleep 10
done


