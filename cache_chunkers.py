import chunker
import pickle

def cache_chunks (l, file_):
  pickle.dump(l,file_, pickle.HIGHEST_PROTOCOL)

def uncache_chunks (file_):
  return pickle.load(file_)

