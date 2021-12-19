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
