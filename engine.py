import pygame
from card import *
from enum import Enum

# Some pygame element definitions
pygame.init()
pygame.display.set_caption("Golf")
width = 1920
height = 1080
bounds = (width, height)
screen = pygame.display.set_mode(bounds)

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
restart_button_text = smallfont.render("Play again?", True, green, blue)

# rects
title_rect = title_text.get_rect()
title_rect.center = (width // 2, 50)
exchange_button_rect = exchange_button_text.get_rect(center=(950, 100))
pass_button_rect = pass_button_text.get_rect(center=(800, 100))
restart_button_rect = restart_button_text.get_rect(center=(950, 200))

# card stuff
card_back = pygame.image.load('images/BACK.png')
card_size = (166, 232)

# player hand positions
player1_card_positions = ((200, 200), (400, 200), (200, 500), (400, 500), (200, 800), (400, 800))
player2_card_positions = ((1520, 200), (1720, 200), (1520, 500), (1720, 500), (1520, 800), (1720, 800))


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
        if self.state == GameState.LASTROUND:
            self.end_game()
        else:
            self.last_round_check()
        self.switch_player()
        self.pile_up.select_pile_up_card()
        self.draw_count = 0
        self.pile_up.selected = False
        self.player1.unselect_all_cards()
        self.player2.unselect_all_cards()
        self.option_to_pass = False

    def last_round_check(self):
        if self.current_player.has_all_cards_face_up():
            self.state = GameState.LASTROUND

    def end_game(self):
        self.state = GameState.ENDED
        self.current_player.flip_over_all_cards()

    def show_pass_button(self):
        self.option_to_pass = True

    def player_turn(self, rects_click, event):
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
        mouse_down_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for count, rect in enumerate(rects_click):
                player_click = rect.collidepoint(mouse_down_pos)
                if player_click == 1:
                    if count == 0:
                        # Player clicked on pile_down
                        if self.draw_count < 1:
                            self.pile_up.add(self.pile_down.deal_card())
                            self.draw_card_on_turn()
                            self.show_pass_button()
                    elif count == 1:
                        # Player clicked on pile_up
                        self.pile_up.select_pile_up_card()
                    else:
                        # Player clicked on one of the 6 hand cards
                        # If draw_count = 1, clicking on any card selects it
                        # If draw_count = 0 and player clicks on a face down card not previously selected,
                        #   the clicked face down card is selected
                        # If draw_count = 0 and player clicks on a face down card previously selected,
                        #   the clicked face down card is flipped and the turn is over
                        # else if any card is clicked, make it the selected card
                        clicked_card = self.current_player.hand[count - 2]
                        currently_selected_card = self.current_player.selected_card
                        if self.draw_count == 1:
                            self.current_player.select_card_in_hand(clicked_card)
                        elif self.draw_count == 0 and not clicked_card.is_face_up and clicked_card != currently_selected_card:
                            self.current_player.select_card_in_hand(clicked_card)
                        elif self.draw_count == 0 and not clicked_card.is_face_up and clicked_card == currently_selected_card:
                            clicked_card.flip_card()
                            self.end_turn()
                        else:
                            self.current_player.select_card_in_hand(clicked_card)

        # If a face up card from the hand is selected and the pile_up card is selected, the player may want to
        # make an exchange. Prompt them and offer an exchange button
        if self.pile_up.is_selected() and self.current_player.get_selected_card():
            self.exchange_button_behavior(mouse_down_pos)
            if self.user_wants_exchange(event):
                # Swap the pile_up card with the player's selected card
                # then end the turn
                pile_up_card = self.pile_up.get_top_card()
                players_selected_card = self.current_player.get_selected_card()
                self.exchange_hand_card_with_pile_up_card(players_selected_card, pile_up_card)

                self.end_turn()

        if self.option_to_pass:
            self.pass_button_behavior(mouse_down_pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player_click_pass = pass_button_rect.collidepoint(mouse_down_pos)
                if player_click_pass == 1:
                    self.end_turn()

    def user_wants_exchange(self, event):
        # return True if the user clicked the exchange button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            exchange_click = exchange_button_rect.collidepoint(mouse_pos)
            if exchange_click == 1:
                return True

        return False

    def exchange_button_behavior(self, mouse):
        # if mouse is hovered on a button it changes to lighter shade
        exchange_button_x = exchange_button_rect.x
        exchange_button_y = exchange_button_rect.y
        if exchange_button_x <= mouse[0] <= exchange_button_x + 140 and exchange_button_y <= mouse[
            1] <= exchange_button_y + 40:
            pygame.draw.rect(screen, color_light, exchange_button_rect)
        else:
            pygame.draw.rect(screen, color_dark, exchange_button_rect)

        # superimposing the text onto our button
        screen.blit(exchange_button_text, (exchange_button_x, exchange_button_y))

    def pass_button_behavior(self, mouse):
        pass_button_x = pass_button_rect.x
        pass_button_y = pass_button_rect.y
        if pass_button_x <= mouse[0] <= pass_button_x + 100 and pass_button_y <= mouse[1] <= pass_button_y + 40:
            pygame.draw.rect(screen, color_light, pass_button_rect)
        else:
            pygame.draw.rect(screen, color_dark, pass_button_rect)

        screen.blit(pass_button_text, (pass_button_x, pass_button_y))

    def restart_button_behavior(self, mouse, event):
        restart = False
        pygame.draw.rect(screen, blue, restart_button_rect)
        screen.blit(restart_button_text, (restart_button_rect.x, restart_button_rect.y))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player_click_restart = restart_button_rect.collidepoint(mouse)
            if player_click_restart == 1:
                restart = True

        return restart

    def draw_rect_border(self, surface, x, y):
        for i in range(4):
            pygame.draw.rect(surface, red, (x - i, y - i, card_size[0], card_size[1]), 1)
