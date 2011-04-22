#!/bin/bash
import urllib2
import MultipartPostHandler
import datetime

def submit(netid,answers):
	answersFile='tmp-answers.txt'
	answersHandle=open(answersFile,'w')
	answersHandle.write(answers)
	answersHandle.close()
	params= { 'netid':netid,
                  'predictions': open(answersFile,'rb')
		}
	opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
	urllib2.install_opener(opener)
	req = urllib2.Request('http://www.cs.cornell.edu/w8/~luwang/cs4740_QA/getFile',params)
	response = urllib2.urlopen(req).read().strip()
	return response+'\n(Submitted at '+datetime.datetime.now().ctime()+')'

def main():
	print submit('tkl22','201 top_docs.201 Hawaii')

if __name__ == "__main__":
    main()
