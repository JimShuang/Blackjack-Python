import random

class person(object):
    def __init__(self):
        self.hand = []
        self.bust = False

#This method add a card to hand
    def deal(self, card):
        self.hand.append(card)

#This method allows people to quit, not adding card anymore
    def quit(self):
        pass

#This method show people card on his hand
    def showhand(self):
        return self.hand

    def gobust(self):
        self.bust = True

    def isbust(self):
        return self.bust

#This method return people's total score in hand; if ace exists, it will output 2 scores, one hard
# score and one soft score
    def getscore(self):
        cards = {
            'A': [1, 11],
            '1': 1,
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
    player = person()


#Shuffle a deck 3 times
    deck = ['A','1','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)

#Both dealer and player get 2 cards. Player show his cards face up while dealer has 1 of his cards face up
#and the other one face down
    print("Ready to play!")
    player.deal(deck.pop())
    dealer.deal(deck.pop())
    player.deal(deck.pop())
    dealer.deal(deck.pop())
    print("Now dealer has * and ", end = '')
    print(dealer.showhand()[0])
    print("Now you have ", end = '')
    print(player.showhand())

    print("Now it is player's turn.")

#Player plays first. He can choose either Hit or Stay. If choose to stay, he will be dealt 1 card
#and his current hand and score will be shown, whether Blackjack or bust will be shown as well;
#if choose to stay, he will finish his round.
    while True:
        play = input("Do you want to [H]it or [S]tay? H/S: ").lower()
        if play == 'h':
            player.deal(deck.pop())
            print('Player now has ', end = '')
            print(player.showhand())
            print('Player score is ', end = '')
            if player.getscore()[0] == player.getscore()[1]:
                print(player.getscore()[0])
                if player.getscore()[0] > 21:
                    player.gobust()
                    print("*****You are bust!!*****")
                    break
                elif player.getscore()[0] == 21:
                    break
            else:
                if player.getscore()[1] > 21:
                    print(player.getscore()[0])
                    if player.getscore()[0] > 21:
                        player.gobust()
                        print("*****You are bust!!*****")
                        break

                elif player.getscore()[1] == 21:
                    print(player.getscore()[1])
                    print("*****You get a Blackjack!!*****")
                    break
                else:
                    print(player.getscore())
        else:
            player.quit()
            break

    print("Now it is dealer's turn.")
    dealer_play(dealer, deck)

#Show both dealer and player hands
    print("Dealer's hand is ", end = '')
    print(dealer.hand)
    print("Player's hand is ", end = '')
    print(player.hand)

    if player.isbust():
        if dealer.isbust():
            print("/////Both bust!!!/////")
        else:
            print("/////You lose!!!/////")
    else:
        if dealer.isbust():
            print("/////You win!!!/////")
        else:
            player_score = player.getscore()[0] if player.getscore()[1] > 21 else player.getscore()[1]
            dealer_score = dealer.getscore()[0] if dealer.getscore()[1] > 21 else dealer.getscore()[1]
            if player_score == dealer_score:
                print("/////Tie!!!/////")
            elif player_score > dealer_score:
                print("/////You win!!!/////")
            else:
                print("/////Dealer win!!!/////")


if __name__ == "__main__":
    main()






