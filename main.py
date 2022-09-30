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
        self.deal()
        self.pile_down = PileDown()
        self.pile_up = PileUp()
        self.current_player = self.player1
        self.state = GameState.PLAYING

    def deal(self):
        for i in range(0, 6):
            self.player1.draw(self.deck)
            self.player2.draw(self.deck)

        print(f"Player 1 cards: {self.player1.hand}")
        print(f"Player 2 cards: {self.player2.hand}")



# pygame.init()
# bounds = (1024, 768)
# window = pygame.display.set_mode(bounds)
# pygame.display.set_caption("Golf")