#!/usr/bin/env python
#import sys
#sys.path.append('./modules')
#import monte

import numpy as np
import mlpy
import random #Just for generating fake data

def dummy_evaluator(x):
	return random.random()

def check_answer(candidate):
	return int(1-2*round(random.random()))

def run_evaluators(candidates):
	#candidate = list of the question-candidate indexes
	evaluators = [dummy_evaluator,dummy_evaluator,dummy_evaluator] #List of evaluator functions
	confidence = []
	for candidate in candidates:
		candidateConfidence=[]
		for evaluator in evaluators:
			candidateConfidence.append(evaluator(candidate))
		confidence.append(candidateConfidence)
	return confidence

def train(model,correctness,features):
	'''
	Train a model for classifying answers as correct or not
	based on the confidence measures from various QA methods.
	This should support paramaters at some point.
	'''
	#Format them for the classification model https://mlpy.fbk.eu/data/doc/classification.html
	xtr = np.array(features)
	ytr = np.array(correctness)
	if model==mlpy.Knn:
		fit=model(k=1)
	else:
		fit=model()  # initialize Svm class
	fit.compute(xtr, ytr)  # compute SVM
	#print svm.weights(xtr,ytr) #Weights/coefficients
	return fit

def test(fit):
	'''
	Guess which test corpus answers are correct based on
	 * The model from the training corpus
	 * The confidence measures from the test corpus
	This also needs to take real paramaters at some point.
	'''
	#Confidence measures for one particular answer
	#from all [let's say 3] QA methods
	confidence=[0.9995270445322,0.378183359280229,0.275786651414819]

	xts = np.array(confidence) # test point
	# predict SVM on test corpus answer
	fit.predict(xts)
	out=[]
	if fit.predict(xts)==-1:
		out.append(False)
	elif fit.predict(xts)==1:
		out.append(True)
	try:
		out.append(fit.realpred)
		# "real-valued prediction"
		# I think it's something like confidence
	except:
		pass
	return out


def demo():
#	y,x=run_evaluators0()
	candidates=range(0,7)
	x=run_evaluators(candidates)
	y=map(check_answer,candidates)
	#The predictions fail if all of the correctness values are the same	
	print ''
	print 'Predictions as to whether an answer is correct'
	print 'for random data from various models'
	print '----------------------------------------------'
        print 'Model Result Confidence? ("Real value")'
	print '----- ------ ---------------------------------'
	print ' SVM  '+str(test(train(mlpy.Svm,y,x)))
	print ' KNN  '+str(test(train(mlpy.Knn,y,x)))
	print ' FDA  '+str(test(train(mlpy.Fda,y,x)))
	print 'SRDA  '+str(test(train(mlpy.Srda,y,x)))
	print ' PDA  '+str(test(train(mlpy.Pda,y,x)))
#	print 'DLDA  '+str(test(train(mlpy.Dlda,y,x)))
	print '----------------------------------------------'

if __name__ == "__main__":
    demo()

