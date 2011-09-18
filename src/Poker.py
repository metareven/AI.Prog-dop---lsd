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
import random

bigBlind = None
smallBlind= None
currentPlayer = None
pot = 0
players = []
remainingPlayers = []
tableCards = []
currentBet = 0
deck = []
startingCash = 0
raiseValue = 100 # Verdien det skal okes med nar man raiser



def main():
    startingCash = 10000
    NewRound()



def NewRound():
    # Henter en ny kortstokk og starter en ny runde
    deck = cards.gen_52_shuffled_cards
    remaningPlayers = players
    # Trekker kort til alle spillerene
    for p in players:
        p.cards = DrawCards(2)
    # Forste runde med vedding
    InitialBet()
    # Trekker flop-kort
    tableCards = DrawCards(3)
    # Ny runde med vedding
    FlopBet()
    # Trekker turn-kort
    flop = DrawCards(1)
    tableCards.append(flop[0])
    # Ny runde med vedding
    TurnBet()
    # Trekker river-kort
    river = DrawCards(1)
    tableCards.append(river[0])
    # Siste runde med vedding
    RiverBet()
    # Showdown


def InitialBet():
    # Starter med at smallBlind og bigBlind m? vedde
    smallBlind.Raise(raiseValue)
    bigBlind.Call()
    bigBlind.Raise(raiseValue)
    # Hver spiller m? s? ta fold, call eller raise
    # Det er her helt tilfeldig hva de gj?r
    for p in players:
        if p != smallBlind and p != bigBlind:
            i = random.randint(0,2)
            if i == 0:
                p.Fold()
            elif i == 1:
                p.Raise(raiseValue)
            else:
                p.Call()

def FlopBet():
    # Her velger man handling basert p? power rating
    # Har man power rating p? under 3 velger man Fold
    # Har man power rating mellom 3 og 4 velger man Call
    # Har man power rating p? over 4 velger man Raise
    for p in players:
        hand = p.cards
        for card in tableCards:
            hand.append(card)
        power = cards.calc_cards_power(hand)[0]
        if power > 4:
            p.Raise(raiseValue)
        elif power > 2:
            p.Call()
        else:
            p.Fold()

def TurBet():
    break

def RiverBet():
    break




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
        cash -= currentBet - bet
        pot += currentBet -bet
        bet = currentBet






    #Finner ut om spilleren skal Raise, Calle eller Folde
    def Assess():
        pass



if __name__ == '__main__':
    main()
