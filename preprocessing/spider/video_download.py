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
		call(["mkdir", "video/" + f[0:7]])
		vlist = open("testall/" + f)
		for li in vlist:
			print (li)
			v_id = li[31:42]
			#print (v_id)
			os.system("youtube-dl --all-subs --max-filesize 100m -o US_video/"+f[0:7]+"/"+v_id + "  " + v_id)
		vlist.close()				


if __name__ == "__main__":
    main()
