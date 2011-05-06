#!/usr/bin/env python
#import sys
#sys.path.append('./modules')
#import monte
import chunker
import numpy as np
import mlpy
import random #Just for generating fake data
import tom
import check_answers
import read_questions

questionDict=dict(read_questions.read_questions_no_answers())

def run_evaluators(candidates,evaluators):
	#candidate = list of the question-candidate indexes
	confidence = []
	for candidate in candidates:
		print candidate[0]
		candidateConfidence=[]
		for evaluator in evaluators:
			foo=evaluator(questionDict[str(candidate[4])],candidate)
			candidateConfidence=candidateConfidence+list(foo)
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
	return fit.realpred

def demo():
	candidates_train=[
	('blown', 'AP881126-0094', 55, 'VP'), ('farther', 'AP881126-0094', 56, 'NP'), ('away', 'AP881126-0094', 57, 'S'),
	('by', 'AP881126-0094', 58, 'PP'), ('Tropical Storm Keith', 'AP881126-0094', 59, 'NP'), (',', 'AP881126-0094', 62, 'S'),
	('which', 'AP881126-0094', 63, 'NP'), ('swept through', 'AP881126-0094', 64, 'PP'), ('the Gulf', 'AP881126-0094', 66, 'NP'),
	('of', 'AP881126-0094', 68, 'PP'), ('Mexico', 'AP881126-0094', 69, 'NP'), ('early', 'AP881126-0094', 70, 'S'),
	('last week', 'AP881126-0094', 71, 'NP'), ('.', 'AP881126-0094', 73, 'S'), ('Brydes whales', 'AP881126-0094', 74, 'NP'),
	('are', 'AP881126-0094', 76, 'VP'), ('native', 'AP881126-0094', 77, 'NP'), ('to', 'AP881126-0094', 78, 'PP'),
	('offshore', 'AP881126-0094', 79, 'VP'), ('tropical water', 'AP881126-0094', 80, 'NP'), ('.', 'AP881126-0094', 82, 'S'),
	('Dr', 'AP881126-0094', 83, 'NP'), ('.', 'AP881126-0094', 84, 'S'), ('Dan Odell', 'AP881126-0094', 85, 'NP'),
	(', also', 'AP881126-0094', 87, 'S'), ('the scientific coordinator', 'AP881126-0094', 89, 'NP'), ('for', 'AP881126-0094', 92, 'PP'),
	('the Southeast U .S', 'AP881126-0094', 93, 'NP'), ('.', 'AP881126-0094', 97, 'S'), ('Marine Mammal Stranding Network', 'AP881126-0094', 98, 'NP'),
	(',', 'AP881126-0094', 102, 'S'), ('gave', 'AP881126-0094', 103, 'VP'), ('a dim prognosis', 'AP881126-0094', 104, 'NP'),
	('for', 'AP881126-0094', 107, 'PP'), ("the whale's survival", 'AP881126-0094', 108, 'NP'), (', but', 'AP881126-0094', 111, 'S'),
	('said', 'AP881126-0094', 113, 'VP'), ('the 22-foot', 'AP881126-0094', 114, 'NP'), (',', 'AP881126-0094', 116, 'S'),
	('9-inch mammal', 'AP881126-0094', 117, 'NP'), ('was resting', 'AP881126-0094', 119, 'VP'), ('and', 'AP881126-0094', 121, 'S'),
	('started making', 'AP881126-0094', 122, 'VP'), ('sounds', 'AP881126-0094', 124, 'NP'), ('.', 'AP881126-0094', 125, 'S'),
	("``That's", 'AP881126-0094', 126, 'NP'), ('about', 'AP881126-0094', 127, 'PP'), ('as', 'AP881126-0094', 128, 'S'),
	('good', 'AP881126-0094', 129, 'NP'), ('as', 'AP881126-0094', 130, 'PP'), ('you', 'AP881126-0094', 131, 'NP'),
	('can expect', 'AP881126-0094', 132, 'VP'), ('from', 'AP881126-0094', 134, 'PP'), ('a beached whale', 'AP881126-0094', 135, 'NP'),
	('at', 'AP881126-0094', 138, 'PP'), ('this point', 'AP881126-0094', 139, 'NP'), (",''", 'AP881126-0094', 141, 'S'),
	('said', 'AP881126-0094', 142, 'VP'), ('Odell', 'AP881126-0094', 143, 'NP'), ('.', 'AP881126-0094', 144, 'S'),
	("``It's been", 'AP881126-0094', 145, 'VP'), ('in', 'AP881126-0094', 147, 'PP'), ('a', 'AP881126-0094', 148, 'NP'),
	('very', 'AP881126-0094', 149, 'S'), ('stressful set', 'AP881126-0094', 150, 'NP'), ('of', 'AP881126-0094', 152, 'PP'),
	('circumstances', 'AP881126-0094', 153, 'NP'), ('probably', 'AP881126-0094', 154, 'S'), ('for', 'AP881126-0094', 155, 'PP'),
	('some days', 'AP881126-0094', 156, 'NP'), (".''", 'AP881126-0094', 158, 'S'), ('Squid', 'AP881126-0094', 159, 'NP'),
	('were placed', 'AP881126-0094', 160, 'VP'), ('in', 'AP881126-0094', 162, 'PP'), ("the whale's mouth every three", 'AP881126-0094', 163, 'NP'),
	('or', 'AP881126-0094', 168, 'S'), ('four hours', 'AP881126-0094', 169, 'NP'), (', but', 'AP881126-0094', 171, 'S'),
	('the whale', 'AP881126-0094', 173, 'NP'), ('did', 'AP881126-0094', 175, 'VP'), ('not', 'AP881126-0094', 176, 'S'),
	('respond', 'AP881126-0094', 177, 'VP'), ('well', 'AP881126-0094', 178, 'S'), ('to', 'AP881126-0094', 179, 'PP'),
	('the food', 'AP881126-0094', 180, 'NP'), ('.', 'AP881126-0094', 182, 'S'), ('Odell', 'AP881126-0094', 183, 'NP'),
	('said', 'AP881126-0094', 184, 'VP'), ('they', 'AP881126-0094', 185, 'NP'), ('hoped', 'AP881126-0094', 186, 'VP')
	]
	candidate_test=[('to', 'AP881126-0094', 187, 'PP')]
	x_train=run_evaluators(candidates_train)
	q_id=323
	y_train=map(lambda a: check_answers.check_answer(q_id,a),candidates_train)
	y_train[4]=1
	x_test =run_evaluators(candidate_test)[0]
#	print x_test
	#Run the predictions for just one of these test question candidates
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

