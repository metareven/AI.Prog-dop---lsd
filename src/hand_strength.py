import cards
import itertools

def calculateHandStrength(hand, numberOfOpponents, tableCards):
    playerHand = hand[:]
    table = tableCards[:]
    numberOfWins = 0
    numberOfTies = 0
    numberOfLosses = 0
    remainingCards = cards.gen_52_cards()
    for c in hand:
        remainingCards.remove(c)
    for c in tableCards:
        remainingCards.remove(c)
    remainingHoleCombinations = list(itertools.combinations(remainingCards
    for  in numberOfSimulations:
        remainingCards = cards.gen_52_shuffled_cards()
        for c in playerHand: 
            remainingCards.remove(c)
        for c in table: 
            remainingCards.remove(c)
        opponents = []
        for foo in numberOfOpponents:
            o = []
            o.append(remainingCards.pop())
            o.append(remainingCards.pop())
            opponents.append(o)
        outcome = calculateOutcome(playerHand, table, opponents)
        if outcome == 1:
            numberOfWins += 1
        elif outcome == 0:
            numberOfTies += 1
        else:
            numberOfLosses += 1
    base_strength = float(float(float(numberOfWins) + float(float(numberOfTies)/float(2))) / float(numberOfSimulations))
    hand_strength = float(1)
    for i in range(numberOfOpponents):
        hand_strength = hand_strength * base_strength
    return hand_strength
    
        
        


def calculateOutcome(player, tableCards, opponents):
    winners = []
    currentWinner = player
    hand = player[:]
    for c in tableCards:
        hand.append(c)
    winningHand = cards.calc_cards_power(hand)
    winners.append(hand)
    for o in opponents:
        ny_hand = o[:]
        for c in tableCards:
            ny_hand.append(c)
        power = cards.calc_cards_power(ny_hand)
        for i in range(len(power)):
            if power[i] > winningHand[i]:
                currentWinner = ny_hand
                winningHand = power
                winners = [currentWinner]
                break
            elif power[i] < winningHand[i]:
                break
            elif i == len(power):
                winners.append(ny_hand)
    if not hand in winners:
        return -1
    elif len(winners) == 1:
        return 1
    else:
        return 0
    
