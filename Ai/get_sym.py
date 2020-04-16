from nltk.corpus import wordnet
import nltk
from dico import *
def txt_process(reply):
	roots=[]
	punctuators=['.',',','!',':',"/","?"]
	stop_words=nltk.corpus.stopwords.words('english')+punctuators
	sentences=nltk.sent_tokenize(reply)
	for sentence in sentences:
		words=nltk.word_tokenize(sentence)
		for word in words:
			if word not in stop_words:
				roots.append(word)
	return(roots)
def root_words(reply):
	sentences = reply
	nouns=[]
	for sentence in sentences:
	     for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
	         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
	             nouns.append(word)
	return(nouns)

def get_symps(reply):
	final=[]
	#print(fixd)
	for word in reply:
		if(word in fixd):
			final.append(word)
		else:
			syns = wordnet.synsets(word)
			count=0
			if(len(syns)<=2):
				continue
			while(count<2):
				if(syns[count].lemmas()[0].name() in fixd):
					final.append(word)
					break
				count=count+1
	return(final)
def merge2s(reply):
	last=[]
	for i in range(0,len(reply)-1):
		wk=reply[i]+"_"+reply[i+1]
		if(wk in twos):
			last.append(wk)
		else:
			last.append(reply[i])
	last.append(reply[len(reply)-1])
	return(last)
def merge3s(reply):
	last=[]
	for i in range(0,len(reply)-2):
		wk=reply[i]+"_"+reply[i+1]+"_"+reply[i+2]
		#print(wk)
		if(wk in threes):
			last.append(wk)
		else:
			last.append(reply[i])
	last.append(reply[len(reply)-1])
	last.append(reply[len(reply)-2])
	return(last)
def clean(reply):
	final=[]
	for word in reply:
		if word in symtoms_all:
			final.append(word)
	return(final)
