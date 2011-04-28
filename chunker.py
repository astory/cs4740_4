#!/usr/bin/env python

# uses the files init.py to get the corpus data
# uses 10 word chunking to form answers

import init

def get_chunked_sentences(namedEntity,q_ids):
    chunk= []
    for q_id in q_ids:
        topdoc = init.get_corpus(q_id)
        doc_nums = topdoc.keys()
        for key in doc_nums[:5]:
            doc_text = topdoc[key].split()
            # pull out sentences from docs that have that word
            positions = [i for i,x in enumerate(doc_text) if x == namedEntity]
            # get a random position
            for pos in positions:
                chunk.append(' '.join(doc_text[(pos - 5):(pos + 5)]))
    return chunk

if __name__=="__main__":
    items= get_chunked_sentences('military',[201,202,203])
    for item in items:
        print item



