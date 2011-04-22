#!/bin/bash
import urllib2
import MultipartPostHandler

def submit(netid,answers):
	params= { 'netid':netid,
                  'predictions': open('README.md','rb')
		}
	#params = {'user':'foo','file':open('foo.jpg', 'rb')}
	opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
	urllib2.install_opener(opener)
	req = urllib2.Request('http://www.cs.cornell.edu/w8/~luwang/cs4740_QA/getFile',params)
	response = urllib2.urlopen(req).read().strip()
	return response 

def main():
	print submit('tkl22','README.md')

if __name__ == "__main__":
    main()
