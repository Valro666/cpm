#!/usr/bin/python

from os import environ, path
from sys import stdout

from pocketsphinx import *
from sphinxbase import *

# Create a decoder with certain model
#err_set_logfp(NULL);
#err_set_debug_level(0);

#pocketsphinx_continuous -samprate 48000 -nfft 2048 -hmm \/usr/local/share/pocketsphinx/model/en-us/en-us -lm 9745.lm -dict 9745.dic \-inmin yes 2>&1|tee ./full-output.log|egrep -v --line-buffered '^INFO:'	

config = Decoder.default_config()
config.set_string('-hmm',  'ps_data/model/en-us')
config.set_string('-lm',   'ps_data/lm/turtle.lm.bin')
config.set_string('-dict', 'ps_data/lex/turtle.dic')
config.set_string('-lognf','dev/null')
decoder = Decoder(config)

# Decode with lm
#decoder.start_utt()
#stream = open('ps_data/exemple/goforward.raw', 'rb')
i = 25 #05 15 25 35 

a = 0
b = 0
c = 0

tr = 1

lres = list()
lref = list()


while tr <= 200 :

	#decoder = Decoder(config)	
	decoder.start_utt()
	a = (tr/100)
	b = (tr/10)%10
	c = tr %10
	chaine = 'td_corpus_digits/td_corpus_digits/SNR'+str(i)+'dB/man/seq1digit_200_files/SNR'+str(i)+'dB_man_seq1digit_'+str(a)+str(b)+str(c)+'.'	
	print(chaine);
	tr = tr+1

#fichier = "001"
	stream = open(chaine+'raw','rb');
	ref = open(chaine+'ref','rb');

	while True:
    		buf = stream.read(1024)
    		if buf:
         		decoder.process_raw(buf, False, False)
    		else:
         		break
	decoder.end_utt()	


	hyp = decoder.hyp()
	if hyp.hypstr != None :

		print ('Decoding with "turtle" language:', hyp.hypstr)

		print ('')
		print ('--------------')
		print ('')
	else :
		break

# Switch to JSGF grammar
	jsgf = Jsgf('ps_data/jsgf/1chiffre.gram')
	rule = jsgf.get_rule('1chiffre.number')
	fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
	fsg.writefile('chiffre.fsg')

	decoder.set_fsg("chiffre", fsg)
	decoder.set_search("chiffre")

	decoder.start_utt()
#stream = open('ps_data/exemple/goforward.raw', 'rb')
	stream = open(chaine+'raw','rb');


	while True:
	    buf = stream.read(1024)
	    if buf:
	         decoder.process_raw(buf, False, False)
	    else:
	         break
	decoder.end_utt()

	if hyp.hypstr != None :
		tmp = ref.read()
		print ('Decoding with "chiffre" grammar:', hyp.hypstr)
		print (tmp)
		lref.append(tmp)
		lres.append(hyp.hypstr)

for i in range(0,200):
	print(lref[i])
	print(lres[i])
	print("--------------")
