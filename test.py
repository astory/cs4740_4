#!/usr/bin/env python

# Loops through all of the top*.* files 
# and reads the <docnum> and <text> content into a dictionary

from BeautifulSoup import BeautifulStoneSoup 
import os 
import glob
  
path = '.\corpus'
#path = ''
dict = {}

for infile in glob.glob( os.path.join(path, 'top*.*') ):
    print "current file is: " + infile

    f = open(infile)
    soup = BeautifulStoneSoup(f)

    # each <docnum>,<text> pair is inside a parent <doc>
    for d in soup('doc'):
        docNum = d.findNext('docno').renderContents().strip()
        # because file 372 has a <doc> and <docnum> without any <text> (the last one)
        dT = d.findNext('text')
        if dT != None:
            docText = dT.renderContents().strip()
            dict[docNum] = docText


for key in dict:
    print key




