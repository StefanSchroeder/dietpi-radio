# Raspberry-Pi radio

This project builds a radio with a raspberry-pi type SBC and
a couple of controls, namely a volume control and channel control.

# Dietpi 

Download:

	wget https://dietpi.com/downloads/images/DietPi_RPi-ARMv6-Bullseye.7z

Extract

	7z x DietPi_RPi-ARMv6-Bullseye.7z

Check the drivename of your SDcard

	lsblk

Install on SDcard. 

	dd if=DietPi_RPi-ARMv6-Bullseye.img of=/dev/mmcblk0 bs=4M status=progress

Mount the first partition on the SD-card

	mount /dev/mmcblk0p1 /mnt

Set your keyboard

	sed -i 's/AUTO_SETUP_KEYBOARD_LAYOUT=gb/AUTO_SETUP_KEYBOARD_LAYOUT=de/' /mnt/dietpi.txt

Enable WiFi

	sed -i 's/AUTO_SETUP_NET_WIFI_ENABLED=0/AUTO_SETUP_NET_WIFI_ENABLED=1/' /mnt/dietpi.txt

Set WiFi-Country Code

	sed -i 's/AUTO_SETUP_NET_WIFI_COUNTRY_CODE=GB/AUTO_SETUP_NET_WIFI_COUNTRY_CODE=DE/' /mnt/dietpi.txt

Set hostname

	sed -i 's/AUTO_SETUP_NET_HOSTNAME=DietPi/AUTO_SETUP_NET_HOSTNAME=radio/' /mnt/dietpi.txt

Fix Timezone (optional)

	sed -i 's/London/Berlin/' /mnt/dietpi.txt

Disable HDMI output

	sed -i 's/AUTO_SETUP_HEADLESS=0/AUTO_SETUP_HEADLESS=1/' /mnt/dietpi.txt

Set Wifi-Credentials

	sed -i 's/aWIFI_SSID[0]=''/aWIFI_SSID[0]='MyWifiName' /mnt/dietpi-wifi.txt
	sed -i 's/aWIFI_KEY[0]=''/aWIFI_KEY[0]='12345678901234567890123456789' /mnt/dietpi-wifi.txt

Eject SD-card

	umount /mnt

Gateway: Now you have a pre-configured SD-card. 

Plug into device. Power up.

There is more than one way to determine the IP address of the device after it successfully connected to the network.

- You can login to your router and determine the device.
- You can scan the network (from another computer to find the device as soon as it shows up) using a tool like 'nmap':

	sudo nmap -v -sn 192.168.0.0/24 

This can be tiresome if there is a lot going on in your network. Therefore it is recommended to note down the
MAC-address of your device the first time you have unambiguously identified your device.

Wait for this command to succeed. Retrieve the IP address.

Log into the machine using the default credentials.

	ssh root@radio # with default password 'dietpi'

After the first login, there are some updates that 
will likely lead to a reboot because of an updated kernel.
Your session will interrupted and you have to re-login
after the system has restarted:

	ssh root@radio # with default password 'dietpi'

Change the default password

	passwd

Update the package database

	apt update

Install a few commands that we use

	apt install -y mplayer git python3 alsa-utils python3-rpi.gpio

Configure Audio (for Raspberry's with audio jack):

	dietpi-config

	Enable Audio -> Select Onboard 3.5 mm bcm2835

After configuring the audio. The device will be rebooted once more.

Note: Sound card = rpi-bcm2835-3.5mm

## Gateway (Audio)

At this point you should be able to play audio.

Test with 

	mplayer https://reckhorn.com/media/music/Test-1.wav

This will play some drums. If it doesn't, don't continue.

## Debugging Audio

To debug, the following tools are helpful:

*amixer* will provide information about the soundcard.

*alsamixer* will allow you to control the volume. Set to 100% initially.
	
## Installing the radion application

Clone the radio repo

	git clone https://github.com/StefanSchroeder/dietpi-radio.git

	cd dietpi-radio

	cp radio.service /etc/systemd/system

	systemctl enable radio.service

## Usage

If you happen to start *radio.py* from the commandline, the program
can be controlled via keyboard:
   
x,y for volume.

m,y for channel selection

z quit

But usually (after being started via crontab) controlling via keyboard
is not possible nor desired. Use the rotary encoder to control the
volume. Press the knob to switch to the next channel.

# OPEN POINTS

- Hifiberry-support
- Preinstall application
- Autoupdate

