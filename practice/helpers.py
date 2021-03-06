from six.moves import xrange
from multiprocessing import Pool
from sklearn.metrics.pairwise import cosine_similarity as coss

# import cPickle as pickle
from six.moves import cPickle as pickle
import tqdm
import numpy as np
import scipy
import math


seed = 3


def mycossim(v1, v2):
    return coss([v1], [v2])[0][0]


def normalizer(myvector):
    mysum = 0.
    for myvalue in myvector:
        mysum += myvalue * myvalue
    if mysum <= 0.:
        return myvector
    mysum = math.sqrt(mysum)
    newvector = []
    for myvalue in myvector:
        newvector.append(myvalue/mysum)
    return newvector


def emblookup(words, word2vec):
    ret = []
    for w in words:
        w = w.lower()
        if w not in word2vec:
            continue
        ret.append(word2vec[w])
    return ret


def emblookup_verbose(words, word2vec):
    ret = []
    ret_w = []
    for w in words:
        w = w.lower()
        if w not in word2vec:
            continue
        ret.append(word2vec[w])
        ret_w.append(w)
    return ret_w


def line_process(l):
    l = l.strip().split()
    try:
        word = l[0].decode("utf-8").lower()
    except:
        return (None, None)
    vals = normalizer([float(v) for v in l[1:]])
    return (word, vals)


def word2vec(emb_path):
    word2vec = {}
    pool = Pool(4)
    with open(emb_path, "rb") as f:
        pairs = pool.map(line_process, tqdm.tqdm(f.readlines()[1:]))
    pool.close()
    pool.join()
    _pairs = []
    for p in pairs:
        if p[0] is not None:
            _pairs.append(p)
    return dict(_pairs)
