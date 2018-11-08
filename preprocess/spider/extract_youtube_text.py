import os,sys,re
import nltk


folder = "video_metadata"
textfolder = "YouTube_text"
for m_folder in os.listdir(folder):
    print m_folder
    os.system("mkdir " + textfolder + "/" + m_folder)
    for m_file in os.listdir(folder + "/" + m_folder):
	print m_file
        fp = open(folder + "/" + m_folder + "/" + m_file)
        ftext = open(textfolder + "/" + m_folder + "/" + m_file + ".txt", 'w')

	m_content = fp.read()
        title = re.search("<title type='text'>(.+?)</title>", m_content)
	content =re.search("<content type='text'>(.+?)</content>", m_content)
	desc = re.search("<media:description type='plain'>(.+?)<", m_content)
	#keywords = re.search("<media:keywords/>(.+?)<m", m_content)
	media_title = re.search("<media:title type='plain'>(.+?)<", m_content)
	if(title is not None):
	    ftext.write(title.group(1)+" ")
	
	if(content is not None):
	    ftext.write(content.group(1)+" ")

	if(desc is not None):
	    ftext.write(desc.group(1)+" ")

	#if(keywords is not None):
	#    ftext.write(keywords.group(1)+" ")

	if(media_title is not None):
	    ftext.write(media_title.group(1)+" ")
	
	fp.close()
	ftext.close()

