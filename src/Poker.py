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
estimatorTable = [[[]]]
raisesThisRound = 0



def main(pNumber,rounds):

    print "starting new game with " , pNumber , " players"
    global blindNumber, startingCash
    blindNumber = 0
    startingCash = 10000
    GeneratePlayers(pNumber) #lager spillere
    for i in range(rounds):
        NewRound()
        PrintMoney()


def GeneratePlayers(n):
    print ("generating" , n , "players")
    types = ["conservative", "bluffer", "persistent"]
    counter = 0
    for i in range(n):
        if(counter >= len(types)):
            counter = 0
        players.append(Player(i,types[counter]))
        #print("Spawned player",i,"with personality",players[i].personality)
        counter += 1


def NewRound():
    # Henter en ny kortstokk og starter en ny runde
    #velger ny big blind og small blind
    global bigBlind,smallBlind,players,remainingPlayers, deck, tableCards,pot,done
    pot = 0
    done = False
    bigBlind = players[1]
    smallBlind = players[0]
    deck = cards.gen_52_shuffled_cards()
    remainingPlayers = players
    # Trekker kort til alle spillerene
    for p in players:
        p.playing = True
        p.cards = DrawCards(2)
    # Forste runde med vedding
    InitialBet()
    if(not done):
        # Trekker flop-kort
       tableCards = DrawCards(3)
       print "TABLE CARDS: ", tableCards
       # Ny runde med vedding
       FlopBet()
       if(not done):
            # Trekker turn-kort
            flop = DrawCards(1)
            tableCards.append(flop[0])
            print "TABLE CARDS: ", tableCards
            # Ny runde med vedding
            TurnBet()
            # Trekker river-kort
            river = DrawCards(1)
            tableCards.append(river[0])
            print "TABLE CARDS: ", tableCards
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
    global remainingPlayers
    print "small blind"
    smallBlind.Raise(raiseValue * 0.5)
    print "big blind"

    bigBlind.Raise(raiseValue * 0.5)
    # Hver spiller m? s? ta fold, call eller raise
    # Det er her helt tilfeldig hva de gj?r
    firstRound = True # Brukes for aa soerge for at smallBlind og bigBlind ikke vedder 2 ganger den foerste runden
    numberOfBettingRounds = 0
    while remainingPlayers and numberOfBettingRounds < 2:
        RemoveFolds()
        for p in remainingPlayers:
            if(not done):
                if (p != smallBlind or not firstRound) and (p != bigBlind or not firstRound):
                    i = random.randint(0,2)
                    if i == 0:
                        p.Fold()

                    elif i == 1:
                        p.Raise(raiseValue)

                    else:
                        p.Call()

        numberOfBettingRounds += 1
        if firstRound:
            firstRound = False
    print "END INITIAL BET"

def FlopBet():
    # Her velger man handling basert p? power rating
    # Har man power rating p? under 2 velger man Fold
    # Har man power rating mellom 2 og 3velger man Call
    # Har man power rating p? over 3 velger man Raise
    #f?rst renkser resetter vi alle bids
    ClearBets()

    print("START FLOP BET")
    numberOfBettingRounds = 0
    global tableCards, remainingPlayers, pot, currentBet
    print("The pot is currently at",pot)
    RemoveFolds()
    while remainingPlayers and numberOfBettingRounds < 1:
        RemoveFolds()
        for p in remainingPlayers:
            cashmult = 1
            powertol = 1
            if(p.personality == "conservative"):
                cashmult = 2
                powertol = 2
            elif(p.personality == "bluffer"):
                cashmult = 4
                powertol = 0
            elif(p.personality == "persistent"):
                cashmult = 99
                powertol = 2


            if(not done):
                hand = p.cards
                for card in tableCards:
                    hand.append(card)
                power = cards.calc_cards_power(hand)[0]
                if power > powertol and p.bet < cashmult*raiseValue:
                    p.Raise(raiseValue)
                elif power > ((powertol/2) and p.bet < (cashmult/2)*raiseValue) or p.bet == currentBet:
                    p.Call()
                else:
                    p.Fold()
        numberOfBettingRounds += 1
    print("END FLOP BET")

def TurnBet():
    #Her velger man handling basert p powerrating akkurat som etter flop
    #f?rst renkser resetter vi alle bids
    ClearBets()

    print("START TURN BET")
    numberOfBettingRounds = 0
    global tableCards, remainingPlayers
    RemoveFolds()
    while remainingPlayers and numberOfBettingRounds < 1:
        RemoveFolds()

        for p in remainingPlayers:

            cashmult = 1
            powertol = 1
            if(p.personality == "conservative"):
                cashmult = 2
                powertol = 2
            elif(p.personality == "bluffer"):
                cashmult = 4
                powertol = 0
            elif(p.personality == "persistent"):
                cashmult = 99
                powertol = 2

            if(not done):
                hand = list([p.cards[0], p.cards[1]])
                for card in tableCards:
                    hand.append(card)
                p.cards = hand
                power = cards.calc_cards_power(hand)[0]
                if power > powertol and p.bet < cashmult*raiseValue:
                    p.Raise(raiseValue)
                elif power > ((powertol/2) and p.bet < (cashmult/2)*raiseValue) or p.bet == currentBet:
                    p.Call()
                else:
                    p.Fold()
        numberOfBettingRounds += 1
    print("END TURN BET")

