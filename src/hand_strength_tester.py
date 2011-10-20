import hand_strength
import cards

def main():
    # Denne testen bruker de samme kortene som i foilen om Hand Strength Development i poker_slides.pdf
    hand1 = [[14, 'D'], [14, 'H']]
    hand2 = [[4, 'S'], [5, 'S']]
    hand3 = [[4, 'H'], [5, 'H']]
    hand4 = [[14, 'D'], [3, 'H']]
    hand5 = [[4, 'D'], [9, 'D']]
    tableCards1 = [[14, 'S'], [2, 'S'], [3, 'S']]
    tableCards2 = list(tableCards1)
    tableCards2.append([14, 'C'])
    print("Table cards: " + str(tableCards1))
    print(str(hand1) + " : " + str(hand_strength.calculateHandStrength(hand1, 1, tableCards1)))
    print(str(hand2) + "   : " + str(hand_strength.calculateHandStrength(hand2, 1, tableCards1)))
    print(str(hand3) + "   : " + str(hand_strength.calculateHandStrength(hand3, 1, tableCards1)))
    print(str(hand4) + "  : " + str(hand_strength.calculateHandStrength(hand4, 1, tableCards1)))
    print(str(hand5) + "   : " + str(hand_strength.calculateHandStrength(hand5, 1, tableCards1)))
    print("Table cards: " + str(tableCards2))
    print(str(hand1) + " : " + str(hand_strength.calculateHandStrength(hand1, 1, tableCards2)))
    print(str(hand2) + "   : " + str(hand_strength.calculateHandStrength(hand2, 1, tableCards2)))
    print(str(hand3) + "   : " + str(hand_strength.calculateHandStrength(hand3, 1, tableCards2)))
    print(str(hand4) + "  : " + str(hand_strength.calculateHandStrength(hand4, 1, tableCards2)))
    print(str(hand5) + "   : " + str(hand_strength.calculateHandStrength(hand5, 1, tableCards2)))
    

if __name__ == "__main__":
    main()
