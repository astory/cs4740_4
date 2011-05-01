#!/usr/bin/env python

# returns Question#, Rewritten Question as either a dictionary or list.

# This re-writes questions, so for:
# "Who is the President?"  you get:
# "the President is "
# Not all questions lend themselves to simple rewrites, in this case I return an
# empty string

import read_questions

def rewriteQuestion(question):
    qReWrite = ""
    qi = 0
    qVerb = ""
    # includes spaces around "is" so words containing "is" aren't matched
    qIndex = question.find(" is ")
    if qIndex != -1:
        qi = 4
        qVerb = " is "
    else:
        qIndex = question.find(" was ")
        if qIndex != -1:
            qi = 5
            qVerb = " was "
    # I also tried "are" and "were", rarely was the rewrite grammatically
    # correct.           

    if qi > 0:
        # take the string after the "is/was"
        qReWrite = question[qIndex + qi:]
        # remove the "?"
        qReWrite = qReWrite[:len(qReWrite)-1]
        # if ends in "ed" (VBN) stick verb in front of it
        if qReWrite.endswith("ed"):
            # find index of last space before "ed" word
            qSpace = qReWrite.rfind(" ")
            qReWrite = qReWrite[:qSpace] + qVerb + qReWrite[qSpace + 1:]
        # "Where was" sometimes needs the verb to go between the NP and the
        # adjective this works fine on the test questions, but could easily
        # be fooled on the unknown questions
        elif question.startswith("Where was"):
            qSpace = qReWrite.rfind(" ")
            qReWrite = qReWrite[:qSpace] + qVerb + qReWrite[qSpace + 1:]
        else:
            qReWrite = qReWrite + qVerb
        return qReWrite

def rewriteQuestionsList():
    # calls the dictionary version and plugs it into a list of lists (like
    # read_questions is presented)
    qDict = rewriteQuestionsDict(read_questions.read_questions_no_answers())
    questionsList = []
    for key in qDict:
        questions = []
        questions.append(key)
        questions.append(qDict[key])
        questionsList.append(questions)
    return questionsList        
    
def rewriteQuestionsDict(qList):
    result = {}
    # because a dictionary is easier for me than a list of lists
    # key: string_of_int(question_number)
    # value: question as a string
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

    # now loop through the dict, rewriting if possible
    for key in qDict:    
        result[key] = rewriteQuestion(qDict[key])

    return result

if __name__ == "__main__":
    print rewriteQuestionsList()
