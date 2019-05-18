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

    def match_dealer(self, dealer_card, card1, card2, matchbet):
        win = False
        for c in (card1, card2):
            if poker.suited_match(dealer_card, c):
                print("*****You suited match dealer!!*****")
                win = True
                self.money += 12 * matchbet
            elif poker.unsuited_match(dealer_card, c):
                print("*****You unsuited match dealer!!*****")
                win = True
                self.money += 4 * matchbet
        if not win:
            print("*****Sorry, you didn't match dealer!!*****")
        #print(self.show_money())


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
    while dealer.getscore()[1] < target:
        dealer.deal(cards.get_card())

    if dealer.getscore()[1] > 21:
        while dealer.getscore()[0] < target:
            dealer.deal(cards.get_card())

    if dealer.getscore()[0] > 21:
        dealer.gobust()

    return