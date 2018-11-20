import os,sys,re
import nltk
import scipy.io
import numpy as np
import codecs
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

lmtzr = WordNetLemmatizer()
doc = {}
doc_count = 0
doc_name = {}
keyword_table = {}
keyword_count = 0
target_folder = '../../../US_text'
translated_folder = '../../../Chinese_desc_translated'
category_lable = {}
# read in documents
fvlist = open('../../used_video_list')
#for folder in os.listdir(target_folder):
#    for fi in os.listdir(target_folder + "/" + folder):
        #vname = re.search("(.+?).txt",fi).group(1)
        #print vname
	#a = raw_input()
for li in fvlist:
    temp = li.split()
    datedir = target_folder + "/" + temp[0]
    print temp, datedir
    if os.path.isdir(datedir) == False:
        print "NO"
        continue
    else :
        if os.path.isfile(datedir + "/" + temp[1]) == False:
	    continue 
        doc_name[temp[1]] = doc_count
        fp = open(datedir + "/" + temp[1])
        doc[doc_count] = []
	for li in fp:
	    mystring = li.decode('utf8', 'ignore')
	    lowers = mystring.lower()
            wtokenizer = RegexpTokenizer(r'\w+')
	    token_list = wtokenizer.tokenize(lowers)
	    token_with_tags = nltk.pos_tag(token_list)
	    filtered_tokens = [token for token in token_with_tags if token[0] not in stopwords.words('english')]

      	    #filter url, and lammatize	
	    for w in filtered_tokens:
		if re.match(r"www|html|http|com",w[0]) is not None:
			continue
		tag = ''
		if w[1].startswith('J'):
			tag = wordnet.ADJ
    		elif w[1].startswith('V'):
			tag = wordnet.VERB
    		elif w[1].startswith('N'):
			tag = wordnet.NOUN
    		elif w[1].startswith('R'):
			tag = wordnet.ADV
		if tag is not '':
                	doc[doc_count].append(lmtzr.lemmatize(w[0],tag))
		#print doc
	    #setlist = set(lmlist)
        doc[doc_count] = set(doc[doc_count])
	doc_count += 1
        fp.close()
    #a = raw_input()
fvlist.close()
#read in translated tags
print translated_folder
for folder in os.listdir(translated_folder):
    print folder
    for fi in os.listdir(translated_folder + '/' + folder):
        cf = open(translated_folder + '/' + folder + '/' +fi)
	print fi[0:10]
	doc_name[fi[0:10]] = doc_count
	doc[doc_count] = []
	for li in cf:
	    mystring = li.decode('utf8', 'ignore')
	    lowers = mystring.lower()
            wtokenizer = RegexpTokenizer(r'\w+')
	    token_list = wtokenizer.tokenize(lowers)
	    token_with_tags = nltk.pos_tag(token_list)
	    filtered_tokens = [token for token in token_with_tags if token[0] not in stopwords.words('english')]

      	    #filter url, and lammatize	
	    for w in filtered_tokens:
		if re.match(r"www|html|http|com",w[0]) is not None:
			continue
		tag = ''
		if w[1].startswith('J'):
			tag = wordnet.ADJ
    		elif w[1].startswith('V'):
			tag = wordnet.VERB
    		elif w[1].startswith('N'):
			tag = wordnet.NOUN
    		elif w[1].startswith('R'):
			tag = wordnet.ADV
		if tag is not '':
                	doc[doc_count].append(lmtzr.lemmatize(w[0],tag))
		#print doc
	    #setlist = set(lmlist)
        doc[doc_count] = set(doc[doc_count])
	doc_count += 1
	cf.close()	


#create keyword table
temp_keyword_table = {}
for d in doc:
    wordset = doc[d]
    for s in wordset:
	if len(s) < 3:
		continue
        if s not in temp_keyword_table:
            temp_keyword_table[s] = 1
        else:
            temp_keyword_table[s] += 1

for word in temp_keyword_table:
    #if temp_keyword_table[word] > 2 and temp_keyword_table[word] < 130:
    keyword_table[word] = keyword_count
    keyword_count += 1

            
