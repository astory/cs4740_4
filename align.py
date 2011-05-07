# Some inspiration from Forrest Bao at http://narnia.cs.ttu.edu/drupal/node/104,
# as such, this code is released under the GNU GPL version 3, although the code
# is entirely my own.
#
# copyright Alec Story, 2011
import numpy
import os
import pickle

MATCH = 2
MISMATCH = -1
GAP = "|"

ZERO_POINT = 0
MATCH_POINT = 1
DEL_POINT = 2
INS_POINT = 3

cache = {}

def load_cache(filename="align_cache.pickle"):
    print "loading cache...",
    path = os.path.relpath(filename)
    f = open(path, 'r')
    cache.update(pickle.load(f))
    f.close()
    print "done."

def save_cache(filename="align_cache.pickle"):
    print "saving cache...",
    path = os.path.relpath(filename)
    f = open(path, 'w')
    pickle.dump(cache, f)
    f.close()
    print "done."

def weight(a_i, b_j):
    if a_i == b_j:
        return MATCH
    else:
        return MISMATCH

def abbreviate(a,b):
    a = a[0:20]
    b = b[0:20]
    return (a,b)

def sw_align(a, b):
    """Smith-Waterman alignment
    Source:  http://en.wikipedia.org/wiki/Smith_Waterman

    Aligns a against b

    returns: (score, aligned-a, aligned-b, (a start index, b start index), (a
    end index, b end index))
    """
    a = GAP + a
    b = GAP + b
    if abbreviate(a,b) in cache:
        pass
    else:
        # Definitions:
        # a,b are strings
        # strings start with GAP to keep indices the same as algorithm given
        # if a_i == b_j then w(a_i, b_j) = w(match)
        # if a_i != b_j then w(a_i, b_j) = w(mismatch)
        # H(i,j) is the maximum Similarity-Score between a suffix of a[1..i] and
        # a suffix of b[1..j]
        # w(c,d), c,d in alphabet and '-', '-' is the gap-scoring scheme
        # H(i,0) = 0, 0 <= i <= m
        m = len(a)
        n = len(b)
        H = numpy.zeros((m,n))
        pointers = numpy.zeros((m,n))
        for i in range(1,m):
            for j in range(1,n):
                s_match = H[i-1,j-1] + weight(a[i],b[j])
                s_del = H[i-1, j]  + weight(a[i],GAP)
                s_ins = H[i, j-1]  + weight(GAP,b[j])
                H[i,j] = max(
                    0,
                    s_match,
                    s_del,
                    s_ins
                )

                # build traceback
                if H[i,j] == 0:
                    pointers[i,j] = ZERO_POINT
                elif H[i,j] == s_match:
                    pointers[i,j] = MATCH_POINT
                elif H[i,j] == s_del:
                    pointers[i,j] = DEL_POINT
                else:
                    pointers[i,j] = INS_POINT

        # To obtain the optimum local alignment, we start with the highest value
        # in the matrix (i,j).
        best = (0,0) # value is always 0
        for i in range(1,m):
            for j in range(1,n):
                if H[i,j] > H[best]:
                    best = (i,j)
        # Then, we go backwards to one of positions (i-1,j), (i,j-1), and
        # (i-1,j-1) depending on the direction of movement used to construct the
        # matrix. We keep the process until we reach a matrix cell with zero
        # value, or the value in position (0,0).
        point = best
        align_a,align_b = "", ""
        while pointers[point] != ZERO_POINT:
            i,j = point
            if pointers[point] == MATCH_POINT:
                align_a = a[i] + align_a
                align_b = b[j] + align_b
                point = (i-1, j-1)
            elif pointers[point] == DEL_POINT:
                align_a = a[i] + align_a
                align_b = GAP + align_b
                point = (i-1, j)
            else: #INS_POINT
                align_a = GAP + align_a
                align_b = b[j] + align_b
                point = (i, j-1)
        cache[abbreviate(a,b)] = H[best], align_a, align_b, point, best
    return cache[abbreviate(a,b)]

if __name__ == "__main__":
    load_cache()
    print sw_align("albacore", "bacon")
    print sw_align("albacore", "baecon")
    save_cache()
