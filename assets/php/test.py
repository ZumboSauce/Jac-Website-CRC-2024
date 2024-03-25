import random
from math import floor
import numpy as np

def splice_random(tgt, n, max_chunk):
    tgt_sorted = sorted(tgt)
    empty = (tgt_sorted[-1] - tgt_sorted[0]) - len(tgt)
    empty = empty if empty > 0 else 0
    sample_nerf = n - len(tgt) + 1 if len(tgt) <= n else 0
    delims = [tgt[0], *sorted(random.sample(range(tgt_sorted[0]+1, tgt_sorted[-1]), n-(1+sample_nerf))), tgt[-1]-empty]
    while(True):
        if len([size for size in [delims[i+1] - delims[i] for i in range(n-sample_nerf)] if size > max_chunk]):
            delims = [tgt[0], *sorted(random.sample(range(tgt_sorted[1], tgt_sorted[-2]), n-(1+sample_nerf))), tgt[-1]-empty]
            continue
        break  
    random.shuffle(tgt)
    it = iter(tgt)
    return [[next(it) for _ in range(size)] for size in [delims[i+1] - delims[i] for i in range(n-sample_nerf)]] + [[] for _ in range(sample_nerf)]


card = {}

#select all under i * 10
#get sample of size selection from 0 to 2
#set keys in dict using comprehension where  row * 10 + i: value

