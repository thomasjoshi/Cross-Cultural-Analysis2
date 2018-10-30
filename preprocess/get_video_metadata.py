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
	for f in os.listdir("testall"):
		print (f)
		call(["mkdir", "video_metadata/" + f[0:7]])
		vlist = open("testall/" + f)
		for li in vlist:
			print (li)
			v_id = li[31:42]
			print (v_id)				
			link = 'https://gdata.youtube.com/feeds/api/videos/'+ v_id
			videolink = requests.get(link)
			k = "video_metadata/" + f[0:7] + "/"+v_id
			file = open(k,"w") #open file in binary mode
			file.writelines(videolink.text.encode('UTF-8'))
			file.close()
		vlist.close()


if __name__ == "__main__":
    main()


