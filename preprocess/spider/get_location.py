from __future__ import print_function
import os, sys
import os.path
from subprocess import call
import time, random
import re
import string
import gdata.youtube.service
import requests
from collections import Counter




def main():
	locate = []
	print ("main")
	for f in os.listdir("user_profile/"):
		print (f)
		vlist = "user_profile/" + f + "/"
		for li in os.listdir(vlist):
			print (li)
			k = "user_profile/" + f + "/"+li
			file = open(k,"r") #open file in binary mode
			location = re.search("<yt:location>(.+?)</yt:location>", file.read()).group(1)
			locate.append(location)
			file.close()
	
	counts = Counter(locate)
	print(counts)


if __name__ == "__main__":
    main()
