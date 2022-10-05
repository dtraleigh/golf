import pygame
from card import *
from engine import *

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

pile_down_rect = card_back.get_rect()
pile_down_rect.center = (1300, 680)

# Initial draw card
pile_up_rect = golf.pile_up.cards[0]._image.get_rect()
pile_up_rect.center = (950, 510)

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

    for card, r in zip(golf.player1.hand, p1_rects):
        screen.blit(pygame.transform.scale(card._image, card_size), r)

    for card, r in zip(golf.player2.hand, p2_rects):
        screen.blit(pygame.transform.scale(card._image, card_size), r)

    # Create pile_down
    screen.blit(pygame.transform.scale(card_back, card_size), pile_down_rect)

    # Add initial draw card
    screen.blit(pygame.transform.scale(golf.pile_up.cards[0]._image, card_size), pile_up_rect)

    if DEBUG_MODE:
        mouse_position = pygame.mouse.get_pos()
        mouse_pos_text = font.render(f"Mouse Pos: {str(mouse_position)}", True, green, blue)
        screen.blit(mouse_pos_text, (600, 670))
        p1_hand_text = font.render(f"P1 Hand: {str(golf.player1.hand)}", True, green, blue)
        screen.blit(p1_hand_text, (230, 900))
        p1_hand_text = font.render(f"P2 Hand: {str(golf.player2.hand)}", True, green, blue)
        screen.blit(p1_hand_text, (230, 930))
        pile_down_count = font.render(f"Cards in pile_down: {str(golf.pile_down.length())}", True, green, blue)
        screen.blit(pile_down_count, (600, 700))
        pile_up_count = font.render(f"Cards in pile_up: {str(golf.pile_up.length())}", True, green, blue)
        screen.blit(pile_up_count, (600, 730))

    pygame.display.flip()

pygame.quit()
