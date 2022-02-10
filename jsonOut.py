import json
import numpy as np
import time

class output:
        def __init__ (self, exit_threshold, sitename, tracked_fish, classes, frame):
                self.sitename = sitename
                self.frame = frame
                self.detection = len(classes)
                self.exit_threshold = exit_threshold
                
                

        def outputLoop (self):
                sequential_frameID = 1
                while self.detection > 0:
                        sequential_frameID += 1
                        

class jsonOut:
	def __init__(self, sitename, INPUTS_FROM_TRACKER_HERE):
		self.dateTime =
		self.site = sitename
		self.species = 
		self.confidence =
		self.travelDirection = 
		self.fishLength =

	def writeFile (self):
		directory = 'outfile'
		filename = 
		json_file = {
			"dateTime":,
			"site":,
			"species":,
			"maxConfidence": np.float64(),
			"travelDirection":
		}

		with open("{}/{}.json".format(directory, filename), 'w') as f:
                json.dump(json_out, f)

	def writeFile_rs (self):
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




