#!/usr/bin/env python
from combine import *
import init
import chunker
import mlpy
import check_answers
import align
from packer import pack
from sequence_length import       seq_length  
from punctuation_location import  punc_loc            
from apposition import question_apposition, rewrite_apposition  
from question_rewrite import literal_question_distance, literal_rewrite_distance, align_question_distance, align_rewrite_distance
from pos import                   pos_test
from bag_of_words import   vector_bag,  bag_of_words        
from novelty_factor import novelty_bool, novelty_count       
import cache_chunkers
from math import floor

question_dict = dict(read_questions.read_questions_no_answers())
def get_question(q_id):
    return question_dict[str(q_id)]

def cache_file(q_id):
    base=int(10*floor(q_id/10))
    low=base+1
    high=base+10
    name='chunks/'+str(low)+'-'+str(high)+'.txt'
    return name

DIST_CUTOFF = 50
SCORE_CUTOFF = 5

def question_candidates(q_id):
    '''Select some useful subset of the candidates for a particular question.
    Return them in a list.
    '''
    init.get_corpus(qNum=q_id)
    foo=cache_file(q_id)
    candidate = cache_chunkers.uncache_chunks(open(foo))[q_id]
    new_l = []
    for c in candidate:
        if (c[3] == "NP"):
            dist = align_question_distance(get_question(q_id), c)
            if dist[0] < DIST_CUTOFF and dist[1] > SCORE_CUTOFF:
                new_l.append(c)
    align.save_cache()
    print len(new_l)
    return new_l[:2000]

def question_learning_data(evaluators,first,last):
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

def run_question_predictions(evaluators,trained_model,first,last):
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
    trainIDs=[334,338]
    validationIDs=[339,339]
    testIDs=[338,338]
    evaluator_combinations=[
#    [],
#    [seq_length],
#    [punc_loc]
#    [bag_of_words],
#    [novelty_bool],
    [pos_test]
#    [seq_length,punc_loc,question_apposition,rewrite_apposition,pos_test,vector_bag,bag_of_words,novelty_bool] #,novelty_count]
#    [novelty_count]
    ]
    evaluatorCombinationID=1
    for evaluators in evaluator_combinations:
        y_train,x_train = question_learning_data(evaluators,trainIDs[0],trainIDs[1])
#        print y_train
        trained=train(mlpy.Srda,y_train,x_train)
        results=run_question_predictions(evaluators,trained,validationIDs[0],validationIDs[1])
        writeAnswers(answerFile(results),'results/combination'+str(evaluatorCombinationID)+'.txt')
        evaluatorCombinationID=evaluatorCombinationID+1
    
if __name__ == '__main__':
    align.load_cache()
    main()
    align.load_cache()
    align.save_cache()
    question_candidates (243)
