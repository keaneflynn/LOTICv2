import json
import numpy as np
import datetime as datetime
import cv2
import queue
import os

class jsonOut:
	def __init__(self, sitename, names_file, outfile_directory):
		self.site = sitename
		self.class_names = []
		self.directory = outfile_directory
		os.makedirs(self.directory, exist_ok=True)

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

			filename = json_data[5]+'_'+json_data[1]+'_'+json_data[2]+'-'+str(json_data[6])
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
	def __init__(self, sitename, names_file, outfile_directory):
		self.site = sitename
		self.class_names = []
		self.directory = outfile_directory
		os.makedirs(self.directory, exist_ok=True)

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

			filename = json_data[5]+'_'+json_data[1]+'_'+json_data[2]+'-'+str(json_data[6])
			json_file = {
				"dateTime":str(json_data[0]),
				"site":json_data[1],
				"species":json_data[2],
				"maxConfidence": np.float64(json_data[3]),
				"travelDirection": json_data[4],
				"fishLength_mm": json_data[5]
				}	
			with open("{}/{}.json".format(self.directory, filename), 'w') as f:
				json.dump(json_file, f)


class videoOutput:
	def updateFilename(self):
		time = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
		self.outfile_name = self.outfile_dir+time+'_'+self.sitename+'_'+str(self.outfile_id)+'.avi'

	def writeFrames(self):
		self.output = cv2.VideoWriter(self.outfile_name, self.fourcc, self.fps, (self.frame_width, self.frame_height))

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
		self.buffer_size = 10 #can only seem to get 10 frames on the realsense camera before running into a buffer issue, no matter the frame size
		self.video_buffer = queue.Queue(self.buffer_size) #gives you x amount frames before the fish shows up after the first detection


	def writeVideo(self, tracked_fish, frame):
		self.video_buffer.put(frame)
		if self.video_buffer.qsize() == self.buffer_size:
			lag_frame = self.video_buffer.get() 

			if (len(tracked_fish) > 0) and (self.counter == 0):
				self.writeFrames()
				self.output.write(lag_frame)
				self.counter = 1
			
			if len(tracked_fish) > 0: 
				self.counter = 1
				self.output.write(lag_frame)
			elif self.counter in range(1, (self.exit_threshold+self.buffer_size+1)): 
				self.output.write(lag_frame)
				self.counter+=1
			elif self.counter == self.exit_threshold+self.buffer_size+1:
				self.counter+=1
				self.outfile_id+=1
				self.updateFilename()
			else:
				self.counter = 0
				self.updateFilename()
		else:
			pass
