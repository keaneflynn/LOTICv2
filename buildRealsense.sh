#!/bin/bash

echo 'cloning into JetsonHacks Realsense build' #Huge shoutout to them for making this an easy process
git clone https://github.com/jetsonhacks/installRealSenseSDK.git

cd installRealsenseSDK
echo 'changing file permissions'
chmod 755 ./buildLibrealsense.sh #might have to change file permissions to run, just to be safe

./buildLibrealsense.sh

cd ..
rm -rf installRealSenseSDK librealsense #cleaning up

echo 'Realsense build complete. To verify install success, try to import pyrealsense2 in python. If no module found error occurs, the PYTHONPATH variable in the .bashrc might need to be modified to the following path: /usr/local/lib/python3.6/librealsense2'
