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
	targetDIR = "../video_metadata/"
	#UKDIR = "../Europe_videos/" 
	USDIR = "../US_videos/" 
	for f in os.listdir(targetDIR):
		print (f)
		call(["mkdir", "../US_videos/" + f])
		#call(["mkdir", "../Europe_videos/" + f])
		for li in os.listdir(targetDIR + f):
			#print (li)
			fv = open(targetDIR + f + "/" + li)
			v_content = fv.read();
			fv.close()

			author = ""
			if re.search('https://gdata.youtube.com/feeds/api/users/(.+?)</uri>', v_content) >-1 :   # this is a general user
				author = re.search('https://gdata.youtube.com/feeds/api/users/(.+?)</uri>', v_content) .group(1)
				#print (author)
			if author =="":
				continue
			#get author location
			file_path = "../user_profile/" + f + "/" + author
			if not os.path.exists(file_path):
				continue
			fa = open(file_path)
			usrinfo = fa.read()
			fa.close()

			location = ""
			if re.search("<yt:location>(.+?)</yt:location>", usrinfo) is None:
				continue
			location = re.search("<yt:location>(.+?)</yt:location>", usrinfo).group(1)
			if location == "US":
				#print ("cp -r ../All_videos/" + f + "/" + li + ".mp4_ffmpeg_iframes" +  "  "  + USDIR + f + "/" + li + ".mp4_ffmpeg_iframes")
				os.system("cp -r ../All_videos/" + f + "/" + li + ".mp4_ffmpeg_iframes" +  "  "  + USDIR + f + "/")
			#elif (location == "GB" or location == "FR") or location == "DE":
			#	#print ("cp -r ../All_videos/" + f + "/" + li + ".mp4_ffmpeg_iframes" +  "  "  + UKDIR + f + "/" + li + ".mp4_ffmpeg_iframes")
			#	os.system("cp -r ../All_videos/" + f + "/" + li + ".mp4_ffmpeg_iframes" +  "  "  + UKDIR + f + "/")
			else: 
				continue


						


if __name__ == "__main__":
    main()
