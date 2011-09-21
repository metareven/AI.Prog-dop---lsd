import cards

kort = cards.gen_52_shuffled_cards()
#for k in kort:
#    print k

deck1 = []
print "Deck 1: "
for i in range(7):
    deck1.append(kort.pop())
    print deck1[i]
print "Deck 1 power: "
power1 = cards.calc_cards_power(deck1)
print power1

deck2 = []
print "Deck 2: "
for i in range(7):
    deck2.append(kort.pop())
    print deck2[i]
print "Deck 2 power: "
power2 = cards.calc_cards_power(deck2)
print power2
print cards.card_power_greater(power1, power2)

