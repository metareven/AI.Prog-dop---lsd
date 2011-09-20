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
from collections import deque

bigBlind = None
smallBlind= None
currentPlayer = None
pot = 0
players = deque()
remainingPlayers = []
tableCards = []
currentBet = 0
deck = []
startingCash = 0
raiseValue = 100 # Verdien det skal okes med nar man raiser



def main(number):
    print("starting new game with " , number , " players" )
    global blindNumber, startingCash
    blindNumber = 0
    startingCash = 10000
    GeneratePlayers(number) #lager spillere
    NewRound()

def GeneratePlayers(n):
    print ("generating" , n , "players")
    for i in range(n):
        players.append(Player(i))


def NewRound():
    # Henter en ny kortstokk og starter en ny runde
    #velger ny big blind og small blind
    global bigBlind,smallBlind,players,remainingPlayers, deck
    bigBlind = players[0]
    smallBlind = players[1]
    deck = cards.gen_52_shuffled_cards()
    remainingPlayers = players
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
    players.rotate(1)


def InitialBet():
    # Starter med at smallBlind og bigBlind m? vedde
    print("start initial bet")
    global remainingPlayers
    print("small blind")
    smallBlind.Raise(raiseValue)
    print("big blind")
    bigBlind.Call()
    bigBlind.Raise(raiseValue)
    # Hver spiller m? s? ta fold, call eller raise
    # Det er her helt tilfeldig hva de gj?r
    firstRound = True # Brukes for aa soerge for at smallBlind og bigBlind ikke vedder 2 ganger den foerste runden
    numberOfBettingRounds = 0
    while remainingPlayers and numberOfBettingRounds < 2:
        RemoveFolds()
        for p in remainingPlayers:
            if (p != smallBlind or not firstRound) and (p != bigBlind or not firstRound):
                i = random.randint(0,2)
                if i == 0:
                    p.Fold()
                    #print("player ", p.name, "has folded")
                elif i == 1:
                    p.Raise(raiseValue)
                    #print("player ", p.name," has raised with ", raiseValue )
                else:
                    p.Call()
                    #print("player ", p.name, "has called")
        numberOfBettingRounds += 1
        if firstRound:
            firstRound = False
        print("end initial bet")
                    
def FlopBet():
    # Her velger man handling basert p? power rating
    # Har man power rating p? under 3 velger man Fold
    # Har man power rating mellom 3 og 4 velger man Call
    # Har man power rating p? over 4 velger man Raise
    print("start flop bet")
    numberOfBettingRounds = 0
    global tableCards, remainingPlayers
    while remainingPlayers and numberOfBettingRounds < 1:
        for p in remainingPlayers:
            hand = p.cards
            for card in tableCards:
                hand.append(card)
            power = cards.calc_cards_power(hand)[0]
            if power > 4 and p.bet < 2*raiseValue:
                p.Raise(raiseValue)
            elif power > 2:
                p.Call()
            else:
                p.Fold()
        numberOfBettingRounds += 1
    print("end flop bet")
                
def TurnBet():
    #Her velger man handling basert p powerrating akkurat som etter flop
    print("start turn bet")
    numberOfBettingRounds = 0
    global tableCards, remainingPlayers
    while remainingPlayers and numberOfBettingRounds < 1:
        for p in remainingPlayers:
            hand = p.cards
            for card in tableCards:
                hand.append(card)
            power = cards.calc_cards_power(hand)[0]
            if power > 4 and p.bet < 2*raiseValue:
                p.Raise(raiseValue)
            elif power > 2:
                p.Call()
            else:
                p.Fold()
        numberOfBettingRounds += 1
    print("end turn bet")

def RiverBet():
    #Her velger man handling basert p powerrating akkurat som etter flop
    print("start river bet")
    numberOfBettingRounds = 0
    global tableCards, remainingPlayers
    while remainingPlayers and numberOfBettingRounds < 1:
        for p in remainingPlayers:
            hand = p.cards
            for card in tableCards:
                hand.append(card)
            power = cards.calc_cards_power(hand)[0]
            if power > 4 and p.bet < 2*raiseValue:
                p.Raise(raiseValue)
            elif power > 2:
                p.Call()
            else:
                p.Fold()
        numberOfBettingRounds += 1
    print("end river bet")


def DrawCards(n):
    global deck
    c = []
    for i in range(n):
        card = deck.pop()
        c.append(card)
    return c

def RemoveFolds():
    global remainingPlayers
    temp = deque(remainingPlayers)
    for p in remainingPlayers:
        if not p.playing:
            temp.remove(p)
    remainingPlayers = temp

def CheckIfFinished():
    global remainingPlayers
    if len(remainingPlayers) == 1:
        print("the winner is: " + str(remainingPlayers[0].name))
        



class Player:
    cards = []
    cash = 0
    bet = 0
    name = 0
    playing = True

    def __init__(self,n):
        self.cards = []
        self.cash = startingCash
        self.bet = 0
        self.name= n

    def Fold(self):
        #Kaster spilleren ut av remainingPlayers
        self.playing = False
        print("player ", self.name, " has folded")
        CheckIfFinished()


    def Raise(self, b):
        #?ker potten og minker cash med bet. Setter ogs? currentBet lik bet
        global currentBet, pot
        #setter temp til verdien som spilleren m? legge til for ? raise med b
        temp = b + (currentBet - self.bet)
        self.bet+=temp
        self.cash-=temp
        currentBet = temp
        pot += b
        print("player " , self.name, " has raised by ", b  )

    def Call(self):
        #?ker bet med s? mye som trengs for at bet skal bli lik currentBet
        global currentBet, pot
        self.cash -= currentBet - self.bet
        pot += currentBet - self.bet
        self.bet = currentBet
        print("player", self.name , "has called")

    #Finner ut om spilleren skal Raise, Calle eller Folde
    def Assess():
        pass



if __name__ == '__main__':
    main(4)
