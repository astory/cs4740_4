#!/usr/bin/env python
from combine import *
import chunker
import mlpy
import chunker
import cache_chunkers

def write (start,stop,filename):
  d = {}
  for x in range(start,stop):
    all_chunks = chunker.run(x)
    print x
    d[x] = all_chunks
  cache_chunkers.cache_chunks(d, open(filename, "r+"))
