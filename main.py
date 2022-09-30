import pygame
from card import *
from enum import Enum


class GameState(Enum):
    PLAYING = 0
    ENDED = 1


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
        self.state = GameState.PLAYING

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

    def switchPlayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1



# pygame.init()
# bounds = (1024, 768)
# window = pygame.display.set_mode(bounds)
# pygame.display.set_caption("Golf")