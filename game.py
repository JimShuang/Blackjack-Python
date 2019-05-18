import random
import poker
import people

def main():

    #Initialize a dealer and a player
    print("Let's play Blackjack!" )
    dealer = people.person()
    balance = int(input("How much do you want to buy in? "))
    player1 = people.player(balance)


    #Shuffle 4 decks 3 times
    decks = poker.deck(4)
    decks.shuffle_deck(3)

    print("Ready to play!")

    play_again = True

    while play_again:
        totalbet = 0
        bet = player1.make_bet()
        totalbet += bet

        play_match = input("Do you want to match the dealer? Y/N: ").lower()

        if play_match == 'y':
            matchbet = player1.make_bet()

        #Both dealer and player get 2 cards. Player show his cards face up while dealer has 1 of his cards face up
        #and the other one face down
        card1, faceup, card2, flip_card = decks.get_card(), decks.get_card(), decks.get_card(), decks.get_card()
        player1.deal(card1)
        dealer.deal(faceup)
        player1.deal(card2)
        flip_card.flip()
        dealer.deal(flip_card)

        print("Now dealer has ", end = '')
        print(dealer.showhand())
        print("Now you have ", end = '')
        print(player1.showhand())

        if play_match == 'y':
            player1.match_dealer(faceup, card1, card2, matchbet)

        if player1.is_blackjack():
            player1.win_blackjack(bet)
            balance = player1.show_money()
            player1.clear()
            dealer.clear()
            play_again = True if input("Do you want to play again? Y/N: ").lower() == 'y' else False
            continue

        #Player plays first. He can choose either Hit or Stay. If choose to stay, he will be dealt 1 card
        #and his current hand and score will be shown, whether Blackjack or bust will be shown as well;
        #if choose to stay, he will finish his round.
        while True:
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
            elif play == 's':
                break

        if player1.isbust():
            balance = player1.show_money()
            player1.clear()
            dealer.clear()
            play_again = True if input("Do you want to play again? Y/N: ").lower() == 'y' else False
            print("/////You are bust, so you lose!!!/////")
            continue
        else:
            player_score = player1.getscore()[0] if player1.getscore()[1] > 21 else player1.getscore()[1]
            print("You have " + str(player_score))
            print("Now it is dealer's turn.")
            flip_card.flip()
            people.dealer_play(dealer, decks, player_score)

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





