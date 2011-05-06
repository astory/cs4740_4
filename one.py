#!/usr/bin/env python
from combine import *
import chunker
import mlpy
import check_answers
from packer import pack
from sequence_length import       seq_length  
from punctuation_location import  punc_loc            
from apposition import question_apposition, rewrite_apposition  
from pos import                   pos_test
from bag_of_words import   vector_bag,  bag_of_words        
from novelty_factor import novelty_bool, novelty_count       


def question_candidates(q_id):
#Incomplete
	'''Select some useful subset of the candidates for a particular question.
	Return them in a list.
	'''
	return [ ('sling', 'AP881126-0094', 55, 'VP',q_id), ('farther', 'AP881126-0094', 56, 'NP',q_id), ('away', 'AP881126-0094', 57, 'S',q_id)]

def question_learning_data(evaluators,first=204,last=204):
	x=[]
	y=[]
	for q_id in range(first,last+1):
		cand=question_candidates(q_id)
		x=x+run_evaluators(cand,evaluators)
		y=y+map(lambda a:check_answers.check_answer(q_id,a),cand)
	return y,x

def question_prediction_data(q_id,candidate,evaluators):
	x=run_evaluators([candidate],evaluators)
	return x[0],candidate

def run_question_predictions(evaluators,trained_model,first=205,last=206):
	answers=[]
	for q_id in range(first,last+1):
		y_hat=[]
		for candidate in question_candidates(q_id):
			x_test,candidate= question_prediction_data(q_id,candidate,evaluators)
			y_hat.append( ( test(trained_model,x_test) , candidate ) )
		y_hat = sorted(y_hat, key=lambda (s,_): s,reverse=True)
		y_hat = map(lambda a:(a[0],a[1][0]),y_hat)
		for i in range(0,5):
			answers.append((q_id,pack(y_hat, 50)[0]))
	return answers

def answerLine(answer):
        return str(answer[0])+' OVER9000 '+answer[1]

def answerFile(answers):
        return "\n".join(map(answerLine,answers))

def writeAnswers(stuff,filename='tmp-answers.txt'):
        answersHandle=open(filename,'w')
        answersHandle.write(stuff)
        answersHandle.close()

def main():
	evaluator_combinations=[
	[seq_length],
#	[punc_loc],
	[pos_test]
#	[seq_length,punc_loc,question_apposition,rewrite_apposition,pos_test,vector_bag,bag_of_words,novelty_bool] #,novelty_count]
#	[novelty_count]
	]
	for evaluators in evaluator_combinations:
		y_train,x_train = question_learning_data(evaluators)
		trained=train(mlpy.Svm,y_train,x_train)
		writeAnswers(answerFile(run_question_predictions(evaluators,trained)),'results/'+str(evaluators))
	
if __name__ == '__main__':
	main()
