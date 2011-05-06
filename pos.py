from chunker import run
import read_questions

# The chunker spits out an answer candidate, docnum, the word index, and feature (either NP, VP, PP or S)
# This (pos_test) will look at the question and try to determine if NP or VP is more appropriate
# PP and S get 0 so they will not be part of our answer.
# Turns out I don't see any questions where a VP is likely, so I made VP = 0.1, 0 might even be better.

def pos_test(question, (answer, doc_num, index, features,q_id)):
    result = 0
    if features == "NP":
        result = 1
    if features == "VP":
        result = 0.1    

    return result


if __name__ == "__main__":
    testQ = 213
    answers = run(testQ)
    #print answers
    #for ansCandidate in answers:
        #print ansCandidate[0], ansCandidate[3]

    # Again I stick the questions into a dictionary
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
        #print key, qDict[key]
        # I'm just going to pick one question to debug
        if key == str(testQ):
            #print key, qDict[key]
            for ansCandidate in answers:
                myAnswer = pos_test(qDict[key], ansCandidate)
                print ansCandidate[0], myAnswer


