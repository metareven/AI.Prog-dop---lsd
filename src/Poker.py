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
    #print(cards.power_test(1))
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
    global bigBlind,smallBlind,players,remainingPlayers,tableCards, deck
    bigBlind = players[0]
    smallBlind = players[1]
    deck = cards.gen_52_shuffled_cards()
    remainingPlayers = players
    # Trekker kort til alle spillerene
    for p in players:
        p.cards = DrawCards(2)
    # Forste runde med vedding
    print("starting pre-flop betting")
    InitialBet()
    # Trekker flop-kort
    tableCards = DrawCards(3)
    # Ny runde med vedding
    print("starting flop betting")
    FlopBet()
    # Trekker turn-kort
    turn = DrawCards(1)
    tableCards.append(turn[0])
    # Ny runde med vedding
    print("starting turn betting")
    TurnBet()
    # Trekker river-kort
    river = DrawCards(1)
    tableCards.append(river[0])
    # Siste runde med vedding
    print("starting river betting")
    RiverBet()
    # Showdown
    players.rotate(1)


def InitialBet():
    # Starter med at smallBlind og bigBlind m? vedde
    global remainingPlayers
    smallBlind.Raise(raiseValue)
    bigBlind.Call()
    bigBlind.Raise(raiseValue)
    # Hver spiller m? s? ta fold, call eller raise
    # Det er her helt tilfeldig hva de gj?r
    firstRound = True # Brukes for aa soerge for at smallBlind og bigBlind ikke vedder 2 ganger den foerste runden
    stillBetting = True # brukes for Ã¥ se om man er ferdig med Ã¥ vedde eller ikke
    while len(remainingPlayers) > 1 and stillBetting  :
        RemoveFolds()
        for p in remainingPlayers:
            if (p != smallBlind or not firstRound) and (p != bigBlind or not firstRound):
                i = random.randint(0,2)
                if i == 0:
                    p.Fold()
                elif i == 1:
                    p.Raise(raiseValue)
                else:
                    p.Call()
        if firstRound:
            firstRound = False

        stillBetting = PlayersStillbetting()

def FlopBet():
    # Her velger man handling basert p? power rating
    # Har man power rating p? under 3 velger man Fold
    # Har man power rating mellom 3 og 4 velger man Call
    # Har man power rating p? over 4 velger man Raise
    stillBetting = True # brukes for Ã¥ se om man er ferdig med Ã¥ vedde eller ikke
    while len(remainingPlayers) > 1 and stillBetting  :
        RemoveFolds()
        for p in remainingPlayers:
            hand = [p.cards[0] , p.cards[1]]
            for card in tableCards:
                hand.append(card)
            p.cards = hand
            power = cards.calc_cards_power(hand)[0]
            print("spiller",p.name,"har håndstyrke",power)
            if power > 4 and p.bet < 2*raiseValue:
             p.Raise(raiseValue)
            elif power > 2 or currentBet == p.bet:
                p.Call()
            else:
                print("currentbet",currentBet,"vs", p.bet)
                p.Fold()


def TurnBet():
    #Her velger man handling basert pÃƒÂ¥ powerrating akkurat som etter flop
    stillBetting = True # brukes for Ã¥ se om man er ferdig med Ã¥ vedde eller ikke
    while len(remainingPlayers) > 1 and stillBetting  :
        RemoveFolds()
        for p in remainingPlayers:
            hand = [p.cards[0] , p.cards[1]]
            for card in tableCards:
                hand.append(card)
            p.cards = hand
            power = cards.calc_cards_power(hand)[0]
            print("spiller",p.name,"har håndstyrke",power)
            if power > 4 and p.bet < 2*raiseValue:
                p.Raise(raiseValue)
            elif power > 2 or currentBet == p.bet:
                p.Call()
            else:
                print("currentbet",currentBet,"vs", p.bet)
                p.Fold()

def RiverBet():
        #Her velger man handling basert pÃƒÂ¥ powerrating akkurat som etter flop
    stillBetting = True # brukes for Ã¥ se om man er ferdig med Ã¥ vedde eller ikke
    while len(remainingPlayers) > 1 and stillBetting  :
        RemoveFolds()
        for p in remainingPlayers:
            hand = [p.cards[0] , p.cards[1]]
            for card in tableCards:
                hand.append(card)
            p.cards = hand
            power = cards.calc_cards_power(hand)[0]
            print("spiller",p.name,"har håndstyrke",power)
            if power > 4 and p.bet < 2*raiseValue:
                p.Raise(raiseValue)
            elif power > 2 or currentBet == p.bet:
                p.Call()
            else:
                print("currentbet",currentBet,"vs", p.bet)
                p.Fold()


def Showdown():
    best = 0
    i = 1
    handType = None
    for p in remainingPlayers:
        temp = cards.calc_cards_power(p.cards)[0]
        if temp >= best:
            best = temp
            handType = cards.calc_cards_power(p.cards)
        else:
            p.playing = False
        RemoveFolds()
        best = 0
    while(i >= len(handType) and remainingPlayers > 1):
        for p in remainingPlayers:
            temp = cards.calc_cards_power(p.cards)[i]
            if temp >= best:
                best = temp
                handType = cards.calc_cards_power(p.cards)
            else:
                p.playing = False

        RemoveFolds()
        best = 0
        ++i

    print ("player",remainingPlayers, "wins!")
    prize = pot/len(remainingPlayers)
    for p in remainingPlayers:
        p.cash += prize




def DrawCards(n):
    global deck
    c = []
    for i in range(n):
        c.append(deck.pop())
    return c

def RemoveFolds():
    global remainingPlayers
    temp = deque(remainingPlayers)
    for p in remainingPlayers:
        if not p.playing:
            temp.remove(p)
    remainingPlayers = temp

def PlayersStillbetting():
    for p in remainingPlayers:
        if(p.bet < currentBet):
            return True
    return False




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
        self.playing = True

    def Fold(self):
        #Kaster spilleren ut av remainingPlayers
        self.playing = False
        print("player ", self.name, " has folded", "with the hand", self.cards)


    def Raise(self, b):
        #?ker potten og minker cash med bet. Setter ogs? currentBet lik bet
        global currentBet, pot
        #setter temp til verdien som spilleren m? legge til for ? raise med b
        temp = b + (currentBet - self.bet)
        print("----------------")
        print("skal raise med",b,". currentBet er",currentBet, "self.bet er",self.bet)
        print("temp blir da",temp)
        print("------------")
        self.bet+=temp
        self.cash-=temp
        currentBet = temp
        pot += b
        print("player " , self.name, " has raised by ", b, "with the hand", self.cards)

    def Call(self):
        #?ker bet med s? mye som trengs for at bet skal bli lik currentBet
        global currentBet, pot
        self.cash -= currentBet - self.bet
        pot += currentBet - self.bet
        self.bet = currentBet
        print("player", self.name , "has called", "with the hand", self.cards)






    #Finner ut om spilleren skal Raise, Calle eller Folde
    def Assess():
        pass



if __name__ == '__main__':
    main(10)
