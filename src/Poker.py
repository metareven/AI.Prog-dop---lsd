#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lars
#
# Created:     13.09.2011
# Copyright:   (c) Lars 2011
# Licence:     <BSD>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import random
import math
import cards

bigBlind
smallBlind
currentPlayer
pot
players
remainingPlayers
tableCards
currentBet
deck

def main():
    pass

def NewRound():
    deck = cards.gen_52_shuffled_cards
    remaningPlayers = players

def DrawCards(n):
    c = []
    for i in range(n):
        c.append(deck.pop)
    return c





class Player:
    self.cards
    self.cash
    self.bet

    def Fold():
        #Kaster spilleren ut av remainingPlayers
        pass


    def Raise(bet):
        #?ker potten og minker cash med bet. Setter ogs? currentBet lik bet
        pass

    def Call():
        #?ker bet med s? mye som trengs for at bet skal bli lik currentBet
        pass

    def Assess():
        #Finner ut om spilleren skal Raise, Calle eller Folde
        pass



if __name__ == '__main__':
    main()
