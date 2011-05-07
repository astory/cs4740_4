#!/usr/bin/env python
import nltk
import read_questions

def firstGram(sentence,n):
  return ' '.join(nltk.tokenize.word_tokenize(sentence)[:n])

def get_question_types(n=1): #Unigrams by default
  questions=read_questions.read_questions_no_answers()
  types=[]
  for question in questions:
    a=firstGram(question[1],n)
    if a not in types:
      types.append(a)	
  return types

def classify_questions(n=1):
	questions={}
	for t in get_question_types(n):
		questions[t]=[]
	for question in read_questions.read_questions_no_answers():
		questions[firstGram(question[1],n)].append(question[0])
	return questions

def question_type(questions,n=2): #Unigrams by default
  for question in questions:
    question.append(firstGram(question[1],n))
  return questions

def main():
  import read_questions
  return answer_type(read_questions.read_questions_answers())

if __name__ == "__main__":
  print get_question_types()
  print classify_questions()
