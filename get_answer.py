#!/usr/bin/env python

# uses the files init.py and read_questions.py to get the corpus data
# uses 10 word chunking (the beginning of each file) to form answers
# uses submit.py to format and submit to the automatic scorer

import random

import init
import read_questions
import submit

def get_answer(first = 380, last = 399):
    """ the process by which the baseline finds answers from the corpus
        first : an integer corresponding to the first question id (inclusive) to answer
        last : an integer corresonding to the last question id (inclusive) to answer
        returns : an int list and string list of question id's and answers """
    
    q_ids = []
    ans_text = []

    # make sure the parameters are good
    if first > last: last, first = first, last

    # read in all the questions and iterate through them
    questions = read_questions.read_questions_no_answers()
    questions = [q for q in questions if int(q[0]) >= first and int(q[0]) <= last]
    for question in questions:
        q_id = int(question[0])
        topdoc = init.get_corpus(q_id)
        doc_nums = topdoc.keys()
        
        # baseline QA system answer process right here...
        for key in doc_nums[:5]:
            doc_text = topdoc[key].split()
            # find a random word from the question
            qs = question[1].split()
            qword = qs[random.randint(0, len(qs) - 1)]
            # pull out sentences from docs that have that word
            positions = [i for i,x in enumerate(doc_text) if x == qword]
            # get a random position
            if len(positions) == 0: positions = [len(doc_text) / 2]
            pos = positions[random.randint(0, len(positions) - 1)]
            q_ids.append(q_id)
            ans_text.append(' '.join(doc_text[(pos - 5):(pos + 5)]))

    return q_ids, ans_text

def to_file(question_ids, answers, filename = "output.txt"):
    """ Uses submit.py to format answers and writes to a file
        question_ids : int list of question ids corresponding to answers
        answers : string list of answer text
        filename : filename to write output """
    
    fh = open(filename, 'w')
    f_contents = submit.formatAnswers(question_ids, answers)
    fh.write(f_contents)
    fh.close()

def run_baseline(write_to_file = "", send_to_scorer = ""):
    """ Run get_answers and do something with them.
        write_to_file : if this is not "", then set it to a filename and it will write to it
        send_to_scorer : string of your netid, submit this to the 4740 scorer website """

    q, a = get_answer()
    out = submit.formatAnswers(q, a)
    print out
    print "==============="

    if(len(send_to_scorer) > 0):
        print submit.submit(send_to_scorer, out)
    if(len(write_to_file) > 0):
        to_file(q, a, write_to_file)
        print "Written to " + write_to_file
