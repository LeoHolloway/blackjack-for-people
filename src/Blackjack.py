import math
import random


#TODO:Consider json for settings/rules
#Global bankroll might go in main
limit = 21

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
    
def PlayerSequence(shoe, bankroll, dealerHand, playerHand, bet, allPlayerHands, isInitialDeal):
    '''Recursively callable. DOES NOT play dealer's hand; it only gets the object passed so it can show it to you.
    Hand values will be recorded in the mutable list allPlayerHands of tuples formatted (score, wager, isNaturalBlackjack); no return. Bankroll is also mutable.'''
    #TODO: move player sequence to this function. 
    if isInitialDeal and HandValue(playerHand) == 21:
        return(21, bet, True)
    while(True):
        print("Dealer Hand:")
        print(dealerHand)
        print("Player Hand:")
        print(playerHand)
        print("H for hit, S for stand, D for double down, P for split")
        playerAction = input()
        if (playerAction == 'H'):
            playerHand.append(shoe.pop())
            if HandValue(playerHand) > limit:
                print("You busted. You lost this hand.")
                break
        elif (playerAction == 'S'):
            break
        elif (playerAction == 'D'):
            if bankroll < bet:
                print("Not enough money to double down. Try a different action.")
                continue
            playerHand.append(shoe.pop())
            bankroll -= bet
            bet *= 2
            break
        elif (playerAction == 'P'):
            if len(playerHand) != 2 or playerHand[0][0] != playerHand[1][0] or bankroll < bet:
                print("Cannot split. Try a different action.")
                continue
            bankroll -= bet
            secondHand = playerHand.pop() #split hand
            secondHand.append(shoe.pop()) #draw 1 card each
            playerHand.append(shoe.pop())
            PlayerSequence(shoe, bankroll, dealerHand, secondHand, bet, allPlayerHands, False) # no need to assign ret value to a list because it will just add it to the list you first passed. Plays sequence of one card.
            continue #plays sequence of first card.
    valToUpdate = HandValue(playerHand)
    if valToUpdate > limit:
        valToUpdate = -1
    allPlayerHands.append((valToUpdate, bet, False))
        
def DealerSequence(shoe, dealerHand):
    '''Dealer draws until he gets standNumber, which will be in a json later, or busts. if hitOnSoft, then he will hit on a soft 17. Returns (handValue, dealerNaturalBlackjack), where handValue = 0 if busts. '''
    standNumber = 17
    limit = 21
    hitOnSoft = True
    dealerHand.append(shoe.pop())
    if HandValue(dealerHand) == 21:
        return (21, True)
    handContainsAce = False
    for card in dealerHand:
        if card[0] == 'A':
            handContainsAce = True
    dealerBusted = False
    while(True):
        print("Dealer Hand:")
        print(dealerHand)
        currVal = HandValue(dealerHand)
        if currVal > limit:
            return 0
        if currVal < standNumber or (currVal == standNumber and (handContainsAce and hitOnSoft)): #Should dealer hit?
            dealerHand.append(shoe.pop())
        else:
            break
    return (currVal, False)

        

def PlayHand(shoe, bankroll):
    '''Plays a Hand'''
    #TODO: solve shoe running out
    dealerHand = []
    playerHand = []
    bet = 0
    while(bet == 0):
        print("Current bankroll is " + str(bankroll) + ".")
        print("Bet?")
        betResponse = int(input())
        if(betResponse < bankroll and betResponse > 0 and betResponse % 1 == 0):
            bet = betResponse
            bankroll -= bet
        else:
            print("Invalid bet")
            continue
    print("Bet was " + str(bet) + ", bankroll is now " + str(bankroll))
    dealerHand.append(shoe.pop())
    for i in range(2):
        playerHand.append(shoe.pop())
    allPlayerHands = []
    PlayerSequence(shoe, bankroll, dealerHand, playerHand, bet, allPlayerHands, True)
    dealerVal = DealerSequence(shoe, dealerHand)

    moneyWonThisHand = 0
    amountBet = 0
    for handVal in allPlayerHands: #handVal has format(value, bet, natural). Dealer has format (value, natural)
        if handVal[2] and not dealerVal[1]: #case of player natural blackjack
            print("You won a hand by natural blackjack with a wager of " + str(handVal[1]) + ". Payout is 3 to 2.")
            moneyWonThisHand += handVal[1] * 3 / 2.0
            bankroll += handVal[1] * 5 / 2.0
        elif handVal[0] > dealerVal[0]: #Player wins normally, also handles cases where player busts on a hand before dealer busts, since dealerVal == 0 and handVal[0] == -1 itc
            print("You won a hand with a wager of " + str(handVal[1]) + ".")
            moneyWonThisHand += handVal[1] 
            bankroll += handVal[1] * 2
        elif handVal[0] == dealerVal[0]:
            print("You pushed a hand with a wager of " + str(handVal[1]) + ".")
            bankroll += handVal[1]
        else: #loss
            print("You lost a hand with a wager of " + str(handVal[1]) + ".")
            moneyWonThisHand -= handVal[1]
        amountBet += handVal[1]

    print("You bet " + str(amountBet) + ".")
    if moneyWonThisHand > 0:
        print("You won " + str(moneyWonThisHand) + " this round.")
    elif moneyWonThisHand < 0:
        print("You lost " + str(-moneyWonThisHand) + " this round.")
    else:
        print("You broke even this round.")
        
myShoe = MakeShoe(1)
myBankroll = 100
PlayHand(myShoe, myBankroll)
