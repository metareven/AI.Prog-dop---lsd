import cards
import itertools
from sys import stdout
import datetime

def main():
    start = datetime.datetime.now()
    stdout.write("Start time: ")
    stdout.write(str(start)+'\n')
    kortstokk = cards.gen_52_cards()     # Ny kortstokk
    pre_flop_table = makePreFlopTable()  # Her lages pre-flop tabellen der sansynlighetene for aa vinne skal legges inn
    allHoleCombinations = list(itertools.combinations(kortstokk, 2)) # Liste med alle mulige hullkombinasjoner
    #allHoleCombinations = [([14,'D'], [14,'H']), ([2,'D'], [3, 'D']), ([2, 'D'], [4, 'S'])]
    calculateProbabilities(allHoleCombinations, pre_flop_table) # Her regner man ut de faktiske sansynlighetene for aa vinne for hver mulige hullkortkombinasjon
    works = True
    for i in range(9):
        for j in range(13):
            for k in range (0, j):
                if pre_flop_table[j][k][0][i] == -1:
                    works = False
                elif pre_flop_table[j][k][1][i] == -1:
                    works = False
    print works
    print pre_flop_table[14-2][14-2][0][8]
    print pre_flop_table[3-2][2-2][1][8]
    print pre_flop_table[4-2][2-2][0][8]
    print pre_flop_table[0][0][0][0]
    makePreFlopFile(pre_flop_table) # Her lages det en fil av tabellen med sansynlighetene
    end = datetime.datetime.now()
    stdout.write("End time: ")
    stdout.write(str(end)+'\n')
    

# Metoden lager en fil som skal representere tabellen den faar inn
# table er en 4-dimensjonal tabell med sansynligheter
def makePreFlopFile(table):
    for i in range(9):
        stdout.write(str(i)+'\n')
        stdout.write('unsuited\n')
        for j in range(1,14):
            for k in range(1, j+1):
                if k == j:
                    stdout.write(str("%.6f" % round(table[j-1][k-1][0][i], 2))+'\n')
                else:
                    stdout.write(str("%.6f" % round(table[j-1][k-1][0][i], 6))+" ")

    for i in range(9):
        stdout.write(str(i)+'\n')
        stdout.write('suited\n')
        for j in range(1,14):
            for k in range(1, j+1):
                if k == j:
                    # stdout.write(str(table[j][k][0][i])+'\n')
                    stdout.write(str("%.6f" % round(table[j-1][k-1][0][i], 2))+'\n')
                else:
                    # stdout.write(str(table[j][k][0][i]) + " ")
                    stdout.write(str("%.6f" % round(table[j-1][k-1][0][i], 6))+" ")


# Her fjerner man player sine kort fra kortstokken, slik at ingen av
# motstanderne kan ha de samme kortene som player
def removeComb(hole, kortstokk):
    for h in hole:
        kortstokk.remove(h)

# Metoden regner ut utfallet av en showdown med hensyn paa player   
# player er hullkortene til spilleren man skal sjekke resultatet til
# tableCards er de 5 kortene paa bordet
# opponents er en liste med motstandere, der hver motstander bestaar av en
# liste med 2 kort
# Returnerer 1 hvis player vinner, 0 hvis player spiller uavgjort og
# -1 hvis player taper.
def calculateOutcome(player, tableCards, opponents):
    winners = []
    currentWinner = player
    hand = player[:]
    for c in tableCards:
        hand.append(c)
    winningHand = cards.calc_cards_power(hand)
    winners.append(player)
    for opponent in opponents:
        ny_hand = opponent
        for c in tableCards:
            ny_hand.append(c)
        power = cards.calc_cards_power(ny_hand)
        for i in range(len(power)):
            if power[i] > winningHand[i]:
                currentWinner = opponent
                winningHand = power
                winners = [currentWinner]
                break
            elif power[i] < winningHand[i]:
                break
            elif i == len(power):
                winners.append(opponent)
    if not player in winners: # Lose
        return -1
    elif len(winners) == 1: # Win
        return 1
    else: # Draw
        return 0
    
# Metoden regner ut sansynligheter for alle mulige komobinasjoner og legger 
# dem til i pre_flop_table. Sansynlighetene regnes ut ved aa gi alle
# motstanderne 2 tilfeldige kort hver og aa legge ut 5 tilfeldige kort paa bordet.
# Dette gjoeres numberOfRollouts ganger ogsaa regner man ut sansynligheten for aa
# vinne basert paa antall seiere, uavgjort og tap.
# Dette gjoeres for 1 til 9 motstandere.
def calculateProbabilities(allHoleCombinations, pre_flop_table):
    for n in range(1, 10): # For 1 til 9 motstandere
        for comb in allHoleCombinations: # For alle kombinasjoner av hullkort
            comb = list(comb)
            sorter(comb)
            classAlreadyCalculated = False
            # Her sjekkes det om det allerede er regnet ut sansynligheten for aa vinne for denne ekvivalensklassen
            if comb[0][1] == comb[1][1]:
                if pre_flop_table[comb[0][0]-2][comb[1][0]-2][1][n-1] != -1:
                    classAlreadyCalculated = True
            elif pre_flop_table[comb[0][0]-2][comb[1][0]-2][0][n-1] != -1:
                    classAlreadyCalculated = True
            if not classAlreadyCalculated:
                numberOfWins = float(0)
                numberOfDraws = float(0)
                numberOfLose = float(0)
                numberOfRollouts = 5000
                for i in range(numberOfRollouts):
                    new_cards = cards.gen_52_shuffled_cards()
                    removeComb(comb, new_cards)
                    opponents = []
                    for foo in range(n):
                        opponent = []
                        opponent.append(new_cards.pop())
                        opponent.append(new_cards.pop())
                        opponents.append(opponent)
                    table = []
                    for bar in range(5):
                        table.append(new_cards.pop())
                    outcome = calculateOutcome(comb, table, opponents)
                    if outcome == -1:
                        numberOfLose += 1
                    elif outcome == 0:
                        numberOfDraws += 1
                    else:
                        numberOfWins += 1
                    temp_strength = (numberOfWins + (numberOfDraws / float(2))) / (numberOfWins + numberOfDraws + numberOfLose)
                    actual_strength = float(1)
                    for i in range(n):
                        actual_strength = actual_strength * temp_strength
                    #print comb
                    #print len(pre_flop_table)
                    #print len(pre_flop_table[14-2])
                    if comb[0][1] != comb[1][1]:
                        pre_flop_table[comb[0][0]-2][comb[1][0]-2][0][n-1] = actual_strength
                    else:
                        pre_flop_table[comb[0][0]-2][comb[1][0]-2][1][n-1] = actual_strength

def sorter(liste):
    #print liste
    if liste[0][0] < liste[1][0]:
        temp = liste[1]
        liste[1] = liste[0]
        liste[0] = temp


def makePreFlopTable():
    pre_flop_table = [] 
    for i in range(1, 14):
        unsuited = [-1] * 9
        suited = [-1] * 9
        new_inner = [[unsuited, suited]] * i
        pre_flop_table.append(new_inner)
    return pre_flop_table


if __name__ == '__main__':
    main()
