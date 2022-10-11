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


def get_number_of_flipped_cards(hand):
    # Take in a hand and return the number of cards that are flipped
    flipped_cards = 0
    for card in hand:
        if card._face:
            flipped_cards += 1

    return flipped_cards


def clear_all_borders():
    return [False, False, False, False, False, False]


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
pile_down_rect.w, pile_down_rect.h = card_size

# Initial draw card
pile_up_rect = golf.pile_up.cards[0]._image.get_rect()
pile_up_rect.center = (950, 510)
pile_up_counter = 0

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
        if card._face:
            screen.blit(pygame.transform.scale(card._image, card_size), r)
        else:
            screen.blit(pygame.transform.scale(card_back, card_size), r)

    for card, r in zip(golf.player2.hand, p2_rects):
        if card._face:
            screen.blit(pygame.transform.scale(card._image, card_size), r)
        else:
            screen.blit(pygame.transform.scale(card_back, card_size), r)

    # Create pile_down
    screen.blit(pygame.transform.scale(card_back, card_size), pile_down_rect)

    # Create pile up
    screen.blit(pygame.transform.scale(golf.pile_up.cards[pile_up_counter]._image, card_size), pile_up_rect)

    ###### End Card stuff ######

    ###### start Game logic ######
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # stores the (x,y) coordinates into the variable as a tuple
        mouse_position = pygame.mouse.get_pos()

        # Prep phase
        if golf.state.value == 0:
            prep_message = font.render("Flip two cards each", True, green, blue)
            screen.blit(prep_message, (650, 170))

            # Each player only flips two cards
            p1_num_flipped_cards = get_number_of_flipped_cards(golf.player1.hand)
            p2_num_flipped_cards = get_number_of_flipped_cards(golf.player2.hand)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position_down = pygame.mouse.get_pos()
                if event.button == 1:
                    for rect, card in zip(p1_rects, golf.player1.hand):
                        p1_click = rect.collidepoint(mouse_position_down)
                        if p1_click == 1 and p1_num_flipped_cards < 2:
                            card.flip_card()

                    for rect, card in zip(p2_rects, golf.player2.hand):
                        p2_click = rect.collidepoint(mouse_position_down)
                        if p2_click == 1 and p2_num_flipped_cards < 2:
                            card.flip_card()

            if p1_num_flipped_cards == 2 and p2_num_flipped_cards == 2:
                golf.play_game()

        # playing phase
        elif golf.state.value == 1:
            current_player_text = font.render(f"Turn: {golf.current_player.name}", True, green, blue)
            screen.blit(current_player_text, (950, 140))

            # On their turn, a player can either
            # Reveal a card that has _face = False
            # OR
            # exchange any card in the hand for the pile_up face card
            # OR
            # move top of pile_down to pile_up
            # then either
            #  1. Pass
            #  2. exchange any card in the hand for the pile_up face card

            # Before drawing from the pile_down, player can either
            # 1. Reveal a card in their hand
            # 2. Exchange pile_up card for a card in their hand
            possible_rects_to_click = [pile_down_rect, pile_up_rect]

            if golf.current_player.name == "Player 1":
                # Player 1 Logic
                possible_rects_to_click += p1_rects
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position_down = pygame.mouse.get_pos()
                    for count, rect in enumerate(possible_rects_to_click):
                        player_click = rect.collidepoint(mouse_position_down)
                        if player_click == 1:
                            if count == 0:
                                # Player clicked on pile_down
                                pass
                            elif count == 1:
                                # Player clicked on pile_up
                                # toggle border and select/deselect it
                                golf.pile_up.select_pile_up_card()
                            else:
                                # If the card is face down, flip it on click
                                selected_card = golf.player1.hand[count - 2]
                                if not selected_card.face:
                                    selected_card.flip_card()
                                    golf.switch_player()
                                    p1_border_control = clear_all_borders()
                                else:
                                    # else if card in this rect is face up, add the border and mark it selected
                                    p1_border_control = [False, False, False, False, False, False]
                                    p1_border_control[count - 2] = not p1_border_control[count - 2]
                                    golf.current_player.select_card_in_hand(golf.current_player.hand[count - 2])
                # If a face up card from the hand is selected and the pile_up card is selected, the player may want to
                # make an exchange. Prompt them and offer an exchange button
                if golf.pile_up.is_selected() and golf.current_player.get_selected_card():
                    exchange_button_behavior(mouse_position)

            else:
                # Player 2 Logic
                possible_rects_to_click += p2_rects
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position_down = pygame.mouse.get_pos()
                    for count, rect in enumerate(possible_rects_to_click):
                        player_click = rect.collidepoint(mouse_position_down)
                        if player_click == 1:
                            if count == 0:
                                # Player clicked on pile_down
                                pass
                            elif count == 1:
                                # Player clicked on pile_up
                                golf.pile_up.select_pile_up_card()
                            else:
                                # If the card is face down, flip it on click
                                selected_card = golf.player2.hand[count - 2]
                                if not selected_card.face:
                                    selected_card.flip_card()
                                    golf.switch_player()
                                    p2_border_control = clear_all_borders()
                                else:
                                    # else if card in this rect is face up, add the border
                                    p2_border_control = [False, False, False, False, False, False]
                                    p2_border_control[count - 2] = not p2_border_control[count - 2]

            # If mouse_click is inside a rect, add the border to that one and remove it from the rest of the hand
            for border_control, p1_rect in zip(p1_border_control, p1_rects):
                if border_control:
                    draw_rect_border(screen, p1_rect.x, p1_rect.y)

            # If mouse_click is inside a rect, add the border to that one and remove it from the rest of the hand
            for border_control, p2_rect in zip(p2_border_control, p2_rects):
                if border_control:
                    draw_rect_border(screen, p2_rect.x, p2_rect.y)

            if golf.pile_up.selected:
                draw_rect_border(screen, pile_up_rect.x, pile_up_rect.y)

            # Click on the top of pile_down and add it to the pile_up
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         # Check if the pile_down was clicked
            #         mouse_position_down = pygame.mouse.get_pos()
            #         pile_down_click = pile_down_rect.collidepoint(mouse_position_down)
            #         if pile_down_click == 1:
            #             golf.pile_up.add(golf.pile_down.deal_card())
            #             pile_up_counter += 1
            #             draw_rect_border(screen, pile_down_rect.x, pile_down_rect.y)
            #
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         # Check if any p1_rects were clicked
            #         mouse_position_down = pygame.mouse.get_pos()
            #         for c, (rect, border_control) in enumerate(zip(p1_rects, p1_border_control)):
            #             p1_click = rect.collidepoint(mouse_position_down)
            #             if p1_click == 1:
            #                 p1_border_control[c] = not p1_border_control[c]
            #
            # for border_control, p2_rect in zip(p2_border_control, p2_rects):
            #     if border_control:
            #         draw_rect_border(screen, p2_rect.x, p2_rect.y)
            #
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         # Check if any p2_rects were clicked
            #         mouse_position_down = pygame.mouse.get_pos()
            #         for c, (rect, border_control) in enumerate(zip(p2_rects, p2_border_control)):
            #             p2_click = rect.collidepoint(mouse_position_down)
            #             if p2_click == 1:
            #                 p2_border_control[c] = not p2_border_control[c]

        # game over man
        elif golf.state.value == 2:
            pass

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
            current_player = font.render(f"current_player: {golf.current_player.name}", True, green, blue)
            screen.blit(current_player, (600, 760))
            pile_up_is_selected = font.render(f"golf.pile_up.get_is_selected: {golf.pile_up.is_selected()}", True, green, blue)
            screen.blit(pile_up_is_selected, (600, 790))
            current_player_get_selected = font.render(f"get_selected_card: {golf.current_player.get_selected_card()}", True, green, blue)
            screen.blit(current_player_get_selected, (600, 820))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click_prompt = font.render(f"Clickity {event.pos}", True, green, blue)
                    screen.blit(mouse_click_prompt, (1, 1))

        pygame.display.flip()

pygame.quit()
