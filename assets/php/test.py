import random
import numpy as np
import copy
import timeit


gen_rows = []
cards = []
while True:
    try:
        thing = [random.sample([idx for idx in range(col * 10, col * 10 + 10)], 10) for col in range(9)]
        gen_rows = random.sample([[row for row in [thing[idx].pop() for idx in np.random.choice(range(9), size=5, replace=False, p=[len(col)/np.sum([len(col) for col in thing]) for col in thing])]] for _ in range(18)], 18)
    except:
        continue
    break
p = lambda d: zip(d.keys(), sorted(d.values()))

for i in range(6):
    card_sorted = dict()
    a = {k:sorted(gen_rows.pop())+[0] for k in range(3)}
    { {idx:row.pop() for idx,row in a if j*10 <= row[0] < (j+1)*10} }
    #{k*9+j:v for k,v in p( { idx: for idx, row in enumerate(a) if j*10 <= row[0] < (j+1)*10 } )
    #card_sorted.update( {k*9+j:v for k,v in p( { idx:row.pop(0) for idx, row in enumerate(a) if j*10 <= row[0] < (j+1)*10 } )} )
    print(card_sorted)

        

            
