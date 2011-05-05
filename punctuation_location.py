#!/usr/bin/env python
import nltk
import init

#returns 1 if the character following the answer in the document is one of <, . " : !>
#and returns 0 otherwise
def punc_loc(question, (answer, doc_num, index, features)):
    doc = init.get_doc(doc_num) #retrieves the document labelled as doc_num
    
    #go to index location of candidate within the document
    alist = answer.split()              #split candidate answer into words (space delimiter)
    answer_len = len(alist)             #word length of the candidate answer
    #print answer_len
    
    punc_word_index = index+answer_len-1   #index of the word that may contain the punctuation
    dlist = doc.split()                    #split the document by words
    punc_word = dlist[punc_word_index]     #getting the actual word from the doc
    #print punc_word
    
    punc_word_len = len(punc_word)         #length of the word    
    punc_char = punc_word[punc_word_len-1] #last character of the word (maybe a punctuation?)
    
    #check if that lastcharacter is a punctuation
    if punc_char == ',' or punc_char == '.' or punc_char == '"'  or punc_char == ':' or punc_char == '!':
        return 1
    else: 
        return 0
    
#test case below was modified to work with specified doc instead of the actual doc to work with a known index
init.get_corpus(qNum=201)
question = 'What was the name, of the first Russian astronaut to do a spacewalk?'
doc = 'The name of the first Russian astronaut to do a spacewalk is Aleksei A. Leonov!'
doc_num = "LA072490-0034"
print punc_loc(question,('Aleksei A. Leonov',doc_num,12,{}))
