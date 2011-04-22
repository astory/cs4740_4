#!/bin/bash
import urllib2
import MultipartPostHandler
import datetime
from os import remove

def formatAnswers(numbers,answers):
	def answerLine(number,answer): return str(number)+' top_docs.'+str(number)+' '+answer
	return '<s> <s>\n'+"\n".join(map(answerLine,numbers,answers))

def submit(netid,answers):
	answersFile='tmp-answers.txt'
	answersHandle=open(answersFile,'w')
	answersHandle.write(answers)
	answersHandle.close()
        answersHandle=open(answersFile,'rb')
	params= { 'netid':netid,
                  'predictions': answersHandle
		}
	opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
	urllib2.install_opener(opener)
	req = urllib2.Request('http://www.cs.cornell.edu/w8/~luwang/cs4740_QA/getFile',params)
	response = urllib2.urlopen(req).read().strip()
	answersHandle.close()
	remove(answersFile)
	return response+'\n(Submitted at '+datetime.datetime.now().ctime()+')'

def main():
	print formatAnswers(['398','248'],['the day after Christmas','Document Freedom Day'])

if __name__ == "__main__":
    main()
