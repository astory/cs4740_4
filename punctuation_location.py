#!/usr/bin/env python
import nltk
import init

#returns 1 if the character following the answer in the document is one of <, . " : !>
#and returns 0 otherwise
def punc_loc(question, (answer, doc_num, index, features)):
    doc = init.get_doc(doc_num)
    #go to index location of candidate within the document
    answer_len = len(answer)
    #check if character at doc[index + len(candidate)] is a punctuation
    if doc[index+answer_len] == ',' or doc[index+answer_len] == '.' or doc[index+answer_len] == '"'  or doc[index+answer_len] == ':' or doc[index+answer_len] == '!':
        return 1
    else: 
        return 0
    

init.get_corpus(qNum=201)
question = 'What was the name of the first Russian astronaut to do a spacewalk?'
doc_num = "LA072490-0034"
print punc_loc (question, ("Aleksei A. Leonov", doc_num, 50, {}))