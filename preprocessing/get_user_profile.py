from __future__ import print_function
import os, sys
import os.path
from subprocess import call
import time, random
import re
import string
import gdata.youtube.service
import requests

def save_author(fname, author_name):
	print ("save")
	link = "https://gdata.youtube.com/feeds/api/users/" + author_name
	site = requests.get(link)
	k = fname+author_name
	print (k) 
	file = open(k,"w") #open file in binary mode
	file.writelines(site.text.encode('UTF-8'))
	file.close()

def main():
	print ("main")
	for f in os.listdir("testall"):
		print (f)
		call(["mkdir", "user_profile/" + f[0:7]])
		vlist = open("testall/" + f)
		for li in vlist:
			print (li)
			videolink = requests.get(li)
			author = ""
			if re.search("http://www.youtube.com/user/", videolink.text) > -1 :   # this is a general user
				author = re.search('href="http://www.youtube.com/user/(.+?)"', videolink.text).group(1)
				print (author)
			elif re.search("http://www.youtube.com/channel/", videolink.text) > -1 : # this is a channel
				author = re.search('href="http://www.youtube.com/channel/(.+?)"', videolink.text).group(1)
				print (author)
			save_author("user_profile/" + f[0:7] + "/", author)
		vlist.close()


if __name__ == "__main__":
    main()
