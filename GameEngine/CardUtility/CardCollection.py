from random import shuffle


class CardInput:
    def __init__(self, card_id="UnknownCard"):
        self.card_id = card_id


class Card:
    def __init__(self, card_input):
        self.card_input = card_input


class DeckCard:
    def __init__(self, card, position_in_deck):
        self.card = card
        self.position = position_in_deck


class DeckInput:
    def __init__(self):
        pass


class Deck:
    def __init__(self, deck_input):
        self.deck_input = deck_input
        self.__cards = []

    def push_back(self, deck_card):
        self.__cards.append(deck_card)

    def draw(self):
        # pop the first one
        ret = self.__cards.pop()

        # put it back at the end of the deck
        self.__cards.append(ret)

        return ret

    def shuffle(self):
        shuffle(self.__cards)