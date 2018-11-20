from __future__ import print_function
import os, sys
import os.path
from subprocess import call
import time, random
import re
import string
import gdata.youtube.service
import requests
from pylab import *
from scipy.stats.stats import pearsonr
#import gaussfitter as gau

def main():
	#print ("main")
	x = []
	y = []
	m = []
	n = []

	A = 0
	Z = 0
	for date in os.listdir("US_videos/"):
		print (date)
		#readin view count and pagerank (dictionary)
		dicview = {}
		fview = open("Viewcount/US/" + date)
		for view in fview:
			if view == "\n":
				continue
			#print (view)
			(key, val) = view.split()
       			dicview[key] = int(val)
		fview.close()
		fprank = open("Pagerank/US/"+date + "prank.txt")
		dicrank = {}
		for prank in fprank:		
			if prank == "\n":
				continue
			#print (prank)
			(key, val) = prank.split()
       			dicrank[key] = float(val)
		fprank.close()
		#print (dicrank)
		#read in clusters
		fcluster = open("Clusters_by_day/US_clusters/" + date + "Cluster.txt" )
		videoinfluence = {}   # video , sum of visual- meme influence
		clusterviewcount = {}   # visual - meme , average viewcount
		c_id = -1
		v_list = []
		for line in fcluster:
			if re.search("Cluster", line) > -1:
				if c_id == -1:
					c_id = int(re.search("Cluster(.+?):", line).group(1))
					continue
				elif c_id >= 0:
					#print (v_list)
					set_vlist = set(v_list)
					for v in set_vlist:
						#print (c_id)
						#print (dicrank[str(c_id)])
						# average cluster viewcount
						if c_id in clusterviewcount:
							clusterviewcount[c_id] += dicview[v]
							#clusterviewcount[c_id] = max(dicview[v], clusterviewcount[c_id])

						else:
							clusterviewcount[c_id] = dicview[v] 	
						#accumulate video influence
						if v in videoinfluence:
							#videoinfluence[v] += dicrank[str(c_id)]
							videoinfluence[v] = max(dicrank[str(c_id)], videoinfluence[v])

						else:
							videoinfluence[v] = dicrank[str(c_id)]
					clusterviewcount[c_id] = clusterviewcount[c_id] / len(v_list)
					v_list = []
					c_id = int(re.search("Cluster(.+?):", line).group(1))
		
			elif line == "" or line == "\n":
				continue
			else:
				v_list.append(re.search("24(.+?)/(.+?).mp4", line).group(2)) 			
		fcluster.close()
		finflu = open("Influence/US/" + date, 'w')
		for key, value in videoinfluence.items():
				finflu.write(str(dicview[key]) + " " + str(value)+"\n")
				x.append(dicview[key])
				y.append(value)
		finflu.close()
		#print (videoinfluence)
		k = pearsonr(x,y)
		A += k[0];
		#plt.plot(x,y)
		#plt.show()

		print (clusterviewcount)
		for key,value in clusterviewcount.items():
			m.append(dicrank[str(key)])
			n.append(value)
		k = pearsonr(n,m)
		Z += k[0]
	print(A/20.0)
	print(Z/20.0)
	fig1 = plt.gcf()
	#plt.xlim([0,1000000])
	plt.plot(log(n), log(m), 'ro')
	k = pearsonr(log(n),log(m)+1)
	#gau.multigaussfit(log(n), log(m),ngauss = 2)
	fdata = open("text.txt", 'w')
	for i in range(0, len(n)):
		fdata.write(str(log(n[i])) + " "+ str(log(m[i]))+ "\n")
	fdata.write("\n")

	fdata.close()
	print (k)
	plt.show()
	plt.draw()
	fig1.savefig('log_max_visual_meme_influence.png')
	fig2 = plt.gcf()
	#plt.xlim([0,1000000])
	plt.plot(log(x), log(y), 'ro')
	k = pearsonr(log(x),log(y))
	print (k)
	fdata = open("text1.txt", 'w')
	for i in range(0, len(x)):
		fdata.write(str(log(x[i])) + " "+ str(log(y[i]))+ "\n")
	fdata.write("\n")
	plt.show()
	plt.draw()
	fig2.savefig('log_video_influence.png')


	


if __name__ == "__main__":
    main()
