#!/usr/bin/env python

# question filter that takes a question and its rewritten form and
# finds the length of the maxmimum sequence between this and the
# answer. A sequence is a list of (not necessarily consecutive) words
# that are shared by two sentences.

import question_rewrite

def seq_length (question, (answer, doc_num, index, features,q_id)):
    """Takes a question and rewrites it. It then returns a list of
       lengths of maximum sequences between the question/answer and
       rewritten question/answer
       
       returns [max_seq_len, max_seq_len_rewrite] (int list)
    """
    ans = (seq_length_literal (question, (answer, doc_num, index, features,q_id)),
           seq_length_rewrite (question, (answer, doc_num, index, features,q_id)))
    return ans

def seq_length_literal (question, (answer, doc_num, index, features,q_id)):
    """Takes a question and calculates the maximum sequence length
       that the question and the answer have in common.
       
       returns max_seq_len (int)
    """
    if(len(question) == 0 or len(answer) == 0):
        return 0
    else:
        # remove puncutation
        question.replace("<space>", "")
        answer.replace("<space>", "")
        punc = [".", ",", ":", ".", "?", "!", "'", "\"", ")", "(", "-"]
        question = ''.join([w for w in question if w.lower() not in punc])
        answer = ''.join([w for w in answer if w.lower() not in punc])

        # tokenize the question and answer
        question = (question.lower()).split()
        answer = (answer.lower()).split()

        # straight from the internet...
        m = len(question)
        n = len(answer)
        # An (m+1) times (n+1) matrix
        C = [[0] * (n+1) for i in range(m+1)]
        for i in range(1, m+1):
            for j in range(1, n+1):
                if question[i-1] == answer[j-1]: 
                    C[i][j] = C[i-1][j-1] + 1
                else:
                    C[i][j] = max(C[i][j-1], C[i-1][j])
        return C[i][j]

def seq_length_rewrite (question, (answer, doc_num, index, features,q_id)):
    """Rewrites the supplied question and calculates the maximum
       sequence length that the question and the answer have in common.
       
       returns max_seq_len_rewrite (int)
    """
    question = question_rewrite.rewriteQuestion(question)
    return seq_length_literal(question, (answer, doc_num, index, features,q_id))
