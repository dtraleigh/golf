import pygame
from card import *
from enum import Enum


class GameState(Enum):
    PREP = 0
    PLAYING = 1
    LASTROUND = 2
    ENDED = 3


class GolfEngine:
    deck = None
    player1 = None
    player2 = None
    pile_down = None
    pile_up = None
    current_player = None
    state = None
    result = None

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.pile_down = PileDown()
        self.pile_up = PileUp()
        self.deal()
        self.current_player = self.player1
        self.state = GameState.PREP
        self.draw_count = 0
        self.option_to_pass = False

    def deal(self):
        # 6 cards to each player
        for i in range(0, 6):
            self.player1.draw(self.deck)
            self.player2.draw(self.deck)

        # Add the remainder of the cards to pile_down
        while self.deck.length() > 0:
            self.pile_down.add(self.deck.deal_card())

        # Add a card from pile_down to pile_up
        self.pile_up.add(self.pile_down.deal_card())

        # print(f"Player 1 cards: {self.player1.hand}")
        # print(f"Player 2 cards: {self.player2.hand}")

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_game(self):
        self.state = GameState.PLAYING

    def draw_card_on_turn(self):
        if self.draw_count == 0:
            self.draw_count += 1
        else:
            self.draw_count = 1

    def exchange_hand_card_with_pile_up_card(self, hand_card, pile_up_card):
        players_selected_card_list_pos = self.current_player.hand.index(hand_card)

        self.pile_up.cards[0] = hand_card
        self.current_player.hand[players_selected_card_list_pos] = pile_up_card

        self.current_player.hand[players_selected_card_list_pos].flip_card()

    def end_turn(self):
        self.last_round()
        self.switch_player()
        self.pile_up.select_pile_up_card()
        self.draw_count = 0
        self.pile_up.selected = False
        self.player1.unselect_all_cards()
        self.player2.unselect_all_cards()
        self.option_to_pass = False

    def last_round(self):
        if self.current_player.has_all_cards_face_up():
            self.state = GameState.LASTROUND

    def end_game(self):
        self.state = GameState.ENDED

    def show_pass_button(self):
        self.option_to_pass = True
