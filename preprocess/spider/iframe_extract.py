from __future__ import print_function
import os, sys
import os.path
from subprocess import call
import time, random
import re
import string
import gdata.youtube.service
import requests
import time


def main():
	print ("main")
	for f in os.listdir("Chinese_videos"):
		print (f)
		for li in os.listdir("Chinese_videos/"+f):
			print (li)
			if re.search('.en.srt', li) > -1:
				print ("subtitle file")
				continue
			else:
				#os.system("mv "+"_video/"+f+"/"+li + " " +"US_video/"+f+"/"+li+".mp4" )
				os.system("../script/DC_component/src/extract" + "  " + "Chinese_videos/"+f+"/" + "  " +li )


if __name__ == "__main__":
    main()
