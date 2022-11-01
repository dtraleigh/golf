import unittest

from card import *


class TestScore(unittest.TestCase):
    # verify that these hand combinations generate the correct score
    def test_scores_scenario1(self):
        deck = Deck()
        player = Player("Golf Tester")
        hand = [deck.get_specific_card_from_deck("DIAMOND", 1),
                deck.get_specific_card_from_deck("JOKER2", 14),
                deck.get_specific_card_from_deck("SPADE", 13),
                deck.get_specific_card_from_deck("HEART", 4),
                deck.get_specific_card_from_deck("JOKER1", 14),
                deck.get_specific_card_from_deck("HEART", 3)]
        self.assertEqual(player.calculate_score(hand), 4)

    def test_scores_scenario2(self):
        deck = Deck()
        player = Player("Golf Tester")
        hand = [deck.get_specific_card_from_deck("DIAMOND", 2),
                deck.get_specific_card_from_deck("HEART", 3),
                deck.get_specific_card_from_deck("SPADE", 4),
                deck.get_specific_card_from_deck("HEART", 5),
                deck.get_specific_card_from_deck("SPADE", 8),
                deck.get_specific_card_from_deck("HEART", 6)]
        self.assertEqual(player.calculate_score(hand), 28)

    def test_scores_scenario3(self):
        deck = Deck()
        player = Player("Golf Tester")
        hand = [deck.get_specific_card_from_deck("DIAMOND", 2),
                deck.get_specific_card_from_deck("HEART", 2),
                deck.get_specific_card_from_deck("SPADE", 4),
                deck.get_specific_card_from_deck("HEART", 4),
                deck.get_specific_card_from_deck("SPADE", 8),
                deck.get_specific_card_from_deck("HEART", 8)]
        self.assertEqual(player.calculate_score(hand), 0)


if __name__ == '__main__':
    unittest.main()
