#!/usr/bin/env python
from combine import *
import chunker
import mlpy
import check_answers

def question_candidates(q_id):
#Incomplete
	'''Select some useful subset of the candidates for a particular question.
	Return them in a list.
	'''
	return [ ('sling', 'AP881126-0094', 55, 'VP'), ('farther', 'AP881126-0094', 56, 'NP'), ('away', 'AP881126-0094', 57, 'S')]

def question_learning_data(first=204,last=204):
	x=[]
	y=[]
	for q_id in range(first,last+1):
		cand=question_candidates(q_id)
		x=x+run_evaluators(cand)
		y=y+map(lambda a:check_answers.check_answer(q_id,a),cand)
	return y,x

def question_prediction_data(q_id=202,candidate=('400 micrograms', 'AP881126-0094', 57, 'S')):
	x=run_evaluators([candidate])
	return x[0],q_id,candidate

def main():
	y_train,x_train = question_learning_data()
	x_test,q_id,candidate= question_prediction_data()
	return train(mlpy.Svm,y_train,x_train)
	
if __name__ == '__main__':
	main()
