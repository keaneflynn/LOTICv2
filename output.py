import json
from turtle import width
import numpy as np
import datetime as datetime

class jsonOut:
	def __init__(self, sitename, names_file):
		self.site = sitename
		self.class_names = []
		with open(names_file, "r") as f:
			self.class_names = [cname.strip() for cname in f.readlines()]

	def writeFile(self, evicted_fish, travel_direction, output_directory):
		for fish in evicted_fish:
			json_data = [datetime.datetime.utcnow(), 
		  				 self.site, 
		  				 self.class_names[fish.class_id[0]], 
		  				 fish.max_confidence,
		  				 travel_direction,
						 datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S"),
						 fish.fish_id]

			directory = output_directory
			filename = json_data[2]+'-'+str(json_data[6])+'_'+json_data[5]
			json_file = {
				"dateTime":str(json_data[0]),
				"site":json_data[1],
				"species":json_data[2],
				"maxConfidence": np.float64(json_data[3]),
				"travelDirection": json_data[4]
				}	
			with open("{}/{}.json".format(directory, filename), 'w') as f:
				json.dump(json_file, f)


class jsonOut_rs:
	def __init__(self, sitename, names_file):
		self.site = sitename
		self.class_names = []
		with open(names_file, "r") as f:
			self.class_names = [cname.strip() for cname in f.readlines()]

	def writeFile_rs(self):
		for fish in evicted_fish:
			json_data = [datetime.datetime.utcnow(), 
		  				 self.site, 
		  				 self.class_names[fish.class_id[0]], 
		  				 fish.max_confidence,
		  				 travel_direction,
						 datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S"),
						 fish.fish_id]

			directory = output_directory
			filename = json_data[2]+'-'+str(json_data[6])+'_'+json_data[5]
			json_file = {
				"dateTime":str(json_data[0]),
				"site":json_data[1],
				"species":json_data[2],
				"maxConfidence": np.float64(json_data[3]),
				"travelDirection": json_data[4],
				"fishLength_mm": json_data[5]
				}	
			with open("{}/{}.json".format(directory, filename), 'w') as f:
				json.dump(json_file, f)


class videoOutput:
	def __init__(self, exit_threshold, video_info):
		self.exit_threshold = exit_threshold
		self.fourcc = cv2.VideoWriter_fourcc(*'MPEG')
		self.fps = video_info[0]
		self.frame_width = video_info[1]
		self.frame_height = video_info[2]

	def writeVideo(self, frame):
		time = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
		outfile_name = 'video'+time+'.avi'
		output = cv2.VideoWriter(outfile_name, self.fourcc, self.fps, (self.frame_width, self.frame_height))
		output.write(frame)
