import random
class card(object):
    def __init__(self, s, v, f = 1):
        self.suit = s
        self.value = v
        self.face_up = f

    def flip(self):
        self.face_up = not self.face_up

    def is_faceup(self):
        return self.face_up

    def get_info(self):
        return self.suit, self.value

class deck(object):
    def __init__(self, n):
        self.cards = []
        for i in range(n):
            for s in ['D', 'H', 'S', 'C']:
                for v in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']:
                    c = card(s, v)
                    self.cards.append(c)

    def shuffle_deck(self, n):
        for i in range(n):
            random.shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()

def test():
    mydeck = deck(2)
    mydeck.shuffle_deck(3)
    pick = mydeck.get_card()
    print("test")
    print(pick.get_info())

if __name__ == "__main__":
    test()