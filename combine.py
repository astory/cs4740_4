#!/usr/bin/env python
#import sys
#sys.path.append('./modules')
#import monte

import numpy as np
import mlpy


def run_evaluators():
	#Whether each of these answerse is correct
	#correct=[True,False,False,True,False,False,False,True,False,True,False]
	correctness=[1,-1,-1,1,-1,-1,-1]
	#Confidence measures from each of the three answer extraction methods for seven questions
	confidence1=[0.978183359280229,0.275786651414819,0.48928187857382]
	confidence2=[0.154237459995784,0.196210152702406,0.376024881959893]
	confidence3=[0.230388485593721,0.108338781050406,0.160494192386977]
	confidence4=[0.001228122622706,0.0764752259710804,0.328412672388367]
	confidence5=[0.64096049607421,0.557334918684016,0.315573251030097]
	confidence6=[0.389133446694662,0.245313317359736,0.278548790918042]
	confidence7=[0.0664477733274301,0.588468289934099,0.476068765856326]
	return correctness,[confidence1,confidence2,confidence3,confidence4,confidence5,confidence6,confidence7]

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
	y,x=run_evaluators()
#	print '----------------------------------------------'
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
	print 'DLDA  '+str(test(train(mlpy.Dlda,y,x)))
	print '----------------------------------------------'

if __name__ == "__main__":
    demo()

