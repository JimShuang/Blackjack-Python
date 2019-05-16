import random

class person(object):
    def __init__(self):
        self.hand = []
        self.bust = False

#This method add a card to hand
    def deal(self, card):
        self.hand.append(card)

#This method allows people to quit, not adding card anymore
    def end(self):
        pass

#This method show people card on his hand
    def showhand(self):
        return self.hand

    def gobust(self):
        self.bust = True

    def isbust(self):
        return self.bust

    def is_blackjack(self):
        return self.getscore()[1] == 21

    def clear(self):
        self.hand = []

#This method return people's total score in hand; if ace exists, it will output 2 scores, one hard
# score and one soft score
    def getscore(self):
        cards = {
            'A': [1, 11],
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 10,
            'Q': 10,
            'K': 10
        }
        hard, soft = 0, 0
        for c in self.hand:
            if c == 'A':
                hard += cards[c][0]
                soft += cards[c][1]
            else:
                hard += cards[c]
                soft += cards[c]
        return hard, soft

class player(person):
    def __init__(self, money):
        person.__init__(self)
        self.money = money

    def make_bet(self):
        bet = int(input("Please place your bet: "))
        while bet > self.money:
            bet = int(input("Not enough balance. Please reduce your bet! Please place your bet: "))
        self.money -= bet
        return bet

#If player wins, he will get double what he bet
    def win_bet(self, bet):
        self.money += 2 * bet

#If break even, he will get back the bet
    def break_even(self, bet):
        self.money += bet

#If player gets a Blackjack, he will automatically get 2.5 times what he bet regardless what dealer has.
    def win_blackjack(self, bet):
        print("*****You got a Blackjack!*****")
        self.money += 2.5 * bet

    def show_money(self):
        print("Your balance is ", end = '')
        print(self.money)
        return self.money

    def gobust(self):
        print("*****You are bust!!*****")
        self.bust = True

#In this method, dealer will decide how to deal his own card, Specifically, if a dealer get a
#score < 17, no matter hard or soft, dealer will deal one card; else, dealer will quit his round.
def dealer_play(dealer, cards):

    if max(dealer.getscore()) == 21:
        print("*****Dealer gets a Blakcjack!!*****")

    while max(dealer.getscore()) < 17:
        dealer.deal(cards.pop())

    while max(dealer.getscore()) > 21 and min(dealer.getscore()) < 17:
        dealer.deal(cards.pop())

    if min(dealer.getscore()) > 21:
        dealer.gobust()
        print("*****Dealer is bust!!*****")


def main():

#Initialize a dealer and a player
    print("Let's play Blackjack!" )
    dealer = person()
    balance = int(input("How much do you want to buy in? "))
    player1 = player(balance)


#Shuffle 4 decks 3 times
    deck = ['A','1','2','3','4','5','6','7','8','9','10','J','Q','K'] * 16
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)

    print("Ready to play!")
    totalbet = 0

    play_again = True
    while play_again:
#Now player1 places the initial bet and any amount is allowed.
        bet = player1.make_bet()
        totalbet += bet

#Both dealer and player get 2 cards. Player show his cards face up while dealer has 1 of his cards face up
#and the other one face down
        player1.deal(deck.pop())
        dealer.deal(deck.pop())
        player1.deal(deck.pop())
        dealer.deal(deck.pop())

        print("Now dealer has * and ", end = '')
        print(dealer.showhand()[0])
        print("Now you have ", end = '')
        print(player1.showhand())
        if player1.is_blackjack():
            player1.win_blackjack(bet)
            balance = player1.show_money()
            quit()

        print("Now it is your turn.")

#Player plays first. He can choose either Hit or Stay. If choose to stay, he will be dealt 1 card
#and his current hand and score will be shown, whether Blackjack or bust will be shown as well;
#if choose to stay, he will finish his round.
        while True:
            play = input("Do you want to [H]it or [S]tand? H/S: ").lower()
            if play == 'h':
                bet = player1.make_bet()
                totalbet += bet
                player1.deal(deck.pop())
                print('You now have ', end = '')
                print(player1.showhand())
                print('Your score is ', end = '')
                if player1.getscore()[0] == player1.getscore()[1]:
                    print(player1.getscore()[0])
                    if player1.getscore()[0] > 21:
                        player1.gobust()
                        break
                    elif player1.getscore()[0] == 21:
                        break
                else:
                    if player1.getscore()[1] > 21:
                        print(player1.getscore()[0])
                        if player1.getscore()[0] > 21:
                            player1.gobust()
                            break
                    else:
                        print(player1.getscore())
            else:
                player1.end()
                break

        print("Now it is dealer's turn.")
        dealer_play(dealer, deck)

#Show both dealer and player hands
        print("Dealer's hand is ", end = '')
        print(dealer.hand)
        print("Player's hand is ", end = '')
        print(player1.hand)

        if player1.isbust():
            if dealer.isbust():
                player1.break_even(totalbet)
                print("/////Both bust!!!/////")
            else:
                print("/////You lose!!!/////")
        else:
            if dealer.isbust():
                player1.win_bet(totalbet)
                print("/////You win!!!/////")
            else:
                player_score = player1.getscore()[0] if player1.getscore()[1] > 21 else player1.getscore()[1]
                dealer_score = dealer.getscore()[0] if dealer.getscore()[1] > 21 else dealer.getscore()[1]
                if player_score == dealer_score:
                    player1.break_even(totalbet)
                    print("/////Tie!!!/////")
                elif player_score > dealer_score:
                    player1.win_bet(totalbet)
                    print("/////You win!!!/////")
                else:
                    print("/////Dealer win!!!/////")

        player1.clear()
        dealer.clear()

        balance = player1.show_money()
        if balance <= 0:
            print("*****You have no balance left!!*****")
            break
        play_again = True if input("Do you want to play again? Y/N: ").lower() == 'y' else False

    print("/////Thank you for playing!!!/////")

if __name__ == "__main__":
    main()






