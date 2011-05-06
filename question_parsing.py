#!/usr/bin/env python

#this file takes in a question and parses it to
#remove stop words,
#pos tag the remaining words in the question
#and then find named entites of the pos tagged words

import os 
import glob
import nltk
from nltk import pos_tag, word_tokenize

def parseQuestion(question):
    question_tokens = word_tokenize(question)
    # need to download: nltk.download("stopwords")
    # removing stop words from the question
    stopwords = nltk.corpus.stopwords.words('english')     
    ques_no_stopwords = [w for w in question_tokens if w.lower() not in stopwords]
    # pos tagging the tokens in the question
    ques_pos_tagged = pos_tag(ques_no_stopwords)
    # need to download: nltk.download('maxent_ne_chunker')
    #                   nltk.download("words")
    # NE tagging the pos tagged tokens, setting binary to False specifies the type of NE
    ques_ne_tagged = nltk.ne_chunk(ques_pos_tagged, binary=False)
    return ques_ne_tagged

#Testing
ques = 'What was the name of the first Russian astronaut to do a spacewalk?'
new_ques = parseQuestion(ques)
for tkn in new_ques:    
    if hasattr(tkn,'node'):
        print 'Named Entity:' + tkn.node   
        print 'Word:' + tkn[0][0]
        print 'POS Tag:' + tkn[0][1] 
    else:
        print 'Word:' + tkn[0]
        print 'POS Tag:' + tkn[1]
