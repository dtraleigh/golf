import pygame
from card import *
from engine import *


def draw_rect_border(surface, x, y):
    for i in range(4):
        pygame.draw.rect(surface, red, (x - i, y - i, card_size[0], card_size[1]), 1)


def exchange_button_behavior(mouse):
    # if mouse is hovered on a button it changes to lighter shade
    exchange_button_x = exchange_button_rect.x
    exchange_button_y = exchange_button_rect.y
    if exchange_button_x <= mouse[0] <= exchange_button_x + 140 and exchange_button_y <= mouse[1] <= exchange_button_y + 40:
        pygame.draw.rect(screen, color_light, exchange_button_rect)
    else:
        pygame.draw.rect(screen, color_dark, exchange_button_rect)

    # superimposing the text onto our button
    screen.blit(exchange_button_text, (exchange_button_x, exchange_button_y))


def pass_button_behavior(mouse):
    # pass_button_x = 782
    # pass_button_y = 83
    pass_button_x = pass_button_rect.x
    pass_button_y = pass_button_rect.y
    if pass_button_x <= mouse[0] <= pass_button_x + 140 and pass_button_y <= mouse[1] <= pass_button_y + 40:
        pygame.draw.rect(screen, color_light, pass_button_rect)
    else:
        pygame.draw.rect(screen, color_dark, pass_button_rect)

    screen.blit(pass_button_text, (pass_button_x, pass_button_y))


def get_number_of_flipped_cards(hand):
    # Take in a hand and return the number of cards that are flipped
    flipped_cards = 0
    for card in hand:
        if card._face:
            flipped_cards += 1

    return flipped_cards


def user_wants_exchange():
    # return True if the user clicked the exchange button
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = pygame.mouse.get_pos()
        exchange_click = exchange_button_rect.collidepoint(mouse_pos)
        if exchange_click == 1:
            return True

    return False


def player_turn(rects_click):
    ###
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
    ###
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_down_pos = pygame.mouse.get_pos()
        for count, rect in enumerate(rects_click):
            player_click = rect.collidepoint(mouse_down_pos)
            if player_click == 1:
                if count == 0:
                    # Player clicked on pile_down
                    if golf.draw_count < 1:
                        golf.pile_up.add(golf.pile_down.deal_card())
                        golf.draw_card_on_turn()
                        golf.show_pass_button()
                elif count == 1:
                    # Player clicked on pile_up
                    golf.pile_up.select_pile_up_card()
                else:
                    # Player clicked on one of the 6 hand cards
                    # If the card is face down, select it (border is added)
                    # On a second click, flip it on click and end turn
                    selected_card = golf.current_player.hand[count - 2]

                    if not golf.current_player.selected_card:
                        golf.current_player.select_card_in_hand(selected_card)
                    else:
                        selected_card.flip_card()
                        golf.end_turn()

    # If a face up card from the hand is selected and the pile_up card is selected, the player may want to
    # make an exchange. Prompt them and offer an exchange button
    if golf.pile_up.is_selected() and golf.current_player.get_selected_card():
        exchange_button_behavior(mouse_position)
        if user_wants_exchange():
            # Swap the pile_up card with the player's selected card
            # then end the turn
            pile_up_card = golf.pile_up.get_top_card()
            players_selected_card = golf.current_player.get_selected_card()
            golf.exchange_hand_card_with_pile_up_card(players_selected_card, pile_up_card)

            golf.end_turn()

    if golf.option_to_pass:
        pass_button_behavior(mouse_position)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player_click_pass = pass_button_rect.collidepoint(mouse_position)
            if player_click_pass == 1:
                golf.end_turn()


# game init
pygame.init()
width = 1920
height = 1080
bounds = (width, height)
screen = pygame.display.set_mode(bounds)
pygame.display.set_caption("Golf")

# For debugging
DEBUG_MODE = False

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
pass_button_text = smallfont.render("Pass", True, white)

