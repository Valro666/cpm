#!/usr/bin/python

from os import environ, path
from sys import stdout

from pocketsphinx import *
from sphinxbase import *

# Create a decoder with certain model
#err_set_logfp(NULL);
#err_set_debug_level(0);

config = Decoder.default_config()
config.set_string('-hmm',  'ps_data/model/en-us')
config.set_string('-lm',   'ps_data/lm/turtle.lm.bin')
config.set_string('-dict', 'ps_data/lex/turtle.dic')
config.set_string('-lognf','dev/null')
decoder = Decoder(config)

# Decode with lm
#decoder.start_utt()
#stream = open('ps_data/exemple/goforward.raw', 'rb')

a = 0
b = 0
c = 0

# variable a changer pour analyser les fichiers
i = '05' #05 15 25 35   bug avec 05
gram = 'number' #number= infini a5 a3 a1
digi = 1 #5 3 1
#  ----------------

lres = list()
lref = list()
nb = 0 #200 pour 1  100
if digi == 1 :
	nb = 200
else :
	nb = 100
chaine = ''
tr = 1
while tr <= nb :

	#decoder = Decoder(config)	
	decoder.start_utt()
	a = (tr/100)
	b = (tr/10)%10
	c = tr %10
	if digi != 1 :
		chaine = 'td_corpus_digits/td_corpus_digits/SNR'+str(i)+'dB/man/seq'+str(digi)+'digits_'+str(nb)+'_files/SNR'+str(i)+'dB_man_seq'+str(digi)+'digits_'+str(a)+str(b)+str(c)+'.'	
	else :
		chaine = 'td_corpus_digits/td_corpus_digits/SNR'+str(i)+'dB/man/seq'+str(digi)+'digit_'+str(nb)+'_files/SNR'+str(i)+'dB_man_seq'+str(digi)+'digit_'+str(a)+str(b)+str(c)+'.'	

	#print(chaine);
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
	#if hyp.hypstr is not None :
	if hyp.hypstr != None :
	#if type(decoder.hyp()) is not None :
		print ('Decoding with "turtle" language:', hyp.hypstr)
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
	        #print('') 
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

	else :
		break
#nom = 'data'+str(nb)+'1mot'+str(i)+'db.txt'
nom = 'data'+gram+'gram'+str(nb)+'nb'+str(digi)+'digi'+str(i)+'db.hyp'
nom2 = 'data'+gram+'gram'+str(nb)+'nb'+str(digi)+'digi'+str(i)+'db.ref'
#nom2 = 'data.ref'
fichier = open(nom,'w')
fichier2 = open(nom2,'w')
for ii in range(0,nb):
	#print(lref[i])
	#print(lres[i])
	#print("--------------")
	fichier.write(chaine+'raw '+lres[ii]+'\n')
	fichier2.write(chaine+'ref '+lref[ii])


fichier2.close()
fichier.close()
