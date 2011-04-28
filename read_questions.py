#!/usr/bin/env python

#this will read in the questions without the answers and return a list where
#each item in the list is a question.  Each question is a list of two things.
#The first item in this list is the question number and the second is the 
#actual text which is a continuous string
def read_questions_no_answers():
  f = open('corpus/questions.txt', 'r')
  top_flag = 0
  question_list = []
  question = []
  for line in f:
    line = line.rstrip('/n').rstrip()
    if len(line)>0:
      word_list = line.split()
      if word_list[0] == '<top>':
        top_flag = 1
      elif word_list[0] == "</top>":
        question = []
        top_flag = 0
      elif word_list[0] == "<num>":
        question.append(word_list[2])
      elif word_list[0] == "<desc>":
        top_flag = 1
      else:
        question.append(line)
        question_list.append(question)

  return question_list

#This will read in the questions with the answers and output a list of
#questions. Each question will be a list which has the id as the first
#entry, the question as the second entry, something that I didn't know
#what was happening but seemed relevant as the third entry, and the
#answer as the fourth entry.  Look in the file answers.txt and the
#format of my list will become clear

def read_questions_answers():
  f = open('corpus/answers.txt', 'r')
  count = 0
  question_list = []
  question = []
  
  for line in f:
    line = line.rstrip('/n').rstrip()
    if len(line)>0:
      word_list = line.split()
      if word_list[0] == 'Question':
        question_list.append(question)   # I think if you want, changing
        question = []                    # it to question = [word_list[1]]
        question.append(word_list[1])    # and then doing
                                         # question_list.append would
                                         # solve the problem below
      else:
        question.append(line)
  
  question_list.append(question)

  # now pop the first element of this list, which is [], since we did
  # question = [] above and question is always appended as the first
  # thing. If this function is rewritten like read_questions_no_answers(),
  # this line below may be unnecessary
  question_list.pop(0)
  return question_list
