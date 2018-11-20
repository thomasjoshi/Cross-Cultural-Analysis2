from microsofttranslator import Translator
import os,sys,re
import unicodedata
from subprocess import call
import subprocess

f_vlist = open('video_list', 'w')
for folder in os.listdir('US_desc/'):
	print folder 
	for fi in os.listdir('US_desc/' + folder):
		print fi
		temp = 'US_desc ' + folder + ' '+ fi
		f_vlist.write(temp + '\n')

for folder in os.listdir('Chinese_desc_translated/'):
	print folder 
	for fi in os.listdir('Chinese_desc_translated/' + folder):
		print fi
		filename = fi[0:11]
		temp = 'Chinese_desc_translated ' + folder + ' '+ fi
		f_vlist.write(temp + '\n')

f_vlist.close()

