import nltk.chunk
import nltk
from nltk.corpus import conll2000
import itertools
from nltk import pos_tag, word_tokenize
import chunker
import read_questions
import pos
def filter_chunks(q_id):
    answers = chunker.run(q_id)
    my_answers = []
    
    qList = read_questions.read_questions_no_answers()
    qDict = {}
    b = 0
    for q in qList:
        for q2 in q:
            if b == 0:
                qN = q2
                b = 1
            else:
                qDict[qN] = q2
                b = 0
                
    for key in qDict:
        if key == str(q_id):
            for ansCandidate in answers:
                print ansCandidate
                passed = pos.pos_test(qDict[key], ansCandidate)
                if (passed !=0):
                    my_answers.append(ansCandidate)
                    
    return my_answers


if __name__=="__main__":
    print filter_chunks(213)
