#!/bin/bash

checksudo=$(whoami)
if [ $checksudo != root ];then 
	echo "You need to run this install script as root or using sudo"
	exit 0
fi
echo -e "Checking for aplay sound player...\n"
which aplay >/dev/null
exitcode=$?
if [ $exitcode = 1 ] ; then
	echo -e "aplay not found, installing aplay...\n"
	apt-get install also-utils
elif [ $exitcode = 0 ]; then
	echo -e "aplay found in $(which aplay)\n"
fi

echo -e "Copying sounds to /usr/share/sounds/fruitplayer...\n"
mkdir -p /usr/share/sounds/fruitplayer/
cp -v *.wav /usr/share/sounds/fruitplayer/

echo -e "\nCopying fruitplayer binary to /usr/bin/...\n"
cp -v fruitplayer /usr/bin/

echo -e "\nDone. You can now delete this directory\n"

echo -e "To run fruitplayer, type \"fruitplayer\" into your terminal\n"
echo -e "Hit w a s d f or g on your keyboard to play the sounds\n"
echo -e "Press the UP or DOWN arrows to switch between piano and mario modes respectively\n"
echo -e "Press the UP arrow and then [space] to announce your ip address"
echo -e "To exit fruitplayer, Press [space] or press CTRL+C"
