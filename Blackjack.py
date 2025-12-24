import math
import random

VALUE_DICT = {
    '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':1
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

def HandValue(hand)
    

def PlayHand(shoe, bankroll):
    '''Plays a Hand. Note that the '''
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
        stood = False

        playerAction = input()
        while(True):
            if (playerAction == 'H'):
                playerHand.append(shoe.pop())

                break
            elif (playerAction == 'S'):
                stood = True
                break

        if(stood):
            break

