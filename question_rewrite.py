#!/usr/bin/env python

# returns Question#, Rewritten Question as either a dictionary or list.

# This re-writes questions, so for:
# "Who is the President?"  you get:
# "the President is "
# Not all questions lend themselves to simple rewrites, in this case I return an
# empty string

from align import sw_align
from difflib import SequenceMatcher as SequenceMatcher
import init
import chunker
import read_questions
import sys

MAX_INT = sys.maxint

def literal_question_distance(question, (answer, doc_num, index, features,q_id)):
    """Evaluates a candidate based on how close it is to the longest fragment of
    the question in the document

    returns (distance, length of fragment)
    """
    doc = chunker.clean_punctuation(init.get_doc(doc_num))
    (start, _, length) = find_match(question, doc)
    words = doc.split()
    index = len(" ".join(words[0:index+1]))
    return (min( abs(start - index),
        abs(start + length - index),
        0 if start <= index <= start + length else MAX_INT), length)

def literal_rewrite_distance(question, candidate):
    """Evaluates a candidate based on how close it is to the longest fragment of
    the re-written question in the document

    returns (distance, length of fragment)
    """
    return literal_question_distance(rewriteQuestion(question), candidate)

def align_question_distance(question, (answer, doc_num, index, features,q_id)):
    """Evaluates a candidate based on how close it is to the alignment of the
    question in the document

    returns (distance, score)
    """
    doc = chunker.clean_punctuation(init.get_doc(doc_num))
    (score, q, d, (q_start, d_start), (q_end, d_end)) = sw_align(question, doc)
    words = doc.split()
    index = len(" ".join(words[0:index+1]))
    return (min( abs(d_start - index),
        abs(d_end - index),
        0 if d_start <= index <= d_end else MAX_INT), score)

def align_rewrite_distance(question, candidate):
    """Evaluates a candidate based on how close it is to the alignment of the
    re-written question in the document

    returns (distance, score)
    """
    return align_question_distance(rewriteQuestion(question), candidate)
    

def rewriteQuestion(question):
    """Attempts to re-write a question
    
    Takes a question as a string, and attempts to re-write it with simple rules.

    Returns a possible re-write, or the empty string
    """

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

def unwrap_match(doc, match):
    """gets the original text assuming doc is a"""
    return doc[match.a:match.a+match.size]

def find_match(question, doc):
    """Finds occurences of question in docs

    Returns the longest match, where a match is a Named Tuple. Use
    unwrap_match(doc, match) to unwrap them or for more documentation.
    """
    question = question.lower()
    doc = doc.lower()
    sm = SequenceMatcher()
    sm.set_seqs(doc,question)
    return sm.find_longest_match(0,len(doc),0,len(question))

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
    init.get_corpus(qNum=209)
    question = "Who is the inventor of the phonograph?"
    doc = "SJMN91-06010225"
    print align_question_distance(question, (1, doc, 30, {}))