def RiverBet():
    #Her velger man handling basert p powerrating akkurat som etter flop
    #f?rst renkser resetter vi alle bids
    ClearBets()

    print("START RIVER BET")
    numberOfBettingRounds = 0
    global tableCards, remainingPlayers
    RemoveFolds()
    while remainingPlayers and numberOfBettingRounds < 1:
        RemoveFolds()
        for p in remainingPlayers:

            cashmult = 1
            powertol = 1
            if(p.personality == "conservative"):
                cashmult = 2
                powertol = 2
            elif(p.personality == "bluffer"):
                cashmult = 4
                powertol = 0
            elif(p.personality == "persistent"):
                cashmult = 99
                powertol = 2

            if(not done):
                hand = list([p.cards[0], p.cards[1]])
                for card in tableCards:
                    hand.append(card)
                p.cards = hand
                power = cards.calc_cards_power(hand)[0]
                if power > powertol and p.bet < cashmult*raiseValue:
                    p.Raise(raiseValue)
                elif power > ((powertol/2) and p.bet < (cashmult/2)*raiseValue) or p.bet == currentBet:
                    p.Call()
                else:
                    p.Fold()
        numberOfBettingRounds += 1
    RemoveFolds()
    print "END RIVER BET"

def Showdown():
    global remainingPlayers
    global tableCards
    print("SHOWDOWN!")
    print("Remaining players:", len(remainingPlayers))
    winners = []
    if len(remainingPlayers) > 0:
        currentWinner = remainingPlayers[0]
        hand = currentWinner.cards

        winningHand = cards.calc_cards_power(hand)
        winners.append(remainingPlayers[0])
        print "Player:", currentWinner.name, winningHand, "     ", currentWinner.cards
    for i in range(1,len(remainingPlayers)):
        hand2 = remainingPlayers[i].cards

        power2 = cards.calc_cards_power(hand2)
        print "Player:", remainingPlayers[i].name, power2, "        ", remainingPlayers[i].cards
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
        print p.name, cards.calc_cards_power(p.cards), "(prize",pot/len(winners),")", "personality:(",p.personality,")"
        p.cash += pot/len(winners)


def PrintMoney():
    asd = 0
    for p in players:
        print "player",p.name,"(",p.personality,")","has",p.cash,"left"
        asd += p.cash
    print "check",  (asd/(len(players)))

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
    global remainingPlayers, pot,done
    actualRemainingPlayers = []
    for p in remainingPlayers:
        if p.playing: actualRemainingPlayers.append(p)
    if len(actualRemainingPlayers) == 1:
        print("THE WINNER IS: " + str(actualRemainingPlayers[0].name) + "(prize" + str(pot) + ")")
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
    table.append(list([player.cards[0], player.cards[1]]))
    table.append(tableCards)
    table.append(CalculateHandStrength(player))

    #PLACEHOLDER FOR NOW
def CalculateHandStrength(player):
    hand_strength.calculateHandStrength([player.cards[0],player.cards[1]], len(remainingPlayers) -1, tableCards)

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




class Player:
    cards = []
    cash = 0
    bet = 0
    name = 0
    playing = True
    personality = None
     #The format for the table is as follows: Context, Action, Hole cards shared cards, hand strength
    contextTable = None

    def __init__(self,n, personality):
        self.cards = []
        self.cash = startingCash
        self.bet = 0
        self.name= n
        self.personality = personality
        self.contextTable = []


    def Fold(self):
        #Kaster spilleren ut av remainingPlayers
        self.playing = False
        print "player ", self.name, " has folded"
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
        print "player " , self.name, " has raised by ", b
        print"the current bet is now at", currentBet,"and the pot is now at",pot
        contextTable.append(GenerateTableInfo(self,"raise"))

    def Call(self):
        #?ker bet med s? mye som trengs for at bet skal bli lik currentBet
        global currentBet, pot
        self.cash -= (currentBet - self.bet)
        pot += (currentBet - self.bet)
        self.bet = currentBet
        print "player", self.name , "has called"
        print "the current pot is now at",pot
        contextTable.append(GenerateTableInfo(self,"call"))

    #Finner ut om spilleren skal Raise, Calle eller Folde
    def Assess():
        pass



if __name__ == '__main__':
    main(10,1)
