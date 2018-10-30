import os,sys,re
import random
from sklearn.feature_extraction.text import TfidfVectorizer

os.system("rm -r Sample_videos")

os.system("mkdir Sample_videos")
text_th = 0.05
num_seeds = 6  # select 6 subevents
from_date = 2457020
to_date = 2457039
#read in videos
video_list = {}
counter = 1
f_vlist = open('video_list')
all_lines = f_vlist.readlines()  
f_vlist.close()



#get event seed
lines = random.sample(all_lines, num_seeds)
for li in lines:
	temp = li.split(' ')
	if re.search('Chinese', temp[0]):
		video_name = temp[2][0:14]
	else:
		video_name = temp[2][0:11]
	print temp, video_name
	folder = temp[0]
	date = int(temp[1])
	begin_date= date-1
	end_date = date+1
	if begin_date < from_date:
		begin_date = from_date
	if end_date > to_date:
		end_date = to_date
	print begin_date, end_date
	#get match data
	data = []
	name_list = {}
	fp = open(temp[0] +'/' +temp[1]+ '/'+ video_name)
	name_list[0] = temp[0] +'/' +temp[1]+ '/'+ video_name
	data.append(fp.read())
	fp.close()
	count = 1
	for i in range(begin_date, end_date+1):
		for fi in os.listdir(folder + '/' + str(i)):
			filename = folder+'/' + str(i) + '/'+fi
			name_list[count] = filename
			count = count+1
			fp = open(filename)
			text = fp.readline()
			data.append(text)
			fp.close()
		print i
	#a = raw_input()
	vect = TfidfVectorizer(min_df=1)
	tfidf = vect.fit_transform(data)
	cosine=(tfidf * tfidf.T).A
	print cosine
	f_cluster = open('Sample_videos/Cluster_' +video_name, 'w')
	f_cluster.write(name_list[0] + ' ' + data[0]+ '\n')
	for i in range(1, len(cosine)):
		print cosine[i][0]
		if cosine[i][0] > text_th:
			f_cluster.write(name_list[i] + ' ' + data[i]+ '\n')
	a = raw_input()
	
