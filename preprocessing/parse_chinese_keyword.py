import os,sys,re,jieba
import jieba.analyse

def extract_phrases(targetfolder, storefolder):

    for folder in os.listdir(targetfolder):
        folder_path = targetfolder+folder
	os.system("mkdir " + storefolder+folder)
        for fi in os.listdir(folder_path):
            file_name = folder_path + '/' + fi
	    out_fold_name = storefolder+folder + '/' + fi;
	    out_fp = open(out_fold_name, 'w')
	    print out_fold_name
            fp = open(file_name)
            content = fp.read()
	    tvName = re.search("\"tvName\":\"(.+?)\"", content).group(1).split()
	    keywords = re.search("\"keyword\":\"(.+?)\"", content).group(1)
	    print tvName, keywords
	    for pp in tvName:
	        out_fp.write(pp + '\n')
	    out_fp.write(keywords + '\n')
	    fp.close()
            #seg_list = jieba.analyse.extract_tags(tvName + keywords)
            
	    #for i in range(0,len(seg_list)):
            #    print seg_list[i]
            #a = raw_input()
  
        


def main():
    extract_phrases('Chinese_desc_remaining/','Chinese_desc_parsed_remaining/')


if __name__ == "__main__":
    main()
