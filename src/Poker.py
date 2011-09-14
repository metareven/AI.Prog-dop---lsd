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

bigBlind = 1
smallBlind= 0
currentPlayer = None
pot = 0
players = []
remainingPlayers = []
tableCards = []
currentBet = 0
deck = []
startingCash = 0
standardRaise = 100
phase = 0

#testkommentar

def main():
    startingCash = 10000
    NewRound()



def NewRound():
    #henter en ny kortstokk og starter en ny runde
    Phase = 0
    deck = cards.gen_52_shuffled_cards
    remaningPlayers = players
    #Trekker kort til alle spillerene
    for p in players:
        p.cards = DrawCards(2)

def BettingRound():
    prePot = pot

    for p in remaningPlayers:
        p.Assess()

    #checking if anyone has raised this round, and if they have,
    #then we start a a new betting round
    while(pot > prePot + (standardRaise * len(remainingPlayers))):
        prePot = pot
        for p in remaningPlayers:
            p.Assess()
    NewPhase()

#starts the next phase, i.e flop, turn, river
def NewPhase():
    phase += 1
    if(len(tableCards) == 0):
        tableCards.append(DrawCards(3))
    else:
        tableCards.append(DrawCards(1))



#Calculate if we have a winner and starts a new round if we have
def FindWinner():
    pass



#Genererer n antall spillere
def GeneratePlayers(n):
    players.append(Player())


def DrawCards(n):
    c = []
    for i in range(n):
        c.append(deck.pop)
    return c





class Player:
    cards = []
    cash = 0
    bet = 0

    def __init__(self):
        self.cards = []
        self.cash = startingCash
        self.bet = 0

    def Fold():
        #Kaster spilleren ut av remainingPlayers
        remainingPlayers.remove(self)


    def Raise(b):
        #?ker potten og minker cash med bet. Setter ogs? currentBet lik bet

        #setter temp til verdien som spilleren m? legge til for ? raise med b
        temp = b + (currentBet - bet)
        bet+=temp
        cash-=temp
        currentBet = temp
        pot += b

    def Call():
        #?ker bet med s? mye som trengs for at bet skal bli lik currentBet
        diff = currentBet - bet
        pot += diff
        cash -= diff
        bet = currentBet






    def Assess():
        #Finner ut om spilleren skal Raise, Calle eller Folde
        power = calc_cards_power(cards)
        rand = random()
        diff = currentBet - bet
        willing = power[0] + (power[1]/14) - rand - (diff/pot)
        if(willing > 1.5):
            raise(standardRaise)
        elif (willing > 0.5):
            call()
        else:
            fold()



if __name__ == '__main__':
    main()
