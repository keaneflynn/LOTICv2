# LOTICv2
Welcome to the updated version of LOTIC (Lightweight Object Tracking Image Capturer)!
This updated version of the software is designed for used with the Nvidia Jetson Xavier NX with an internet protocol (IP) camera.
This build is currently in progress but should be finished by early spring 2022.
Our goal is to have this program able to process up to 30 fps with YOLOv4 tiny models and 12-15 fps with full-sized YOLOv4 models.
We want to make this build available for the Jetson Nanos in the future to make this hardware setup even cheaper.

## GitHub Build Protocol
For contributors for editing process:
Open your terminal and move into your local repository using ` cd ~/LOTICv2 `
```
git fetch origin
git reset --hard origin/main
git checkout -b TemporaryBranchName
```
Then go ahead and make whatever edits in your session you want to make, then continue to the following commands:
```
git add .
git commit -m "thoughtful commit message"
git push origin TemporaryBranchName
```
Proceed to make a pull request on the GitHub UI and I will merge the pull request. 

Final step from terminal:
```
git checkout main
git branch -D TemporaryBranchName
git pull
```

## Introduction
This repository was created and designed by Keane Flynn, Ryan Flynn, Jack Rogers, and Gabriel Rossi to provide an open-source program to be paired with low-cost hardware which can be used in freshwater fisheries monitoring to detect, speciate, and record migratory fish in rivers. Based off of the [original LOTIC repository](https://github.com/keaneflynn/LOTIC), this program works with YOLO (you only look once) object detection methods (Redmond et al. 2016) combined with a SORT based object tracker to identify individual fish over the duration of a video in which they are detected. This program was designed as an alternative to downstream/upstream migrant trapping to alleviate stress on fishes and reduce the amount of fieldwork required to collect necessary data for monitoring programs. This is **not** intended to replace people, there are plenty of situations where human effort will outperform this program (i.e. turbid conditions). 


![Detection of juvenile coho salmon in Woods Creek](https://github.com/keaneflynn/LOTICv2/blob/main/media/cohoGif.gif)


## Necessary Hardware
- Nvidia Jetson Xavier NX (has not been tested, but should probably work on an AGX if you can get one)
- External camera (will work with any camera source, but designed around use for an IP camera or Intel Realsense Camera)
- Power source (can be powered from stock jetson power supply or from solar -> 19v supply for standalone unit)
- Additional storage for output videos (Nvidia Jetson Xavier's can be outfitted with M.2 SSDs for fast write speeds)
- Weir environment to channel migrating fishes (not necessary, but a sterile environment will improve detection efficiency)

## Setting Up on the Nvidia
To allow for this program to run on startup, place the [service file](https://github.com/keaneflynn/LOTICv2/blob/main/lotic.service) in /etc/systemd/system/. Then issue the following command: ``` sudo systemctl enable lotic ``` to enable the service file to work on startup, and if the service file is modified in any way you must issue the following command ``` sudo systemctl daemon-reload ```. Finally, to start it before leaving the computer unattended, issue the following command: ``` sudo systemctl restart lotic ```. 
This series of commands will allow the service file to operate on startup and restart itself if the computer or program shuts down unexpectedly (i.e. power loss, camera input crash, etc.). 
To check to make sure the program is up and running while logged into the Jetson, issue the following command: ``` systemctl status lotic.service ```.
Any errors with the program will be output to an error log file which by default is located in the *errorLogs* directory, but the location can be adjusted in the lotic.service file.

## Python program
To run the python program (command will be embedded in the service file for continuous operation), issue the following command to view positional (required) arguments for program to run ``` python main.py -h ```
An example of what this string of commands looks like would be as follows:
``` 
python3 main.py ./media/coho-steelhead-test.mov ./models/yolov4-tiny-fish.weights ./models/yolov4-tiny-fish.cfg ./models/yolov4-tiny-fish.names TestSite RR 0.25 2 ./outfile/ 
```

## Upcoming fixes
The current repository is functional but it is very much a beta with upcoming updates:
- Multithreading the video input: this will allow for reduced latency on the main detection loop and improve IP camera functionality
- Adding an option to draw bounding boxes on output videos: this will be better for demonstration purposes, not adding these will allow the output videos to be used to inform future neural network training for model tweaks.
- Adding a video frame queue for the video output: this will allow for the video output to contain a few frames before the first fish detection. This can be helpful in less than optimal conditions to have more frames containing fish. If using this, make sure to check for ram usage under load, can potentially throttle the program or result in a segmentation fault if the queue is too large.

## Acknowledgements
There are so many people to thank for this program coming to fruition. First and foremost, my older brother Ryan has given me most of my coding knowledge and has directly helped on both the original LOTIC repository as well as this one and none of this could have been done without him. Secondly, the research group from UC Berkeley, namely Dr. Gabriel "the fundraiser" Rossi, who has helped with every step of this project including but now limited to: funding, landowner access, collaboration across multiple agencies, moral support, & a bunch of other stuff. Jack Rogers, who has been a tremendous help in integrating the object tracking component into LOTICv2 in a very timely manner despite being a few timezones away and having to decipher my half-ass python skills. My last thank you in terms of individual people goes out to my boy Florida-Man Pete who works at Nvidia and has provided a lot of very useful insight in hardware recommendations and software suggestions to get the ball rolling on this project.

I would also like to thank CalTrout for funding my time working on this project so that it may be used by any agency needing to monitor migratory fish remotely, the north coast division led by Darren Mierau has been incredibly helpful and inspiring in promoting advancements in fisheries technology. The Grantham and Carlson Labs from UC Berkeley were integral in funding the first iteration of LOTIC and it would have never gotten to where it is without their support. I would like to thank the Aquatic Ecosystems Analysis lab at UNR for assisting in my research on this topic and allowing me to pursue it for the second chapter of my master's thesis. Lastly, I would like to thank the Summit Lake Paiute Tribe for allowing me to launch the test version of this system on their reservation and assisting with its integration to monitor the threatened Lahontan cutthroat trout population.

