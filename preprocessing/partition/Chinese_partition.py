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
	targetDIR = "../All2_videos/"
	#UKDIR = "../Europe_videos/" 

	for f in os.listdir(targetDIR):
		print (f)
		call(["mkdir", "../Chinese_videos/" + f])
		#call(["mkdir", "../Europe_videos/" + f])
		for li in os.listdir(targetDIR + f):
			if re.search("ffmpeg", li) > -1 :
				os.system("cp -r ../All2_videos/" + f + "/" + li  +  "  "  + "../Chinese_videos/" + f + "/")


						


if __name__ == "__main__":
    main()
