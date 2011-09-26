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
from collections import deque
import hand_strength

bigBlind = None
smallBlind= None
currentPlayer = None
done = False #boolean som sier om runden er over eller ikke
pot = 0
players = deque()
remainingPlayers = []
tableCards = []
currentBet = 0
deck = []
startingCash = 0
raiseValue = 100 # Verdien det skal okes med nar man raiser
estimatorTable = []
raisesThisRound = 0
numberOfBettingRounds = 0
firstRound = True
preFlopTable = None



def main(pNumber,rounds):
    #print "starting new game with " , pNumber , " players"
    global blindNumber, startingCash, estimatorTable,preFlopTable

    preFlopTable = hand_strength.getPreFlopTable()
    blindNumber = 0
    startingCash = 10000
    GeneratePlayers(pNumber) #lager spillere
    currentRound = 0
    for i in range(rounds):
        print currentRound
        NewRound()
        currentRound += 1
    PrintMoney()

    #print(estimatorTable)


def GeneratePlayers(n):
    global estimatorTable
    #print ("generating" , n , "players")
    personalities = ["conservative", "bluffer", "persistent"]
    types = ["phase3","phase3","phase3","phase2","phase2"]
    counter = 0
    typeCounter = 0
    for i in range(n):
        if(counter >= len(personalities)):
            counter = 0

        if(typeCounter >= len(types)):
            typeCounter = 0

        players.append(Player(i,personalities[counter],types[typeCounter]))
        #legger til en liste i estimatorTable for hver person
        estimatorTable.append([])
        #print("Spawned player",i,"with personality",players[i].personality)
        counter += 1
        typeCounter += 1


def NewRound():
    # Henter en ny kortstokk og starter en ny runde
    #velger ny big blind og small blind
    global bigBlind,smallBlind,players,remainingPlayers, deck, tableCards,pot,done

    pot = 0
    done = False
    bigBlind = players[1]
    smallBlind = players[0]
    deck = cards.gen_52_shuffled_cards()
    remainingPlayers = deque(players)
    # Trekker kort til alle spillerene
    for p in players:
        p.playing = True
        p.cards = DrawCards(2)
    # Forste runde med vedding
    InitialBet()
    if(not done):
        # Trekker flop-kort
       tableCards = DrawCards(3)
       #print "TABLE CARDS: ", tableCards
       # Ny runde med vedding
       FlopBet()
       if(not done):
            # Trekker turn-kort
            flop = DrawCards(1)
            tableCards.append(flop[0])
            #print "TABLE CARDS: ", tableCards
            # Ny runde med vedding
            TurnBet()
            # Trekker river-kort
            river = DrawCards(1)
            tableCards.append(river[0])
            #print "TABLE CARDS: ", tableCards
            # Siste runde med vedding
            RiverBet()
            if(not done):
                # Showdown
                Showdown()
                players.rotate(1)


def InitialBet():
    #f?rst renkser resetter vi alle bids
    ClearBets()

    # Starter med at smallBlind og bigBlind m? vedde
    print "START INITIAL BET"
    global remainingPlayers, firstRound, numberOfBettingRounds,deck
    #print "small blind"
    smallBlind.Raise(raiseValue * 0.5)
    #print "big blind"

    bigBlind.Raise(raiseValue * 0.5)
    # Hver spiller m? s? ta fold, call eller raise
    # Det er her helt tilfeldig hva de gj?r
    firstRound = True # Brukes for aa soerge for at smallBlind og bigBlind ikke vedder 2 ganger den foerste runden
    numberOfBettingRounds = 0
    deck = cards.gen_52_shuffled_cards()

    while remainingPlayers and numberOfBettingRounds < 4:
        RemoveFolds()
        for p in remainingPlayers:
            if(not done):
                p.Assess()

        numberOfBettingRounds += 1
        if firstRound:
            firstRound = False
    #print "END INITIAL BET"
    ResetHandStrenghts()

def FlopBet():
    # Her velger man handling basert p? power rating
    # Har man power rating p? under 2 velger man Fold
    # Har man power rating mellom 2 og 3velger man Call
    # Har man power rating p? over 3 velger man Raise
    #f?rst renkser resetter vi alle bids
    ClearBets()

    #print("START FLOP BET")
    numberOfBettingRounds = 0
    global tableCards, remainingPlayers, pot, currentBet
    #print("The pot is currently at",pot)
    RemoveFolds()
    while remainingPlayers and numberOfBettingRounds < 4:
        RemoveFolds()
        for p in remainingPlayers:
            p.Assess()
        numberOfBettingRounds += 1
    #print("END FLOP BET")
    ResetHandStrenghts()

