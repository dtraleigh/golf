import pygame
from card import *
from engine import *

# For debugging
DEBUG_MODE = False

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
            p1_num_flipped_cards = golf.player1.get_number_of_flipped_cards()
            p2_num_flipped_cards = golf.player2.get_number_of_flipped_cards()

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

            golf.player_turn(possible_rects_to_click, event)

            # Adding borders to selected cards
            for card, rect in zip(golf.current_player.hand, possible_rects_to_click[2:]):
                if card == golf.current_player.get_selected_card():
                    golf.draw_rect_border(screen, rect.x, rect.y)
            if golf.pile_up.is_selected():
                golf.draw_rect_border(screen, pile_up_rect.x, pile_up_rect.y)

        # last round
        elif golf.state.value == 2:
            current_player_text = font.render(f"Last round: {golf.current_player.name}", True, green, blue)
            screen.blit(current_player_text, (950, 140))

            possible_rects_to_click = [pile_down_rect, pile_up_rect]

            if golf.current_player.name == "Player 1":
                possible_rects_to_click += p1_rects
            else:
                possible_rects_to_click += p2_rects

            golf.player_turn(possible_rects_to_click, event)

            # Adding borders to selected cards
            for card, rect in zip(golf.current_player.hand, possible_rects_to_click[2:]):
                if card == golf.current_player.get_selected_card():
                    golf.draw_rect_border(screen, rect.x, rect.y)
            if golf.pile_up.is_selected():
                golf.draw_rect_border(screen, pile_up_rect.x, pile_up_rect.y)

        # Game over man
        elif golf.state.value == 3:
            current_player_text = font.render(f"Game over, man!", True, green, blue)
            screen.blit(current_player_text, (950, 140))

            restart_game = golf.restart_button_behavior(mouse_position, event)
            if restart_game:
                golf = GolfEngine()

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
