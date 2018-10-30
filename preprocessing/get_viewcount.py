from __future__ import print_function
import os, sys
import os.path
from subprocess import call
import time, random
import re
import string
import gdata.youtube.service
import requests

def main():
	print ("main")
	
	for date in os.listdir("US_videos/"):
		print (date)
		fview = open("Viewcount/US/" + date, 'w')

		#date = "2457029"
		for v_id in os.listdir("video_metadata/" + date):
			ff = open("video_metadata/" + date + "/" + v_id)
			temp = ff.read()
			if re.search('viewCount=(.+?)/>', temp)  is None:
				print (date), (v_id)
				continue 
			viewcount = re.search('viewCount=\'(.+?)\'/>', temp).group(1)

			fview.write (v_id + "  "  +  viewcount + "\n")
		fview.close()



if __name__ == "__main__":
    main()
