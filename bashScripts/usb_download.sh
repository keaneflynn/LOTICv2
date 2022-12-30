#!/bin/bash

SOURCE_FOLDER='/home/garcia/LOTIC/LOTICv2/outfile'
DESTINATION_FOLDER='/media/garcia/T7'
SITENAME='site1' #UPDATE WITH SITENAME FOR EACH UNIQUE COMPUTER
FILENAME=$(date '+%m-%d-%y_%H-%M-%S')_$SITENAME
FLASH_CHECK=$(lsusb | grep 'Samsung' | wc -l)
DIRECTORY_CHECK=$(ls $SOURCE_FOLDER | wc -l)

if [[ $FLASH_CHECK -gt 0 ]]
then
	if [[ $DIRECTORY_CHECK -lt 5 ]] #THRESHOLD FOR FILE TRANSFER IS 5 FILES CURRENTLY
	then
		echo 'No files to transfer'
		udisksctl unmount -b /dev/sda1
		udisksctl power-off -b /dev/sda1
		exit 0
	else
	mv $SOURCE_FOLDER/* $DESTINATION_FOLDER
	systemctl status usb_download.service >> $DESTINATION_FOLDER/systemStatus.log
	fi
else
	echo 'No USB drive detected'
	exit 0
fi

cd $DESTINATION_FOLDER
zip -q $FILENAME *.avi *.json *.log
rm *.avi && rm *.json && rm *.log 

cd ~/ 
udisksctl unmount -b /dev/sda1 
udisksctl power-off -b /dev/sda1 
exit 0

