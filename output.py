import json
import numpy as np
import datetime as datetime

class jsonOut:
	def __init__(self, sitename, names_file):
		self.site = sitename
		self.class_names = []
		with open(names_file, "r") as f:
			self.class_names = [cname.strip() for cname in f.readlines()]

	def writeFile(self, evicted_fish, travel_direction):
		for fish in evicted_fish:
			json_data = [datetime.datetime.utcnow(), 
		  				 self.site, 
		  				 self.class_names[fish.fish_id], 
		  				 fish.max_confidence,
		  				 travel_direction]

		directory = 'outfile'
		filename = 
		json_file = {
			"dateTime":json_data[0],
			"site":json_data[1],
			"species":json_data[2],
			"maxConfidence": np.float64(json_data[3]),
			"travelDirection": json_data[4]
		}

		with open("{}/{}.json".format(directory, filename), 'w') as f:
            json.dump(json_out, f)


class jsonOut_rs:
	def __init__(self, sitename, INPUTS_FROM_TRACKER_HERE):
		self.dateTime = 
		self.site = sitename
		self.species = 
		self.confidence =
		self.travelDirection = 
		self.fishLength =

	def jsonOutputUpdate_rs(self):

	def writeFile_rs(self):
		directory = 'outfile'
		filename = 
		json_file = {
			"dateTime":,
			"site":,
			"species":,
			"maxConfidence": np.float64(),
			"travelDirection":,
			"fishLength_mm": np.float64()
		}

		with open("{}/{}.json".format(directory, filename), 'w') as f:
			json.dump(json_out, f)


class output:
	def __init__(self, exit_threshold, sitename, classes, frame):
		self.sitename = sitename
		self.frame = frame
		self.detection = len(classes)
		self.exit_threshold = exit_threshold
                       

	def outputLoop(self, tracked_fish):
		outfileID = 0
		frames_since_detection = 0
		while grabbed: #Condition: video frame is successfully imported 
			outfileID += 1
			vid_outfileName = os.path.join()
			json_outfileName = os.path.join()
			started = False
			while grabbed: #Condition: video frame is successfully imported & filenames for outfiles are updated

				fish_detected = len(classes) > 0
				
				if started: #Condition: frame following first frame with detected fish
					if fish_detected: #Condition: frame following frame with detected fish has detected fish
						videoWrite.write()
						jsonOutputUpdate()
						frames_since_detection = 0
					else: #Condition: frame following frame with detected fish has no fish detected
						frames_since_detection += 1
						videoWrite.write()
						if frames_since_detection > exitThresholdFPS: #Condition: no detection & number of frames since detection is greater than set exit threshold
							videoWrite.release()
							frames_since_detection = 0
							break
						else: #Condition: no detection & number of frames since detection is less than set exit threshold 
							pass

				else: #Condition: frame imported when started =/= True
					if fish_detected: #Condition: First frame imported with fish detection
						started = True
						videoWrite = cv2.videowriter(INSERTINFOHERE)
						jsonOutputUpdate()
						
					else: #Condition: Any video frame imported with no fish detection
						pass 
                        
