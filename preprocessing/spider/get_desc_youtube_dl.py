import string
import gdata.youtube.service
import requests
import os
from subprocess import call
import subprocess


def main():
	print ("main")
	for fdate in os.listdir("US_videos"):
		print (fdate)
		call(["mkdir", "US_text/" + fdate[0:7]])
		for fi in os.listdir("US_videos/" + fdate):
			print (fi)
			v_id = fi[0:11]
			#print (v_id)

			#check if the v
			desccmd = "youtube-dl --get-description "+v_id
			try:
				desc = subprocess.check_output(desccmd, shell=True)
			except Exception, e:
				desc = ""
			titlecmd = "youtube-dl --get-title "+v_id
			try:
				title = subprocess.check_output(titlecmd, shell=True)
			except Exception, e:
				title = ""
			print title, desc
			#a = raw_input()
			dfile = open("US_text/"+fdate[0:7]+"/"+v_id, 'w')
			dfile.write(title)
			dfile.write(desc)
			dfile.close()

			#os.system("youtube-dl --write-sub --max-filesize 100m -o US_video/"+f[0:7]+"/"+v_id + "  " + v_id)


if __name__ == "__main__":
    main()
