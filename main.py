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

# For debugging
DEBUG_MODE = True

# some colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

# text
font = pygame.font.Font("freesansbold.ttf", 32)
title_text = font.render("Golf, the card game", True, green, blue)
p1_text = font.render("Player 1", True, green, blue)
p2_text = font.render("Player 2", True, green, blue)

# rects
title_rect = title_text.get_rect()
title_rect.center = (X // 2, 50)

# card stuff
card_back = pygame.image.load('images/BACK.png')
card_size = (166, 232)

# player hand positions
player1_card_positions = ((200, 200), (400, 200), (200, 500), (400, 500), (200, 800), (400, 800))
player2_card_positions = ((1520, 200), (1720, 200), (1520, 500), (1720, 500), (1520, 800), (1720, 800))

# Game init
golf = GolfEngine()

# Create card rects
p1_rects = []
p2_rects = []

for card, position in zip(golf.player1.hand, player1_card_positions):
    this_card = card._image.get_rect()
    this_card.center = position
    p1_rects.append(this_card)

for card, position in zip(golf.player2.hand, player2_card_positions):
    this_card = card._image.get_rect()
    this_card.center = position
    p2_rects.append(this_card)

selected = None
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # green background
    screen.fill((4, 157, 0))

    # Text rects
    screen.blit(title_text, title_rect)
    screen.blit(p1_text, (200, 1000))
    screen.blit(p2_text, (1550, 1000))

    # for card, position in zip(golf.player1.hand, player1_card_positions):
    #     screen.blit(pygame.transform.scale(card._image, card_size), position)
    #
    # for card, position in zip(golf.player2.hand, player2_card_positions):
    #     screen.blit(pygame.transform.scale(card._image, card_size), position)

    for card, r in zip(golf.player1.hand, p1_rects):
        screen.blit(pygame.transform.scale(card._image, card_size), r)

    for card, r in zip(golf.player2.hand, p2_rects):
        screen.blit(pygame.transform.scale(card._image, card_size), r)

    if DEBUG_MODE:
        mouse_position = pygame.mouse.get_pos()
        mouse_pos_text = font.render(str(mouse_position), True, green, blue)
        # mouse_pos_text = font.render("mouse coords", True, green, blue)
        screen.blit(mouse_pos_text, (1000, 1000))

    pygame.display.flip()

pygame.quit()
