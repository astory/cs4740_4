import nltk.chunk
import nltk
from nltk.corpus import conll2000
import itertools
from nltk import pos_tag, word_tokenize

class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents): 
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data) 

    def parse1(self, sentence): 
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        #conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
         #            in zip(sentence, chunktags)]
        #return nltk.chunk.conlltags2tree(conlltags)
        conlltags = [(word +' '+ pos +' '+ chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return conlltags

    def parse2(self, tokens):
        # split words and part of speech tags
        (words, tags) = zip(*tokens)
        # get IOB chunk tags
        chunks = self.tagger.tag(tags)
        # join words with chunk tags
        wtc = itertools.izip(words, chunks)
        # w = word, t = part-of-speech tag, c = chunk tag
        lines = [' '.join([w, t, c]) for (w, (t, c)) in wtc if c]
        # create tree from conll formatted chunk lines
        return nltk.chunk.conllstr2tree('\n'.join(lines))


def run(q_id):
    train_sents = conll2000.chunked_sents('train.txt')
    unigram_chunker = UnigramChunker(train_sents)

    import init
    #get document here and tag; put into this format:
    #tagged = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN"),(".", ".")]
    topdoc = init.get_corpus(q_id)
    doc_nums = topdoc.keys()
    for key in doc_nums[:1]:
        doc_text = topdoc[key]
        doc_text = doc_text.replace("."," .")
        doc_text = doc_text.replace(","," ,")
        #print doc_text
        doc_text= doc_text.split()
        tagged=pos_tag(doc_text)

    answers= [];
    chunked=unigram_chunker.parse2(tagged)
    answers=[]
    flatten= chunked.pos()
    #print flatten
    numbered= enumerate(flatten)
    currentTag=''
    words=[]
    for i,v in numbered:
        #print i,v
        ((word,tag),phrasetag)=v
        if currentTag=='':
            currentTag=phrasetag
        if currentTag==phrasetag:
            words.append(word)
        else:
            feature_dict = {currentTag: 1}
            answers.append((' '.join(words),q_id,i-len(words),feature_dict))
            currentTag= phrasetag
            words= [word]
    feature_dict = {currentTag: 1}
    answers.append((' '.join(words),q_id,i-len(words),feature_dict))
          
    return answers


if __name__=="__main__":
    print run(201)
    
