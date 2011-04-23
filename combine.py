#import sys
#sys.path.append('./modules')
#import monte

import numpy as np
import mlpy

def train(model):
	'''
	Train a model for classifying answers as correct or not
	based on the confidence measures from various QA methods.
	This should support paramaters at some point.
	'''

	#Here are some answers. We probably won't use them at all.
	answers=[
	'Alaska, Canada, Greenland and Soviet Union',
	'rare medabolic disorder',
	'about 100,000 light years',
	'saguaro, (evens giganteius)',
	'an eating disorder',
	'Nina, Pinta and Santa Maria',
	'Chester A. Arthur',
	'Braintree , now Quincy, Mass.',
	'an Aztec god',
	'South American Indian mythical god',
	'connects the two spheres of the brain'
	]

	#Whether each of these answerse is correct
	#correct=[True,False,False,True,False,False,False,True,False,True,False]
	correct=[1,-1,-1,1,-1,-1,-1]
	#Confidence measures from each of the three answer extraction methods for seven questions
	confidence1=[0.978183359280229,0.275786651414819,0.48928187857382]
	confidence2=[0.154237459995784,0.196210152702406,0.376024881959893]
	confidence3=[0.230388485593721,0.108338781050406,0.160494192386977]
	confidence4=[0.001228122622706,0.0764752259710804,0.328412672388367]
	confidence5=[0.64096049607421,0.557334918684016,0.315573251030097]
	confidence6=[0.389133446694662,0.245313317359736,0.278548790918042]
	confidence7=[0.0664477733274301,0.588468289934099,0.476068765856326]

	#Format them for the classification model https://mlpy.fbk.eu/data/doc/classification.html
	xtr = np.array([confidence1,confidence2,confidence3,confidence4,confidence5,confidence6,confidence7])
	ytr = np.array(correct)
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
	if fit.predict(xts)==-1:
		#print fit.realpred # real-valued prediction. I'm not sure what this is. I guess it's the predicted Y value?
		return False
	elif fit.predict(xts)==1:
		return True

def main():
	print 'Predictions for random data from various models'
	print ' SVM result: '+str(test(train(mlpy.Svm)))
	print ' KNN result: '+str(test(train(mlpy.Knn)))
	print ' FDA result: '+str(test(train(mlpy.Fda)))
	print 'SRDA result: '+str(test(train(mlpy.Srda)))
	print ' PDA result: '+str(test(train(mlpy.Pda)))
	print 'DLDA result: '+str(test(train(mlpy.Dlda)))

if __name__ == "__main__":
    main()

