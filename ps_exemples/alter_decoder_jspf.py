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
nb = 100
digi = 5
gram = 'number'
while tr <= nb :

	#decoder = Decoder(config)	
	decoder.start_utt()
	a = (tr/100)
	b = (tr/10)%10
	c = tr %10
	chaine = 'td_corpus_digits/td_corpus_digits/SNR'+str(i)+'dB/man/seq'+str(digi)+'digits_'+str(nb)+'_files/SNR'+str(i)+'dB_man_seq'+str(digi)+'digits_'+str(a)+str(b)+str(c)+'.'	
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
	rule = jsgf.get_rule('1chiffre.'+gram)
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
#nom = 'data'+str(nb)+'1mot'+str(i)+'db.txt'
nom = 'data.hyp'
nom2 = 'data.ref'
fichier = open(nom,'w')
fichier2 = open(nom2,'w')
for i in range(0,nb):
	#print(lref[i])
	#print(lres[i])
	#print("--------------")
	fichier.write(chaine+'raw '+lres[i]+'\n')
	fichier2.write(chaine+'ref '+lref[i])


fichier2.close()
fichier.close()
