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
target_folder = '../../../US_desc/'
translated_folder = '../../../Chinese_desc_translated/'
category_lable = {}
# read in documents
fvlist = open('../../selected_video_set/sample_data_set_flat.txt')
for li in fvlist:
    print li
    temp = re.search('videos/(.+?).mp4', li).group(1)
    if re.search('US', li) is not None:
        filepath = target_folder + temp
	filename = temp[8:19]
    else:
	filepath = translated_folder + temp + ".txt"
	filename = temp[8:18]
    print filepath, filename
    if os.path.isfile(filepath) == False:
	print "Missing"
	#a = raw_input()
        continue
    else : 
        doc_name[filename] = doc_count
        fp = open(filepath)
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

            
print  "keyword count:" + str(keyword_count)
print "document count:" + str(doc_count)
a = raw_input()
#read in cluster file
fcluster = open('../../selected_video_set/SampleCluster.txt')
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
	templist.append(temp)
    else:
        if len(set(templist)) < 2:
            del cluster_name[cluster_count]
	    del templist[:]
            templist = []
            iscontent = False
            continue
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
os.system("rm -r timeline_matrix")
os.system("mkdir timeline_matrix")
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
#create cultural matrix
os.system("rm -r culture_mat")
os.system("mkdir culture_mat")
c_1_mat = np.zeros((cluster_count, keyword_count))
c_2_mat = np.zeros((cluster_count, keyword_count))
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
	    if len(v) == 11:
	        c_1_mat[i][keyword_table[w]] += 1
	    else:
	        c_2_mat[i][keyword_table[w]] += 1
scipy.io.savemat("culture_mat/c_1_mat.mat", mdict={'c_1': c_1_mat}) 
scipy.io.savemat("culture_mat/c_2_mat.mat", mdict={'c_2': c_2_mat}) 


	
#create ground truth matrix
gt_clusters = {}
glist = open('../../selected_video_set/sample_data_set.txt')
for li in glist:
    if re.search('Cluster', li) is not None:
        ClusterID = li
	Clist = []
    elif re.search('245',li) is not None:
	temp = re.search("2457(.+?)/(.+?).mp4", li)
	Clist.append(temp.group(2))
    else:
	gt_clusters[ClusterID] = set(Clist)
	del Clist[:]
glist.close()    
print gt_clusters
os.system("rm -r ground_truth_2D_mat")
os.system("mkdir ground_truth_2D_mat")
gdata = open('cluster_name.txt', 'w')
for key,value in gt_clusters.items():
    v_mat = np.zeros(cluster_count)
    t_mat = np.zeros(keyword_count)
    for i in range(0, len(cluster_dict)):
        vname_list = cluster_dict[i]
	if len(set(vname_list).intersection(value)) < 0.8*len(vname_list):
	    continue
	#print value, vname_list
	v_mat[i] = 1

    for v in value:
        if v not in doc_name:
	    print v
            continue
        video_index = doc_name[v] #look at the index by video name	
        word_set = doc[video_index]
	for w in word_set:
            if w not in keyword_table:
                continue
	    t_mat[keyword_table[w]] += 1
    tmat_name = "ground_truth_2D_mat/" + key[0:len(key)-3] + "_tag.mat"
    gdata.write(tmat_name+'\n')
    vart_name = "c_tag"  
    scipy.io.savemat(tmat_name, mdict={vart_name: t_mat}) 
    mmat_name = "ground_truth_2D_mat/" + key[0:len(key)-3] + "_meme.mat"
    gdata.write(mmat_name+'\n')
    varm_name = "c_meme"  
    scipy.io.savemat(mmat_name, mdict={varm_name: v_mat})      
gdata.close()

