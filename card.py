import random
import pygame


class Card:
    def __init__(self, suit, number, value):
        self._suit = suit  # underscore means should not change this, just good practice and good programming style
        self._number = number
        self._image = pygame.image.load(f"images/{self._suit}-{str(self.number)}.svg")
        self._value = value
        self._face = False
        self._is_selected = False

    def __repr__(self):
        return f"{self._number} of {self._suit}"

    @property
    def suit(self):
        return self._suit

    @property
    def number(self):
        return self._number

    @property
    def image(self):
        return self._image

    @property
    def value(self):
        return self._value

    @property
    def hand_position(self):
        return self.X, self.Y

    @property
    def face(self):
        # face up or down, default is down which I'm calling False
        return self._face

    @property
    def selected(self):
        return self._is_selected

    def flip_card(self):
        # In golf, once a card in a hand is flipped up, it is never face down again
        if not self._face:
            self._face = True

    def select_card(self):
        self._is_selected = not self._is_selected

    # @suit.setter
    # def suit(self, suit):
    #     if suit in ["HEART", "CLUB", "DIAMOND", "SPADE"]:
    #         self._suit = suit
    #     else:
    #         print("Not a valid suit.")
    #
    # @number.setter
    # def number(self, number):
    #     if number.upper() in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]:
    #         self._number = number
    #     else:
    #         print("Not a valid number.")


class Deck:
    def __init__(self):
        self._cards = []
        self.populate()
        # print(self._cards)

    def populate(self):
        suits = ["HEART", "CLUB", "DIAMOND", "SPADE"]
        # 1 through 13 or A, 1-10, J, Q, K
        numbers = [x for x in range(1, 14)]

        for suit in suits:
            for number in numbers:
                # if Ace or 1-10:
                if number <= 10:
                    self._cards.append(Card(suit, number, number))
                # Jack and Queen are 10 points
                elif number == 11 or number == 12:
                    self._cards.append(Card(suit, number, 10))
                # King is 0 points
                elif number == 13:
                    self._cards.append(Card(suit, number, 0))

        # add the two jokers
        self._cards.append(Card("JOKER", 1, -2))
        self._cards.append(Card("JOKER", 2, -2))

    def shuffle(self):
        random.shuffle(self._cards)

    def view_deck(self):
        print(f"There are {str(len(self._cards))} cards in the deck")
        print(self._cards)

    def deal_card(self):
        return self._cards.pop()

    def length(self):
        return len(self._cards)


class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.selected_card = None

    def draw(self, deck):
        self.hand.append(deck.deal_card())

    def get_player_name(self):
        return self.name

    def select_card_in_hand(self, card):
        self.selected_card = card

    def get_selected_card(self):
        return self.selected_card


class PileDown:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def deal_card(self):
        return self.cards.pop()

    def length(self):
        return len(self.cards)


class PileUp:
    def __init__(self):
        self.cards = []
        self.selected = False

    def add(self, card):
        self.cards.append(card)

    def length(self):
        return len(self.cards)

    def select_pile_up_card(self):
        self.selected = not self.selected

    def is_selected(self):
        return self.selected
