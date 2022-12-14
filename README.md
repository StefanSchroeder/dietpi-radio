# Raspberry-Pi Radio

This project builds a radio with a raspberry-pi type SBC and
a rotary encoder to  control the volume and channel.

## Prior art

- https://blog.sharedove.com/adisjugo/index.php/2020/05/10/using-ky-040-rotary-encoder-on-raspberry-pi-to-control-volume/
- https://www.instructables.com/Raspberry-Pi-Radio/

# Install Dietpi 

Download:

	wget https://dietpi.com/downloads/images/DietPi_RPi-ARMv6-Bullseye.7z

Extract

	7z x DietPi_RPi-ARMv6-Bullseye.7z

Insert SD-card and find the drivename of your SD-card

	lsblk
or
	dmesg

Install on SDcard. 

	dd if=DietPi_RPi-ARMv6-Bullseye.img of=/dev/mmcblk0 bs=4M status=progress

Mount the first partition of the SD-card

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

	sed -i 's/aWIFI_SSID\[0\]=\x27\x27/aWIFI_SSID[0]=\x27MyWifiName\x27/' /mnt/dietpi-wifi.txt
	sed -i 's/aWIFI_KEY\[0\]=\x27\x27/aWIFI_KEY[0]=\x27MySuperSecretWifiPassword\x27/' /mnt/dietpi-wifi.txt
	
Note: The square brackets must be quoted. The single quotes must be
written as \x27 to not interfere with the quoting.

Eject SD-card

	umount /mnt

## SD-card is ready to launch!

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
may lead to a reboot because of an updated kernel.
Your ssh-session will be interrupted and you have to re-login
after the system has restarted:

	ssh root@radio # with default password 'dietpi'

When you login, the system will ask you to do some maintenance.

You can now change the default passwords, update the package-database,
decline the invitation to participate in a survey, etc.

Update the package database

	apt update

Configure Audio (for Raspberry's with audio jack):

	dietpi-config

	Enable Audio -> Select Onboard 3.5 mm bcm2835

Cmdline:

	/boot/dietpi/func/dietpi-set_hardware rpi-bcm2835-3.5mm

After configuring the audio. The device will be rebooted once more.

Note: Sound card = rpi-bcm2835-3.5mm

Install a few commands that we use

	apt install -y mplayer git python3-rpi.gpio

The required package *alsa-utils* will have been installed already
when configuring the audio. *python3* will be installed as a
dependency of *python3-rpi.gpio*. 

## Gateway (Audio)

At this point you should be able to play audio.

Test with 

	mplayer https://reckhorn.com/media/music/Test-1.wav

This will play some drums. If it doesn't, don't continue.

## Debugging Audio

To debug audio, the following tools are helpful:

*amixer* will provide information about the soundcard.

*alsamixer* will allow you to control the volume. Set to 100% initially.

## Installing the radion application

Clone the radio repo (we are in /root)

	git clone https://github.com/StefanSchroeder/dietpi-radio.git

	cp dietpi-radio/radio.service /etc/systemd/system

	systemctl enable radio.service
	systemctl start radio.service

## Usage

After the next reboot the radio application will automatically start.

Use the rotary encoder to control the volume. Press the knob to switch
to the next channel.

The URLs of radio channels are listed in the JSON file.  The *current*
variable indicates the initial channel (starting with 0).  The
*volume* variable indicates the initial volume.  The *amixer* variable
indicates the name of the audio device as indicated by the *amixer*
command.

# OPEN POINTS

- Hifiberry-support
- Preinstall application
- Autoupdate
- PiZero support 

