import cards
import itertools

kortstokk = cards.gen_52_cards()
hole = []
hole.append(kortstokk.pop(0))
hole.append(kortstokk.pop(0))
print hole

for i in range(2,11): # For 2 til 10 players
    

#teststokk = []
#for i in range(10):
#    teststokk.append(kortstokk.pop(0))
#result = list(itertools.combinations(teststokk, 8))
#print len(result)

#stokk = cards.gen_52_cards()
#r = list(itertools.combinations(stokk,2))
#print len(r)