def TurnBet():
    #Her velger man handling basert p powerrating akkurat som etter flop
    #f?rst renkser resetter vi alle bids
    ClearBets()

    print("START TURN BET")
    global tableCards, remainingPlayers, numberOfBettingRounds
    numberOfBettingRounds = 0
    RemoveFolds()
    while remainingPlayers and numberOfBettingRounds < 4:
        RemoveFolds()

        for p in remainingPlayers:
            p.Assess()

        numberOfBettingRounds += 1
    #print("END TURN BET")
    ResetHandStrenghts()

def RiverBet():
    #Her velger man handling basert p powerrating akkurat som etter flop
    #f?rst renkser resetter vi alle bids
    ClearBets()

    print("START RIVER BET")
    numberOfBettingRounds = 0
    global tableCards, remainingPlayers
    RemoveFolds()
    while remainingPlayers and numberOfBettingRounds < 5:
        RemoveFolds()
        for p in remainingPlayers:

            p.Assess()
        numberOfBettingRounds += 1
    RemoveFolds()
    #print "END RIVER BET"
    ResetHandStrenghts()

def Showdown():
    global remainingPlayers
    global tableCards, estimatorTable
    print("SHOWDOWN!")
    #print("Remaining players:", len(remainingPlayers))
    winners = []
    for a in remainingPlayers:
        estimatorTable[a.name].append(a.contextTable)

    if len(remainingPlayers) > 0:
        currentWinner = remainingPlayers[0]
        hand = currentWinner.cards
        winningHand = cards.calc_cards_power(currentWinner.cards)
        winners.append(remainingPlayers[0])
        #print "Player:", currentWinner.name, winningHand, "     ", currentWinner.cards

    for i in range(1,len(remainingPlayers)):
        hand2 = remainingPlayers[i].cards

        power2 = cards.calc_cards_power(hand2)
        #print "Player:", remainingPlayers[i].name, power2, "        ", remainingPlayers[i].cards
        for j in range(len(power2)):
            if power2[j] > winningHand[j]:
                currentWinner = remainingPlayers[i]
                winningHand = cards.calc_cards_power(remainingPlayers[i].cards)
                winners = [currentWinner]
                break
            elif power2[j] < winningHand[j]:
                break;
            elif j == len(power2):
                winners.append(remainingPlayers[i])
    print "Winner(s) after showdown!:"
    for p in winners:
        print p.name, cards.calc_cards_power(p.cards), "(prize",pot/len(winners),")", "personality:(",p.personality,")","type:(",p.type,")"
        p.cash += pot/len(winners)

def ResetHandStrenghts():
    for p in players:
        p.handStrength = 0

def PrintMoney():
    asd = 0
    for p in players:
        print "player",p.name,"(",p.personality,")","(",p.type,")","has",p.cash,"left"
        asd += p.cash
    #print "check",  (asd/(len(players)))

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
    remainingPlayers = deque(temp)

def CheckIfFinished():
    global remainingPlayers, pot,done
    actualRemainingPlayers = []
    for p in remainingPlayers:
        if p.playing: actualRemainingPlayers.append(p)
    if len(actualRemainingPlayers) == 1:
        #print("THE WINNER IS: " + str(actualRemainingPlayers[0].name) + "(prize" + str(pot) + ")")
        actualRemainingPlayers[0].cash += pot
        done = True


#metode som resetter alle bets til 0 f?r vi starter en ny runde
def ClearBets():
    global remainingPlayers,currentBet
    for p in remainingPlayers:
        p.bet = 0
    currentBet = 0


def GenerateTableInfo(player, action):
    table = []
    table.append(GenerateContext(player))
    table.append(action)
    table.append([player.cards[0], player.cards[1]])
    table.append(tableCards)
    table.append(CalculateHandStrength(player))
    return table

def CalculateHandStrength(player):
    #print player.cards
    return hand_strength.calculateHandStrength(player.cards, len(remainingPlayers) -1, tableCards)
    #return 0

