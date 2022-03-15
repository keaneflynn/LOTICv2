import json
import numpy as np
import datetime as datetime
import cv2

class jsonOut:
	def __init__(self, sitename, names_file, outfile_directory):
		self.site = sitename
		self.class_names = []
		self.directory = outfile_directory
		with open(names_file, "r") as f:
			self.class_names = [cname.strip() for cname in f.readlines()]

	def writeFile(self, evicted_fish, travel_direction):
		for fish in evicted_fish:
			json_data = [datetime.datetime.utcnow(), 
		  				 self.site, 
		  				 self.class_names[fish.class_id], 
		  				 fish.max_confidence,
		  				 travel_direction,
						 datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S"),
						 fish.fish_id]

			filename = json_data[2]+'-'+str(json_data[6])+'_'+json_data[5]
			json_file = {
				"dateTime":str(json_data[0]),
				"site":json_data[1],
				"species":json_data[2],
				"maxConfidence": np.float64(json_data[3]),
				"travelDirection": json_data[4]
				}	
			with open("{}/{}.json".format(self.directory, filename), 'w') as f:
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
	def __init__(self, sitename, exit_threshold, video_info, outfile_directory):
		self.exit_threshold = int(exit_threshold * video_info[0])
		self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
		self.fps = video_info[0]
		self.frame_width = int(video_info[1])
		self.frame_height = int(video_info[2])
		self.counter = 0
		self.sitename = sitename
		self.outfile_id = 0
		self.outfile_dir = outfile_directory
		
		time = datetime.datetime.now().strftime("%m-%d-%Y")
		outfile_name = self.outfile_dir+time+'_'+self.sitename+'_'+str(self.outfile_id)+'.avi'
		self.output = cv2.VideoWriter(outfile_name, self.fourcc, self.fps, (self.frame_width, self.frame_height))

	def writeVideo(self, tracked_fish, frame):
		if len(tracked_fish) > 0:
			self.output.write(frame)
			self.counter = 1
		else:
			if self.counter in range(1,self.exit_threshold+1):
				self.output.write(frame)
				self.counter+=1
			elif self.counter == self.exit_threshold+1:
				self.counter+=1
				self.outfile_id+=1
				time = datetime.datetime.now().strftime("%m-%d-%Y")
				outfile_name = 'outfile/'+time+'_'+self.sitename+'_'+str(self.outfile_id)+'.avi'
				self.output = cv2.VideoWriter(outfile_name, self.fourcc, self.fps, (self.frame_width, self.frame_height))
			else:
				self.counter = 0
				time = datetime.datetime.now().strftime("%m-%d-%Y")
				outfile_name = 'outfile/'+time+'_'+self.sitename+'_'+str(self.outfile_id)+'.avi'
				self.output = cv2.VideoWriter(outfile_name, self.fourcc, self.fps, (self.frame_width, self.frame_height))

