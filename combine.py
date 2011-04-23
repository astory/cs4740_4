#import sys
#sys.path.append('./modules')
#import monte

import numpy as np
import mlpy

def train():
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
	correct=[True,False,False,True,False,False,False,True,False,True,False]
	#Confidence measures from each of the three answer extraction methods
	confidence1=[0.378183359280229,0.275786651414819,0.48928187857382,0.154237459995784,0.196210152702406,
	0.376024881959893,0.230388485593721,0.108338781050406,0.160494192386977,0.225011750124395,0.355593698564917]
	confidence2=[0.001228122622706,0.0764752259710804,0.328412672388367,0.477082112804055,0.0747434163931757,
	0.405251491814852,0.320799129549414,0.12499387213029,0.0304218637757003,0.0601054372964427,0.460696235764772]
	confidence3=[0.64096049607421,0.557334918684016,0.315573251030097,0.376614285632968,0.601862544659525,
	0.389133446694662,0.245313317359736,0.278548790918042,0.0664477733274301,0.588468289934099,0.476068765856326]

	#Format them for the classification model https://mlpy.fbk.eu/data/doc/classification.html
	xtr = np.array([confidence1,confidence2,confidence3,]
	ytr = np.array(correct)
	svm = mlpy.Svm()  # initialize Svm class
	svm.compute(xtr, ytr)  # compute SVM
	return svm

def test(svm):
	'''
	Guess which test corpus answers are correct based on
	 * The model from the training corpus
	 * The confidence measures from the test corpus
	This also needs to take real paramaters at some point.
	'''
	#Confidence measures for one particular answer
	#from all [let's say 3] QA methods
	confidence=[0.5995270445322,0.219738627163072,0.0829813567300638]

	xts = np.array(confidence) # test point
	print svm.predict(xts)  # predict SVM model on test point
	print svm.realpred # real-valued prediction

def main():
	test(train())


if __name__ == "__main__":
    main()