print keyword_count
print doc_count
a = raw_input()
#read in cluster file
fcluster = open('../../ClusterAll.txt')
iscontent = False
cluster_dict = {}
cluster_name = {}
cluster_count = 0
doc_meme = {}
templist = []
date_video_info = {}
for line in fcluster:
    if re.search("Cluster", line) is not None:
        cluster_name[cluster_count] = line
        iscontent = True
    elif re.search(".jpg", line) is not None:
	t_list = re.search("2457(.+?)/(.+?).mp4", line)
	temp = t_list.group(2)
	date_str= "2457" + t_list.group(1)
	if date_str not in date_video_info:
		date_video_info[date_str] = []
	date_video_info[date_str].append(temp)
        #print temp
        #a = raw_input()
	templist.append(temp)
    else:
      	#if len(set(templist)) > 10 or len(set(templist)) < 2:
        #    del cluster_name[cluster_count]
	#    del templist[:]
        #    templist = []
        #    iscontent = False
        #    continue
        cluster_dict[cluster_count] = set(templist)
        cluster_count += 1
	del templist[:]
        templist = []
        iscontent = False

#output index file
#video id
 
fvid = open("video_index", 'w')
for name in doc_name:
    fvid.write(name + " ")
    fvid.write(str(doc_name[name])+"\n")
fvid.close()

#scipy.io.savemat("index_visual_meme", mdict={"index_visual_meme": cluster_name}) 
fmeme = open("visual_meme_index", "w")
for cluster_id in cluster_name:
    cname =  cluster_name[cluster_id]
    fmeme.write( cname[0:len(cname)-1]+ " ")
    fmeme.write(str(cluster_id) + "\n")
fmeme.close()

index_keyword = {}
for k in keyword_table:
    index_keyword[str(keyword_table[k])] = k
#scipy.io.savemat("index_keyword", {"index_keyword": index_keyword}) 

ftag = codecs.open("tag_index", "w", "utf-8")
for k in keyword_table:
    ftag.write(k + " ")
    ftag.write(str(keyword_table[k]) + "\n")
ftag.close()

for c_id in cluster_dict:
    vname_list = cluster_dict[c_id]
    for v in vname_list:
        if v not in doc_meme:
	    doc_meme[v] = []
        doc_meme[v].append(c_id)
print doc_meme
a = raw_input()

#create mat along time()
#for v_name in sorted(date_video_info):
#	print v_name, set(date_video_info[v_name])

date_list = sorted(date_video_info)
print date_list
# for each date, create a mat : visual_text
for i in range(0, len(date_list)):
    v_t_i_mat =  np.zeros((cluster_count, keyword_count))
    #get document name of date i
    d_name_list = date_list[i]
    print d_name_list
    for d in set(date_video_info[d_name_list]):
        #for each doc get list of visual memes index 
        if d not in doc_meme or d not in doc_name:
            continue
	v_meme_list = doc_meme[d]
	tag_list = doc[doc_name[d]]  # doc name to doc index to tag list
	for t in tag_list:
	    if t not in keyword_table:
	        continue
	    t_index = keyword_table[t]
            for v in v_meme_list:
            	v_t_i_mat[v][t_index] += 1  

    mat_name = "timeline_matrix/v_t_" + str(i) + ".mat"
    var_name = "v_t"  
    scipy.io.savemat(mat_name, mdict={var_name: v_t_i_mat})     
    #print "save"
    #a = raw_input()

#a = raw_input()
# create  (tags + visual memes)X C (video counts)
vt_c_mat = np.zeros((cluster_count+keyword_count,doc_count))
#fill in tag part
for d in doc_name:
    d_index = doc_name[d]
    d_keyword = doc[d_index]
    for k in d_keyword:
        if k not in keyword_table:
            continue
        k_index = keyword_table[k]
        row_index = cluster_count+k_index
        vt_c_mat[row_index][d_index] += 1
#fill in visual meme part
for cluster_id in cluster_dict:
    vname_list = cluster_dict[cluster_id]
    for v in vname_list:
        if v not in doc_name:
            continue
        v_index = doc_name[v]
        vt_c_mat[cluster_id][v_index] += 1
scipy.io.savemat('vt_c_mat.mat', mdict={'vt_c_mat': vt_c_mat})

# for each clusters, create relation matrix  visual_text
relation_mat = np.zeros((cluster_count, keyword_count))
for i in range(0, len(cluster_dict)):
    vname_list = cluster_dict[i]
    for v in vname_list:
        if v not in doc_name:
	    #print v
            continue
        v_index = doc_name[v] #look at the index by video name
        word_set = doc[v_index]
	for w in word_set:
            if w not in keyword_table:
                continue
	    relation_mat[i][keyword_table[w]] += 1

scipy.io.savemat('bi_relation_mat.mat', mdict={'bi_relation_mat': relation_mat})
	
    
