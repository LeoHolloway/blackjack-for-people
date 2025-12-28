import math
import random


#Consider json for settings/rules
#Consider global bankroll

VALUE_DICT = {
    '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11
}

#blackjack
def MakeDeck():
    """Generates a deck of 52 cards.
    The deck of cards is a list of (rank, suit) tuples that will be sorted by suit, then rank.
    Helper function.
    """
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck

def MakeShoe(deckNum):
    '''Creates shoe with deckNum decks'''
    deck = MakeDeck()
    bigDeck = deck * deckNum
    random.shuffle(bigDeck)
    return bigDeck

def HandValue(hand):
    '''hand is a list of tuples. Ace default val is 11; if your hand contains aces and > 21, it converts aces to 1s until it's a good hand or you run out of aces.'''
    value = 0
    aces = 0
    for card in hand:
        if card[0] == 'A':
            value += VALUE_DICT[card[0]]
            aces += 1
        else:
            value += VALUE_DICT[card[0]]
    if value > 21:
        while(aces > 0):
            value -= 10
            if value <= 21:
                break
    return value
    
def PlayerHand(shoe, bankroll, xx):
    #TODO: move player sequence to this function. should be able to 

def PlayHand(shoe, bankroll):
    '''Plays a Hand'''
    #TODO: solve shoe running out
    dealerHand = []
    playerHand = []
    playerTotal = 0
    dealerTotal = 0
    bet = 0
    while(bet == 0):
        print("Current bankroll is" + bankroll + ".")
        print("Bet?")
        betResponse = input()
        if(betResponse < bankroll and betResponse > 0 and betResponse % 1 == 0):
            bet = betResponse
            bankroll = bankroll - betResponse
            
    print("Bet was" + bet + ", bankroll is now" + bankroll)
    dealerHand.append(shoe.pop())
    for i in range(2):
        playerHand.append(shoe.pop())
    
    #Player sequence
    while(True):
        print("Dealer Hand:")
        print(dealerHand)
        print("Player Hand:")
        print(playerHand)
        print("H for hit, S for stand, D for double down, P for split")
        turnOver = False
        busted = False
        playerAction = input()
        
        while(True):
            if (playerAction == 'H'):
                playerHand.append(shoe.pop())
                if HandValue(playerHand) > 21:
                    turnOver = True
                    busted = True
                break
            elif (playerAction == 'S'):
                turnOver = True
                break
            elif (playerAction == 'D'):
                if bankroll < bet:
                    print("Not enough money to double down. Try a different action.")
                    continue
                playerHand.append(shoe.pop())
                turnOver = True
                if HandValue(playerHand) > 21:
                    busted = True
            elif (playerAction == 'P'):
                #TODO: code split. This will work by recursively calling the PlayerHand function with this shoe object etc. Will need to have a list of hand outcomes.

        if(turnOver):
            break

MakeShoe(1)
