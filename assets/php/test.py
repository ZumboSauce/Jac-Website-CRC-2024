import random
from math import floor

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

gen_cols = []
rows = []
for i in [[j for j in sorted(random.sample(range(0, 100), 90)) if floor(j/10)==k] for k in range(10)]:
    gen_cols.append(splice_random(i, 6, 3))
for i in range(6):
    card = {idx: None for idx in range(27)}
    layout = [0 for _ in range(10)]
    for cols in [row for row in [sorted([row for row in random.sample(range(10), 5)]) for __ in range(3)]]:
        for col in cols:
            layout[col] += 1
    for col in range(10):
        print(random.choice([gen for gen in gen_cols[col] if len(gen) == layout[col]]))