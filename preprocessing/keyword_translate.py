from microsofttranslator import Translator
import os,sys,re
import unicodedata

def translate_phrases(targetfolder, storefolder):
    translator = Translator('eshiland', 'MysFlkproThuDKqtbUm93ML6BdYRT/F+4ap44540ntM=')
    for folder in os.listdir(targetfolder):
        folder_path = targetfolder+folder
	os.system("mkdir " + storefolder+folder)
        for fi in os.listdir(folder_path):
            file_name = folder_path + '/' + fi
	    out_fold_name = storefolder+folder + '/' + fi;
	    out_fp = open(out_fold_name, 'w')
	    print out_fold_name
            fp = open(file_name, 'r')
	    
	    for li in fp:
	        translate_temp = translator.translate(li.decode('utf-8'), "en")
	        print translate_temp
	        out_fp.write(translate_temp + '\n')

 	    #a = raw_input()


	    fp.close()
	    out_fp.close()

#print translator.translate("Hello", "pt")





def main():
    translate_phrases('Chinese_desc_parsed_remaining/','Chinese_desc_translated/')


if __name__ == "__main__":
    main()
