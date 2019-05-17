import random
import poker

class person(object):
    def __init__(self):
        self.hand = []
        self.bust = False

    def deal(self, card):
        self.hand.append(card)

    def end(self):
        pass

    def showhand(self):
        show = []
        for c in self.hand:
            if c.is_faceup():
                show.append(c.get_info())
            else:
                show.append("*")
        return show

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
        values = {
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
            v = c.get_info()[1]
            if v == 'A':
                hard += values[v][0]
                soft += values[v][1]
            else:
                hard += values[v]
                soft += values[v]
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

def dealer_play(dealer, cards, player_score):
    target = max(player_score, 17)
    while dealer.getscore()[1] <= target:
        dealer.deal(cards.get_card())

    if dealer.getscore()[1] > 21:
        while dealer.getscore()[0] < target:
            dealer.deal(cards.get_card())

    if dealer.getscore()[0] > 21:
        dealer.gobust()

    return

def main():

    #Initialize a dealer and a player
    print("Let's play Blackjack!" )
    dealer = person()
    balance = int(input("How much do you want to buy in? "))
    player1 = player(balance)


    #Shuffle 4 decks 3 times
    decks = poker.deck(4)
    decks.shuffle_deck(3)

    print("Ready to play!")

    play_again = True

    while play_again:
        totalbet = 0
        bet = player1.make_bet()
        totalbet += bet

        #Both dealer and player get 2 cards. Player show his cards face up while dealer has 1 of his cards face up
        #and the other one face down
        player1.deal(decks.get_card())
        flip_card = decks.get_card()
        flip_card.flip()
        dealer.deal(flip_card)
        player1.deal(decks.get_card())
        dealer.deal(decks.get_card())

        print("Now dealer has ", end = '')
        print(dealer.showhand())
        print("Now you have ", end = '')
        print(player1.showhand())

        #Player plays first. He can choose either Hit or Stay. If choose to stay, he will be dealt 1 card
        #and his current hand and score will be shown, whether Blackjack or bust will be shown as well;
        #if choose to stay, he will finish his round.
        while True:

            if player1.is_blackjack():
                player1.win_blackjack(bet)
                balance = player1.show_money()
                break

            play = input("Do you want to [H]it or [S]tand? H/S: ").lower()
            if play == 'h':
                bet = player1.make_bet()
                totalbet += bet
                player1.deal(decks.get_card())
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

        if player1.isbust():
            print("/////You are bust, so you lose!!!/////")
            break
        else:

            player_score = player1.getscore()[0] if player1.getscore()[1] > 21 else player1.getscore()[1]
            print("You have " + str(player_score))
            print("Now it is dealer's turn.")
            flip_card.flip()
            dealer_play(dealer, decks, player_score)

            #Show both dealer and player hands
            print("Dealer's hand is ", end = '')
            print(dealer.showhand())
            print("Player's hand is ", end = '')
            print(player1.showhand())

            if dealer.isbust():
                player1.win_bet(totalbet)
                print("/////Dealer is bust but you are not, so you win!!!/////")
            else:
                dealer_score = dealer.getscore()[0] if dealer.getscore()[1] > 21 else dealer.getscore()[1]
                print("Dealer has " + str(dealer_score))
                if player_score == dealer_score:
                    player1.break_even(totalbet)
                    print("/////You and dealer have the same points, so you are even!!!/////")
                elif player_score > dealer_score:
                    player1.win_bet(totalbet)
                    print("/////You have more points, so you win!!!/////")
                else:
                    print("/////Dealer has more points so dealer win!!!/////")

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
