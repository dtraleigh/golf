import random
import pygame


class Card:
    def __init__(self, suit, number, point_value):
        self._suit = suit  # underscore means should not change this, just good practice and good programming style
        self._number = number
        self._image = pygame.image.load(f"images/{self._suit}-{str(self.number)}.svg")
        self._point_value = point_value
        self._face = False

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
        return self._point_value

    @property
    def hand_position(self):
        return self.X, self.Y

    @property
    def is_face_up(self):
        # face up or down, default is down which I'm calling False
        return self._face

    def flip_card(self):
        # In golf, once a card in a hand is flipped up, it is never face down again
        if not self._face:
            self._face = True


class Deck:
    def __init__(self):
        self._cards = []
        self.populate()
        # print(self._cards)

    def populate(self):
        suits = ["HEART", "CLUB", "DIAMOND", "SPADE"]
        # 1 through 14 representing A, 1-10, J, Q, K, Joker
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
        self._cards.append(Card("JOKER1", 14, -2))
        self._cards.append(Card("JOKER2", 14, -2))

    def shuffle(self):
        random.shuffle(self._cards)

    def view_deck(self):
        print(f"There are {str(len(self._cards))} cards in the deck")
        print(self._cards)

    def deal_card(self):
        return self._cards.pop()

    def length(self):
        return len(self._cards)

    def get_specific_card_from_deck(self, suit, number):
        # suits are "HEART", "CLUB", "DIAMOND", "SPADE", "JOKER1", "JOKER2"
        # number can be 1 through 14 representing A, 1-10, J, Q, K, Joker
        for count, card in enumerate(self._cards):
            if card._suit == suit and card._number == number:
                return self._cards.pop(count)
        return None

class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.selected_card = None
        self.score = 0

    def draw(self, deck):
        self.hand.append(deck.deal_card())

    def get_player_name(self):
        return self.name

    def select_card_in_hand(self, card):
        self.selected_card = card

    def get_selected_card(self):
        return self.selected_card

    def unselect_all_cards(self):
        self.selected_card = None
        for card in self.hand:
            card._is_selected = False

    def has_all_cards_face_up(self):
        for card in self.hand:
            if not card.is_face_up:
                return False
        return True

    def flip_over_all_cards(self):
        for card in self.hand:
            card.flip_card()

    def calculate_score(self, cards):
        # First, check for row pairs and exclude them from the score count
        points_list = []
        if cards[0]._number == cards[1]._number:
            points_list += [0, 0]
        else:
            points_list += [cards[0]._point_value, cards[1]._point_value]

        if cards[2]._number == cards[3]._number:
            points_list += [0, 0]
        else:
            points_list += [cards[2]._point_value, cards[3]._point_value]

        if cards[4]._number == cards[5]._number:
            points_list += [0, 0]
        else:
            points_list += [cards[4]._point_value, cards[5]._point_value]

        return sum(points_list)

    def get_number_of_flipped_cards(self):
        # return the number of cards that are flipped in a player's hand
        flipped_cards = 0
        for card in self.hand:
            if card._face:
                flipped_cards += 1

        return flipped_cards


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
        # self.cards.append(card)
        self.cards = [card] + self.cards

    def length(self):
        return len(self.cards)

    def select_pile_up_card(self):
        self.selected = not self.selected

    def is_selected(self):
        return self.selected

    def get_top_card(self):
        return self.cards[0]
