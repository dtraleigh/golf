import pygame
from card import *
from engine import *


def draw_rect_border(surface, x, y):
    for i in range(4):
        pygame.draw.rect(surface, red, (x - i, y - i, card_size[0], card_size[1]), 1)


def exchange_button_behavior(mouse):
    # if mouse is hovered on a button it changes to lighter shade
    exchange_button_x = 950
    exchange_button_y = 100
    if exchange_button_x <= mouse[0] <= exchange_button_x + 140 and exchange_button_y <= mouse[1] <= exchange_button_y + 40:
        pygame.draw.rect(screen, color_light, [exchange_button_x, exchange_button_y, 140, 40])
    else:
        pygame.draw.rect(screen, color_dark, [exchange_button_x, exchange_button_y, 140, 40])

    # superimposing the text onto our button
    screen.blit(exchange_button_text, (exchange_button_x, exchange_button_y))


# game init
pygame.init()
width = 1920
height = 1080
bounds = (width, height)
screen = pygame.display.set_mode(bounds)
pygame.display.set_caption("Golf")

# For debugging
DEBUG_MODE = True

# some colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
red = (255, 0, 0)

# text
font = pygame.font.Font("freesansbold.ttf", 32)
smallfont = pygame.font.SysFont('Corbel', 35)
title_text = font.render("Golf, the card game", True, green, blue)
p1_text = font.render("Player 1", True, green, blue)
p2_text = font.render("Player 2", True, green, blue)
exchange_button_text = smallfont.render("Exchange", True, white)

# rects
title_rect = title_text.get_rect()
title_rect.center = (width // 2, 50)

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
    card_rect = card._image.get_rect()
    card_rect.center = position
    card_rect.w, card_rect.h = card_size
    p1_rects.append(card_rect)
p1_border_control = [False, False, False, False, False, False]

for card, position in zip(golf.player2.hand, player2_card_positions):
    card_rect = card._image.get_rect()
    card_rect.center = position
    card_rect.w, card_rect.h = card_size
    p2_rects.append(card_rect)
p2_border_control = [False, False, False, False, False, False]

pile_down_rect = card_back.get_rect()
pile_down_rect.center = (1300, 680)

# Initial draw card
pile_up_rect = golf.pile_up.cards[0]._image.get_rect()
pile_up_rect.center = (950, 510)

selected = None
is_running = True

while is_running:
    ###### Some basics ######
    # green background
    screen.fill((4, 157, 0))

    # Text rects
    screen.blit(title_text, title_rect)
    screen.blit(p1_text, (200, 1000))
    screen.blit(p2_text, (1550, 1000))

    ###### End basics ######

    ###### Some Card stuff ######
    for card, r in zip(golf.player1.hand, p1_rects):
        screen.blit(pygame.transform.scale(card._image, card_size), r)

    for card, r in zip(golf.player2.hand, p2_rects):
        screen.blit(pygame.transform.scale(card._image, card_size), r)

    # Create pile_down
    screen.blit(pygame.transform.scale(card_back, card_size), pile_down_rect)

    # Add initial draw card
    screen.blit(pygame.transform.scale(golf.pile_up.cards[0]._image, card_size), pile_up_rect)

    ###### End Card stuff ######

    ###### start Game logic ######
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # stores the (x,y) coordinates into the variable as a tuple
        mouse_position = pygame.mouse.get_pos()

        exchange_button_behavior(mouse_position)

        # If mouse_click is inside a rect, add the border
        for border_control, p1_rect in zip(p1_border_control, p1_rects):
            if border_control:
                draw_rect_border(screen, p1_rect.x, p1_rect.y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if any p1_rects were clicked
                mouse_position_down = pygame.mouse.get_pos()
                for c, (rect, border_control) in enumerate(zip(p1_rects, p1_border_control)):
                    p1_click = rect.collidepoint(mouse_position_down)
                    if p1_click == 1:
                        p1_border_control[c] = not p1_border_control[c]

        for border_control, p2_rect in zip(p2_border_control, p2_rects):
            if border_control:
                draw_rect_border(screen, p2_rect.x, p2_rect.y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if any p2_rects were clicked
                mouse_position_down = pygame.mouse.get_pos()
                for c, (rect, border_control) in enumerate(zip(p2_rects, p2_border_control)):
                    p2_click = rect.collidepoint(mouse_position_down)
                    if p2_click == 1:
                        p2_border_control[c] = not p2_border_control[c]

    ###### end Game logic ######

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
            # p1_border_control_debug = font.render(f"p1_border_control: {str(p1_border_control)}", True, green, blue)
            # screen.blit(p1_border_control_debug, (600, 760))
            # p1_rect_size = font.render(f"first rect size: {str(p1_rects[0].size)}", True, green, blue)
            # screen.blit(p1_rect_size, (600, 790))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click_prompt = font.render(f"Clickity {event.pos}", True, green, blue)
                    screen.blit(mouse_click_prompt, (1, 1))

        pygame.display.flip()

pygame.quit()
