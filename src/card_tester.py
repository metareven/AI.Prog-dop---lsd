import cards

kort = cards.gen_52_shuffled_cards()
#for k in kort:
#    print k

deck1 = []
print "Deck 1: "
for i in range(3):
    deck1.append(kort.pop())
    print deck1[i]
print "Deck 1 power: "
print cards.calc_cards_power(deck1)[0]
#print cards.power_test(deck1)

deck2 = []
print "Deck 2: "
for i in range(7):
    deck2.append(kort.pop())
    print deck2[i]
print "Deck 2 power: "
#print cards.power_test(deck2)
#print cards.power_test([deck1, deck2])

