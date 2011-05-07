#!/usr/bin/env python

# Given a question ### (as a string or int) 
# finds the matching top_docs.### file
# and reads the <docnum> and <text> content into a dictionary

from BeautifulSoup import BeautifulStoneSoup 
import os 
import glob

global_doc_dict = {}

def get_doc(doc_num):
    return global_doc_dict[doc_num]
  
def get_corpus(qNum=0):  
    path = 'corpus'
    dict = {}
    
    # if no question # is passed will loop through the entire corpus
    if qNum == 0:
        fname = 'top_docs.*'
    else:
        fname = 'top_docs.' + str(qNum)
    
    # loop through corpus file(s)
    for infile in glob.glob( os.path.join(path, fname) ):
        f = open(infile)
        soup = BeautifulStoneSoup(f)

        # each <docnum>,<text> pair is inside a parent <doc>
        for d in soup('doc'):
            docNum = d.findNext('docno').renderContents().strip()
            dT = d.findNext('text')
            
            # because file 372 has a <doc> and <docnum> without any <text> (the last one)
            if dT != None:
                docText = dT.renderContents().strip()
                docText = " ".join(docText.split("\n"))
                dict[docNum] = docText

                global_doc_dict[docNum] = docText

    return dict

if __name__ == "__main__":
    get_corpus(qNum=204)
