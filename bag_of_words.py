#!/usr/bin/env python

#this returns the dot product of the question vector and answer vector as  I understand the vector space model does.  Basically just takes each word in the question as a dimension and the number of times that the word appears as the value.  Then it does the same thing with the answers and takes the dot product
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from math import sqrt
def vector_bag (q_list, (a_list, doc_num, context,d)):
  question_list = word_tokenize(q_list)
  answer_list = word_tokenize(a_list)
  v1 = []
  v2 = []
  for q in question_list:
     b = 0.0
     for (c,s) in v1:
       if s.lower() == q.lower():
         b = b +1.0
         break
     if (b>0):
       v1[v1.index((c,q))] = ((c+b,q))
     else:
       v1.append((1.0,q))
  for v in v1:
    v2.append(0.0)
  for a in answer_list:
    for (c,q) in v1:
      if(a.lower()==q.lower()):
        v2[v1.index((c,q))] = v2[v1.index((c,q))] +1.0
  print v1
  print v2
  numer = 0.0
  denom1 = 0.0
  denom2 = 0.0
  count = 0
  for (c,q) in v1:
    numer = numer + c * v2[count]
    denom1 = denom1 + c * c
    denom2 = denom2 + v2[count] * v2[count]
    count = count + 1
  dot = numer/sqrt(denom1)/sqrt(denom2)
  print dot
  (q_list, doc_num, a_list, dot)   

#this will return the number of words that are in the question divided by the number of words in the answer to give a percent value.  Thsi is normalized.  It migth be best to not normalize it
def bag_of_words (q_list, (a_list, doc_num, context,d)):
  question_list = word_tokenize(q_list)
  answer_list = word_tokenize(a_list)
  count = 0.0
  for a in answer_list:
    temp = 1
    for q in question_list:
       if a.lower() == q.lower():
         count = count + 1.0
         break
  count = count / (len(answer_list))
  print count
  (q_list, doc_num, a_list, count)