# rects
title_rect = title_text.get_rect()
title_rect.center = (width // 2, 50)
exchange_button_rect = exchange_button_text.get_rect(center=(950, 100))
pass_button_rect = pass_button_text.get_rect(center=(800, 100))

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

for card, position in zip(golf.player2.hand, player2_card_positions):
    card_rect = card._image.get_rect()
    card_rect.center = position
    card_rect.w, card_rect.h = card_size
    p2_rects.append(card_rect)

pile_down_rect = card_back.get_rect()
pile_down_rect.center = (1300, 680)
pile_down_rect.w, pile_down_rect.h = card_size

# Initial draw card
pile_up_rect = golf.pile_up.get_top_card()._image.get_rect()
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
    screen.blit(pygame.transform.scale(golf.pile_up.get_top_card()._image, card_size), pile_up_rect)

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position_down = pygame.mouse.get_pos()
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

            possible_rects_to_click = [pile_down_rect, pile_up_rect]

            if golf.current_player.name == "Player 1":
                possible_rects_to_click += p1_rects
            else:
                possible_rects_to_click += p2_rects

            player_turn(possible_rects_to_click)

            # Adding borders to selected cards
            for card, rect in zip(golf.current_player.hand, possible_rects_to_click[2:]):
                if card == golf.current_player.get_selected_card():
                    draw_rect_border(screen, rect.x, rect.y)
            if golf.pile_up.is_selected():
                draw_rect_border(screen, pile_up_rect.x, pile_up_rect.y)

        # last round
        elif golf.state.value == 2:
            current_player_text = font.render(f"Last round: {golf.current_player.name}", True, green, blue)
            screen.blit(current_player_text, (950, 140))

            possible_rects_to_click = [pile_down_rect, pile_up_rect]

            if golf.current_player.name == "Player 1":
                possible_rects_to_click += p1_rects
            else:
                possible_rects_to_click += p2_rects

            player_turn(possible_rects_to_click)

            # Adding borders to selected cards
            for card, rect in zip(golf.current_player.hand, possible_rects_to_click[2:]):
                if card == golf.current_player.get_selected_card():
                    draw_rect_border(screen, rect.x, rect.y)
            if golf.pile_up.is_selected():
                draw_rect_border(screen, pile_up_rect.x, pile_up_rect.y)

        # Game over man
        elif golf.state.value == 3:
            current_player_text = font.render(f"Game over, man!", True, green, blue)
            screen.blit(current_player_text, (950, 140))

            # Displays the final player score
            p1_score = font.render(f"Score: {golf.player1.calculate_score(golf.player1.hand)}", True, green, blue)
            screen.blit(p1_score, (200, 1040))
            p2_score = font.render(f"Score: {golf.player2.calculate_score(golf.player2.hand)}", True, green, blue)
            screen.blit(p2_score, (1550, 1040))

    ###### end Game logic ######

        if DEBUG_MODE:
            mouse_position = pygame.mouse.get_pos()
            mouse_pos_text = font.render(f"Mouse Pos: {str(mouse_position)}", True, green, blue)
            screen.blit(mouse_pos_text, (600, 670))
            p1_hand_text = font.render(f"P1 Hand: {str(golf.player1.hand)}", True, green, blue)
            screen.blit(p1_hand_text, (230, 900))
            p2_hand_text = font.render(f"P2 Hand: {str(golf.player2.hand)}", True, green, blue)
            screen.blit(p2_hand_text, (230, 930))
            pile_down_sneak = font.render(f"Next few pile_down card: {str(golf.pile_down.cards[0:3])}", True, green, blue)
            screen.blit(pile_down_sneak, (230, 960))
            pile_down_count = font.render(f"Cards in pile_down: {str(golf.pile_down.length())}", True, green, blue)
            screen.blit(pile_down_count, (600, 700))
            pile_up_count = font.render(f"Cards in pile_up: {str(golf.pile_up.length())}", True, green, blue)
            screen.blit(pile_up_count, (600, 730))
            golf_draw_count = font.render(f"golf.draw_count: {golf.draw_count}", True, green, blue)
            screen.blit(golf_draw_count, (600, 760))
            pile_up_list = font.render(f"golf.pile_up.hand: {golf.pile_up.cards[:3]}", True, green, blue)
            screen.blit(pile_up_list, (600, 790))
            current_player_get_selected = font.render(f"get_selected_card: {golf.current_player.get_selected_card()}", True, green, blue)
            screen.blit(current_player_get_selected, (600, 820))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click_prompt = font.render(f"Clickity {event.pos}", True, green, blue)
                    screen.blit(mouse_click_prompt, (1, 1))

        pygame.display.flip()

pygame.quit()
