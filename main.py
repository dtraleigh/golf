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
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1


# game init
pygame.init()
X = 1920
Y = 1080
bounds = (X, Y)
screen = pygame.display.set_mode(bounds)
pygame.display.set_caption("Golf")

# some colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

# text
font = pygame.font.Font("freesansbold.ttf", 32)
text = font.render("Golf, the card game", True, green, blue)
title_rect = text.get_rect()
title_rect.center = (X // 2, 50)

# card stuff
card_back = pygame.image.load('images/BACK.png')
card_size = (166, 232)

# player hand positions
player1_card_positions = ((100, 100), (300, 100), (100, 400), (300, 400), (100, 700), (300, 700))
player2_card_positions = ((1420, 100), (1620, 100), (1420, 400), (1620, 400), (1420, 700), (1620, 700))

# Game init
golf = GolfEngine()

is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # green background
    screen.fill((4, 157, 0))

    # Title
    screen.blit(text, title_rect)

    for card, position in zip(golf.player1.hand, player1_card_positions):
        screen.blit(pygame.transform.scale(card._image, card_size), position)

    for card, position in zip(golf.player2.hand, player2_card_positions):
        screen.blit(pygame.transform.scale(card._image, card_size), position)

    # Create a Deck, deal a card, and place it on the screen
    # deck = Deck()
    # deck.shuffle()
    # card1 = deck.deal_card()
    # screen.blit(card1._image, (100, 100))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (100, 100))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (300, 100))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (100, 400))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (300, 400))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (100, 700))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (300, 700))
    #
    # screen.blit(pygame.transform.scale(card1._image, card_size), (1420, 100))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (1620, 100))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (1420, 400))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (1620, 400))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (1420, 700))
    # screen.blit(pygame.transform.scale(card1._image, card_size), (1620, 700))

    pygame.display.flip()

pygame.quit()
