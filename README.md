# imac_brightness

An iMac autbrightness daemon for the display, ready to be built as a package in Arch Linux. The script is built and tested on my iMac19,1. Adapted to run on CachyOS.

clone the git:

git clone https://github.com/DerNoli/imac_brightness

then cd into the directory by typing:

cd imac_brightness

when you are in the directory, just type:

makepkg -si

enable the service with:

sudo systemctl enable --now autobrightness
