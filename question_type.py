#!/usr/bin/env python
import nltk

def firstGram(sentence,n):
  return ' '.join(nltk.tokenize.word_tokenize(sentence)[:n])

def answer_type(questions,n=2): #Unigrams by default
  for question in questions:
    question.append(firstGram(question[1],n))
  return questions

def main():
  import read_questions
  return answer_type(read_questions.read_questions_answers())

if __name__ == "__main__":
  print main()