def GenerateContext(player):
    i = 0
    #decides which round we are in
    if(len(tableCards) == 3):
        i += 100
    elif(len(tableCards) == 4):
        i += 200
    elif(len(tableCards) == 5):
        i += 300
    i += len(remainingPlayers)*10
    if(player.bet > raiseValue *50):
        i+= 9
    elif(player.bet > raiseValue * 30):
        i +=8
    elif(player.bet > raiseValue * 20):
        i += 7
    elif(player.bet > raiseValue * 10):
        i += 6
    elif(player.bet > raiseValue * 8):
        i += 5
    elif(player.bet > raiseValue * 6):
        i+= 4
    elif(player.bet > raiseValue * 4):
        i+=3
    elif(player.bet > raiseValue * 3):
        i+=2
    elif(player.bet > raiseValue ):
        i+= 1
    return i




class Player:
    cards = []
    cash = 0
    bet = 0
    name = 0
    playing = True
    personality = None
    type = None
    lastAction = None
     #The format for the table is as follows: Context, Action, Hole cards shared cards, hand strength
    contextTable = []
    handStrength = 0

    def __init__(self,n, personality, type):
        self.cards = []
        self.cash = startingCash
        self.bet = 0
        self.name= n
        self.personality = personality
        self.contextTable = []
        self.type = type


    def Fold(self):
        #Kaster spilleren ut av remainingPlayers
        self.playing = False
        #print "player ", self.name, " has folded"
        self.contextTable = []
        CheckIfFinished()


    def Raise(self, b):
        #?ker potten og minker cash med bet. Setter ogs? currentBet lik bet
        global currentBet, pot
        #setter temp til verdien som spilleren m? legge til for ? raise med b
        temp = b + (currentBet - self.bet)
        self.bet= currentBet + b
        #self.bet+=temp
        self.cash-=temp
        currentBet += b
        pot += temp
        #print "player " , self.name,"type:",self.type, "has raised by ", b
        #print"the current bet is now at", currentBet,"and the pot is now at",pot
        self.contextTable.append(GenerateTableInfo(self,"raise"))
        self.lastAction = "raise"

    def Call(self):
        #?ker bet med s? mye som trengs for at bet skal bli lik currentBet
        global currentBet, pot
        self.cash -= (currentBet - self.bet)
        pot += (currentBet - self.bet)
        self.bet = currentBet
        #print "player", self.name ,"type:",self.type, "has called"
        #print "the current pot is now at",pot
        self.contextTable.append(GenerateTableInfo(self,"call"))
        self.lastAction = "call"

    #Finner ut om spilleren skal Raise, Calle eller Folde
    def Assess(self):

        if(self.type == "phase1"):

            if(len(tableCards) == 0):
                pass
            else:


                if (self != smallBlind or not firstRound) and (self != bigBlind or not firstRound):
                        i = random.randint(0,2)
                        if i == 0:
                            self.Fold()

                        elif i == 1:
                            self.Raise(raiseValue)

                        else:
                            self.Call()

                else:
                    cashmult = 1
                    powertol = 1
                    if(self.personality == "conservative"):
                        cashmult = 2
                        powertol = 2
                    elif(self.personality == "bluffer"):
                        cashmult = 4
                        powertol = 0
                    elif(self.personality == "persistent"):
                        cashmult = 99
                        powertol = 2

                    if(not done):
                        temp = []
                        temp.append(self.cards[0])
                        temp.append(self.cards[1])
                        for card in tableCards:
                            temp.append(card)
                        hand = list(temp)
                        #self.cards = list(hand)
                        power = cards.calc_cards_power(hand)[0]
                        if power > powertol and self.bet < cashmult*raiseValue:
                            self.Raise(raiseValue)
                        elif power > ((powertol/2) and self.bet < (cashmult/2)*raiseValue) or self.bet == currentBet:
                            self.Call()
                        else:
                            self.Fold()


        elif(self.type == "phase2"):

            if len(tableCards) == 0:
                high = None
                low = None
                suit = None
                if self.cards[0][0] > self.cards[1][0]:
                    high = self.cards[0][0]
                    low = self.cards[1][0]
                else:
                    high = self.cards[1][0]
                    low = self.cards[0][0]

                if self.cards[0][1] == self.cards[1][1]:
                    suit = 1
                else:
                    suit = 0
                if(self.handStrength == 0):
                    self.handStrength = preFlopTable[high -2][low -2][suit][len(players) -2] *2

            else:
                if(self.handStrength == 0):
                    self.handStrength = CalculateHandStrength(self)
            #raiser med bra kort, men raiser ikke med for mye
            if self.personality == "conservative":
                if(self.handStrength > 0.6):
                    if self.bet < raiseValue * 2:
                        self.Raise(raiseValue)
                    else:
                        self.Call()
                elif((self.handStrength >0.45 and self.bet < raiseValue * 2) or self.bet == currentBet):
                    self.Call()
                else:
                    self.Fold()

            elif self.personality == "bluffer":
                    if(self.handStrength > 0.5):
                        if self.bet < raiseValue * 10:
                            self.Raise(raiseValue)
                        else:
                            self.Call()
                    elif(self.handStrength > (1/len(remainingPlayers)) or self.bet == currentBet):
                        self.Call()
                    else:
                        self.Fold()

            elif self.personality == "persistent":
                    if(self.handStrength > 0.6):
                        if self.bet < raiseValue * 20:
                            self.Raise(raiseValue)
                        else:
                            self.Call()
                    elif(self.handStrength >(1/len(remainingPlayers)) or self.bet == currentBet):
                        self.Call()
                    else:
                        self.Fold()


        elif(self.type == "phase3"):

            if(len(tableCards) == 0):
                high = None
                low = None
                suit = None
                if self.cards[0][0] > self.cards[1][0]:
                    high = self.cards[0][0]
                    low = self.cards[1][0]
                else:
                    high = self.cards[1][0]
                    low = self.cards[0][0]

                if self.cards[0][1] == self.cards[1][1]:
                    suit = 1
                else:
                    suit = 0
                if(self.handStrength == 0):
                    self.handStrength = preFlopTable[high -2][low -2][suit][len(players) -2] * 2

            else:
                if(self.handStrength == 0):
                    self.handStrength = CalculateHandStrength(self)
                #ownStrength = hand_strength.calculateHandStrength([self.cards[0],self.cards[1]], len(remainingPlayers) -1, tableCards)
            guess = self.GuessHand()

            shouldRaise = False
            shouldCall = True
            shouldFold = False
            if self.personality == "conservative":
                    for g in guess:
                        if g > self.handStrength:
                            shouldFold = True
                            shouldRaise = False
                            break
                        elif self.handStrength-0.1 > g:
                            Raise = True
                    if(shouldRaise):
                        if(self.bet < raiseValue * 3):
                            self.Raise(raiseValue)
                        else:
                            self.Call()
                    elif(shouldCall or self.bet == currentBet):
                        self.Call()
                    elif(shouldFold):
                        self.Fold()

            elif self.personality == "persistent":
                    counter = 0
                    for g in guess:
                        if g > self.handStrength:
                            counter += 1
                    if(counter > len(remainingPlayers)/3):
                        shouldFold = True
                        shouldCall = False
                    elif counter == 0:
                        shouldRaise = True
                        shouldCall = False

                    if(shouldRaise):
                        if(self.bet < 20*raiseValue):
                            self.Raise(raiseValue)
                        else:
                            self.Call()
                    elif (shouldCall or self.bet == currentBet):
                        self.call
                    else:
                        self.Fold()

            elif self.personality == "bluffer":
                    counter = 0
                    for g in guess:
                        if g -0.1> self.handStrength:
                            counter += 1
                    if(counter > len(remainingPlayers)/2):
                        shouldFold = True
                        shouldCall = False
                    elif counter < 2:
                        shouldRaise = True
                        shouldCall = False

                    if(shouldRaise):
                        if(self.bet < 10*raiseValue):
                            self.Raise(raiseValue)
                        else:
                            self.Call()
                    elif (shouldCall or self.bet == currentBet):
                        self.Call()
                    else:
                        self.Fold()













    def GuessHand(self):
        guesses = []
        for p in remainingPlayers:
            if ( not p == self):
                temptable = estimatorTable[p.name]
                currentContext = GenerateContext(p)
                table = []
                strength = 0
                for e in temptable:
                    if(e[0] == currentContext):
                        if(e[1] == p.lastAction):
                            table.append(e)
                for ex in table:
                    strength += ex[4]
                if(len(table) > 0):
                    strength = strength/len(table)
                guesses.append(strength)
        return guesses









if __name__ == '__main__':
    main(5,1000)
