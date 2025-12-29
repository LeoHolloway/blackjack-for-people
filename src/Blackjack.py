import random

# blackjack
def MakeDeck(settings):
    """Generates a deck of 52 cards."""
    suits = settings["suits"]
    ranks = settings["ranks"]

    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck


def MakeShoe(settings):
    """Creates a shoe with deckNum decks."""
    deck = MakeDeck(settings)
    bigDeck = deck * settings["number_of_decks"]

    random.shuffle(bigDeck)
    return bigDeck


def HandValueAndSoft(hand, settings):
    value = 0
    aces = 0

    for rank, _ in hand:
        value += settings["value_dict"][rank]
        if rank == 'A':
            aces += 1

    limit = settings["limit"]
    soft = False
    while value > limit and aces > 0:
        value -= 10
        aces -= 1

    if aces > 0:
        soft = True

    return value, soft


def PlayerSequence(shoe, bankroll, dealerHand, playerHand, bet, allPlayerHands, isInitialDeal, settings):
    limit = settings["limit"]

    if isInitialDeal and HandValueAndSoft(playerHand, settings)[0] == limit:
        allPlayerHands.append((limit, bet, True))
        return

    while True:
        print("Dealer Hand:")
        print(dealerHand)

        print("Player Hand:")
        print(playerHand)

        print("H for hit, S for stand, D for double down, P for split")
        playerAction = input()

        if playerAction == 'H':
            playerHand.append(shoe.pop())

            if HandValueAndSoft(playerHand, settings)[0] > limit:
                print("You busted. You lost this hand.")
                break

        elif playerAction == 'S':
            break

        elif playerAction == 'D':
            if bankroll < bet:
                print("Not enough money to double down. Try a different action.")
                continue

            playerHand.append(shoe.pop())
            bet *= 2

            print("Player Hand:")
            print(playerHand)
            break

        elif playerAction == 'P':
            if len(playerHand) != 2 or playerHand[0][0] != playerHand[1][0] or bankroll < bet:
                print("Cannot split. Try a different action.")
                continue

            secondHand = [playerHand.pop()]  # split hand
            secondHand.append(shoe.pop())    # draw 1 card each
            playerHand.append(shoe.pop())

            PlayerSequence(shoe, bankroll, dealerHand, secondHand, bet, allPlayerHands, False, settings)
            continue

    valToUpdate = HandValueAndSoft(playerHand, settings)[0]
    if valToUpdate > limit:
        valToUpdate = -1

    allPlayerHands.append((valToUpdate, bet, False))


def DealerSequence(shoe, dealerHand, settings):
    standNumber = settings["dealer_stop"]
    hitOnSoft = settings["dealer_hits_soft"]
    limit = settings["limit"]

    dealerHand.append(shoe.pop())

    currVal, isSoft = HandValueAndSoft(dealerHand, settings)
    if currVal == limit:
        return (limit, True)

    while True:
        print("Dealer Hand:")
        print(dealerHand)

        currVal, isSoft = HandValueAndSoft(dealerHand, settings)

        if currVal > limit:
            return (0, False)

        if currVal < standNumber:
            dealerHand.append(shoe.pop())
        elif currVal == standNumber and isSoft and hitOnSoft:
            dealerHand.append(shoe.pop())
        else:
            break

    return (currVal, False)


def PlayHand(shoe, bankroll, settings):
    blackjack_payout = settings["blackjack_payout"]

    dealerHand = []
    playerHand = []
    bet = 0

    while bet == 0:
        print(f"Current bankroll is {bankroll}.")
        print("Bet?")
        betResponse = int(input())
        if betResponse <= bankroll and betResponse > 0:
            bet = betResponse
        else:
            print("Invalid bet")
            continue

    print(f"Bet was {bet}, bankroll is now {bankroll}")

    dealerHand.append(shoe.pop())

    for i in range(2):
        playerHand.append(shoe.pop())

    allPlayerHands = []
    PlayerSequence(shoe, bankroll, dealerHand, playerHand, bet, allPlayerHands, True, settings)

    dealerVal = DealerSequence(shoe, dealerHand, settings)

    moneyWonThisHand = 0
    amountBet = 0

    for handVal in allPlayerHands:  # handVal has format (value, bet, natural)
        value, wager, isNatural = handVal
        amountBet += wager

        if isNatural:  # natural blackjack
            if not dealerVal[1]:
                print(f"You won a hand by natural blackjack with a wager of {wager}. Payout is 3 to 2.")
                moneyWonThisHand += wager * blackjack_payout
            else:
                print(f"You pushed a hand with a wager of {wager}.")

        elif value > dealerVal[0]:  # win
            print(f"You won a hand with a wager of {wager}.")
            moneyWonThisHand += wager

        elif value == dealerVal[0]:  # push
            print(f"You pushed a hand with a wager of {wager}.")

        else:  # loss
            print(f"You lost a hand with a wager of {wager}.")
            moneyWonThisHand -= wager

    bankroll += moneyWonThisHand

    print(f"You bet {amountBet}.")

    if moneyWonThisHand > 0:
        print(f"You won {moneyWonThisHand} this round.")
    elif moneyWonThisHand < 0:
        print(f"You lost {-moneyWonThisHand} this round.")
    else:
        print("You broke even this round.")

    return moneyWonThisHand


def PlayRound(settings):
    print("Bankroll?")
    myBankroll = int(input())

    myShoe = MakeShoe(settings)

    while True:
        #TODO: Handle empty shoe
        #TODO: Handle condition of losing all your money
        #TODO: Handle 
        print(f"Bankroll is {myBankroll}.")
        print("P to play, Q to quit.")
        playerAction = input()

        if playerAction == "P":
            myBankroll += PlayHand(myShoe, myBankroll, settings)
        elif playerAction == "Q":
            break
        else:
            print("Invalid input")
            continue

    print("Hope you had fun.")
