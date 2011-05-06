#!/usr/bin/env python

#as of now this is going to assume that both the question and the answer is a list of words and that the dictionary is irrelevant for what this task should do this will return 1 if a new word has been found and 0 if a new word has not been found
import nltk
from nltk import word_tokenize

stopwords = nltk.corpus.stopwords.words('english')
def remove_stop_words (question_tokens):     
  return [w for w in question_tokens if w.lower() not in stopwords]

def novelty_bool (q_list, (a_list, doc_num, context,d,q_id)):
  question_list = remove_stop_words (word_tokenize(q_list))
  answer_list = remove_stop_words(word_tokenize(a_list))
  b = 0  
  for a in answer_list:
    temp = 1
    for q in question_list:
       if a.lower() == q.lower():
         temp = 0
         break
    if temp == 1:
      b = 1
  (b)

#this will return the number of words that are novel divided by the number of words in the answer to give a percent value
def novelty_count (q_list, (a_list, doc_num, context,d,q_id)):
  count = 0.0
  question_list = remove_stop_words (word_tokenize(q_list))
  answer_list = remove_stop_words(word_tokenize(a_list))
  for a in answer_list:
    temp = 1
    for q in question_list:
       if a.lower() == q.lower():
         temp = 0
         break
    if temp == 1:
      count = count + 1.0
  count = count / (len(answer_list))
  (count)
