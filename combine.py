#!/usr/bin/env python
#import sys
#sys.path.append('./modules')
#import monte
import chunker
import numpy as np
import mlpy
import random #Just for generating fake data
import tom

def dummy_evaluator(candidate):
	#Do magic
	#print 'Doing magic'
	#Return a number
	return [random.random()]

def dummy_evaluator2(candidate):
	return tom.interactions(random.random(),random.random())

def check_answer(candidate):
	#Check whether the answer is correct
	#print 'Checking whether the answer is correct'
	#Return 1 for correct and -1 for incorrect
	return int(1-2*round(random.random()))

def run_evaluators(candidates):
	#candidate = list of the question-candidate indexes
	evaluators = [dummy_evaluator,dummy_evaluator2] #List of evaluator functions
	confidence = []
	for candidate in candidates:
		candidateConfidence=[]
		for evaluator in evaluators:
			candidateConfidence=candidateConfidence+evaluator(candidate)
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

def test(fit,features):
	'''
	Guess which test corpus answers are correct based on
	 * The model from the training corpus
	 * The confidence measures from the test corpus
	This also needs to take real paramaters at some point.
	'''
	xts = np.array(features) # test point
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
	candidates=range(1,50)
#	candidates=chunker.run(333)[0:55]
	candidates_train=candidates[0:40]
	candidates_test =candidates[45:55]
	x_train=run_evaluators(candidates_train)
	y_train=map(check_answer,candidates_train)
	x_test =run_evaluators(candidates_test)
	#Run the predictions for just one of these test question candidates
	x_test=x_test[0]
	#The predictions fail if all of the correctness values are the same	
	print ''
	print 'Predictions as to whether an answer is correct'
	print 'for random data from various models'
	print '----------------------------------------------'
        print 'Model Result Confidence? ("Real value")'
	print '----- ------ ---------------------------------'
	print ' SVM  '+str(test(train(mlpy.Svm,y_train,x_train),x_test))
#	print ' KNN  '+str(test(train(mlpy.Knn,y_train,x_train),x_test))
	print ' FDA  '+str(test(train(mlpy.Fda,y_train,x_train),x_test))
	print 'SRDA  '+str(test(train(mlpy.Srda,y_train,x_train),x_test))
	print ' PDA  '+str(test(train(mlpy.Pda,y_train,x_train),x_test))
#	print 'DLDA  '+str(test(train(mlpy.Dlda,y_train,x_train),x_test))
	print '----------------------------------------------'

if __name__ == "__main__":
    demo()

