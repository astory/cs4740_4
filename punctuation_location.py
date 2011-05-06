#!/usr/bin/env python
import nltk
import init
import chunker

#returns 1 if the character following the answer in the document is one of <, . " : !>
#and returns 0 otherwise
def punc_loc(question, (answer, doc_num, index, features,q_id)):
    doc = chunker.clean_punctuation(init.get_doc(doc_num))
    
    answer = chunker.clean_punctuation(answer)
    #go to index location of candidate within the document
    alist = answer.split()              #split candidate answer into words (space delimiter)
    answer_len = len(alist)             #word length of the candidate answer
    #print answer_len
    
    punc_word_index = index+answer_len   #index of the word that may contain the punctuation
    dlist = doc.split()                    #split the document by words
    punc_word = dlist[punc_word_index]     #getting the actual word from the doc
    
    #check if that lastcharacter is a punctuation
    if punc_word == ',' or punc_word == '.' or punc_word == '"'  or punc_word == ':' or punc_word == '!':
        return [1]
    else: 
        return [0]
    
#test case below was modified to work with specified doc instead of the actual doc to work with a known index
def test():
	question = 'What was the name, of the first Russian astronaut to do a spacewalk?'
	doc = 'The name of the first Russian astronaut to do a spacewalk is Aleksei A. Leonov!'
	doc_num = "LA072490-0034"
	init.global_doc_dict[doc_num] = doc
	print punc_loc(question,('Aleksei A. Leonov',doc_num,12,{}))
	return (question,('Aleksei A. Leonov',doc_num,12,{}))

if __name__ == "__main__":
	a,b= test()
	print ''
	print(punc_loc(a,b))
