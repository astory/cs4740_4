#!/usr/bin/env python
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import brown
brown_tagged = brown.tagged_sents()
unigram_tagger = nltk.UnigramTagger(brown_tagged)
def pos_tagger(context,position,dictionary):
  list_tags = pos_tag(word_tokenize(context[position]))
  x,y = list_tags[0]
  dictionary["pos"] = y
  return dictionary

def unigram_tagger(context,position):
  list_tags = unigram_tagger.tag(word_tokenize(context[position]))
  x,y = list_tags[0]
  dictionary["unigram pos"] = y
  return dictionary

def bigram_tagger(context, position):
  if position == 0:
    input = context[position]
  else:
    input = context[position] + " " + context[position-1]
  list_tags = bigram_tagger.tag(word_tokenize(input))
  x,y = list_tags[1]
  dictionary["bigram pos"] = y
  return dictionary

def tag_answers():
  import read_questions
  answers=[]
  for i in read_questions.read_questions_answers():
      answers.append(i[3])

