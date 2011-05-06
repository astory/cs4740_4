#!/usr/bin/env python
from align import sw_align
from question_rewrite import rewriteQuestion
import init

def question_apposition(question, (answer, doc_num, index, features,q_id)):
    doc = init.get_doc(doc_num)
    apposition = question + ", " + answer + ","
    plain = question + " " + answer

    (app_score, app, doc_app, starts, ends) = sw_align(apposition, doc)
    (plain_score, pl, doc_pl, starts, ends) = sw_align(plain, doc)

    return max(0, app_score - plain_score)

def rewrite_apposition(question, candidate):
    return question_apposition(rewriteQuestion(question), candidate)

if __name__ == "__main__":
    init.get_corpus(qNum=209)
    question = "Who is the inventor of the phonograph?"
    doc = "SJMN91-06010225"
    print question_apposition(question, ("joe smith", doc, 700, {}))
    print rewrite_apposition(question, ("joe smith", doc, 700, {}))
