#!/usr/bin/env python

# returns Question#, Rewritten Question as either a dictionary or list.

# This re-writes questions, so for:
# "Who is the President?"  you get:
# "the President is "
# Not all questions lend themselves to simple rewrites, in this case I return an
# empty string

from difflib import SequenceMatcher as SequenceMatcher
import read_questions

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

def find_match(question, documents):
    """Finds occurences of a question and a re-written question in documents

    Returns a list of (match, match), where a match is a Named Tuple. Use
    unwrap_match(doc, match) to unwrap them or for more docs.
    """
    question = question.lower()
    rewrite = rewriteQuestion(question)
    sm = SequenceMatcher()
    sm.set_seq2(question)
    smrw = SequenceMatcher()
    smrw.set_seq2(rewrite)
    matches = []
    for doc in documents:
        doc = doc.lower()
        smrw.set_seq1(doc)
        sm.set_seq1(doc)
        m = sm.find_longest_match(0,len(doc),0,len(question))
        mrw = smrw.find_longest_match(0,len(doc),0,len(rewrite))
        print unwrap_match(doc, mrw)
        matches.append((m,mrw))
    return matches

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
    print find_match("Who invented the phonograph?", [""" If these seemingly disparate historical tidbits attract you, then leaf through "The New York Public Library Desk Reference," a book full of surprises. It is based on the more than 5 million questions the library and its 82 branches answer each year.;    Vartan Gregorian, former president and chief executive officer of the library, writes in his preface, ". . . unlike annuals and almanacs that need revising and updating each year, the Desk Reference (Stonesong Press, $34.95) holds a considerable amount of true reference information, unchanging basic facts and background.;    "We also hope that our book will be easy to read and fun to browse through.";    It is.;    For instance, if you know Thomas Alva Edison invented the phonograph in 1878, you will be pleased to know L.O. Colvin  invented the milking machine the same year, and James J. Ritty  invented the cash register the year after that.;    These were heady times, a veritable cascade of brainstorms. But every year was like that.;    For instance, last year was the 110th birthday of the hearing aid, and the 120th for linoleum and the snap button. It also was the 100th anniversary of motion pictures and the electric subway. It was the 90th anniversary of the paper clip.;    This year is the 100th birthday of the flashlight (by England's Bristol Electric Lamp Co.), the aluminum boat (by Switzerland's Escher Wyss &amp; Co.) and the zipper (by Whitcombe L.  Judson).; The Desk Reference has less esoteric fare. It tells you how to write your member of congress and how to call toll-free for rental cars and hotels.  There are 15 pages of visa requirements to travel anywhere from Afghanistan to Zimbabwe.;    There is an illustrated section on the human anatomy and one on how to play board games from backgammon to Scrabble or cards  from blackjack to solitaire.;    There is simply no way to list all of the tidy bits of information from dietary tables to musical terms and symbols,  from extinct animals to semaphore, from etiquette to legal forms, from animal first aid to a directory of poison control centers.;    It's also a settler of arguments.  Take religion: The book says there are 648 million Hindus, 18 million Jews, 840 million Muslims, 158 million Orthodox Catholics, 307 million Buddhists and 5.6 million followers of Confucius.;    In the United States, there are 31 million Baptists, 2.7 million Episcopalians, 13.5 million Methodists, 2.8 million Mormons, 8 million Lutherans and 700,000 Jehovah's Witnesses. But worldwide, there are 900 million Roman Catholics, the largest Christian Church in the world. It takes 6 1/2 pages to list all the popes.;    One thing that strikes the reader is how long ago some of the inventions sprang from the human mind. And what in the world did mankind do before they came along?; We were blessed with the screwdriver and wrench about 1550 by unknown"""])
