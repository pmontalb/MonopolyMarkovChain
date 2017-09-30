from random import shuffle
from Utility.Logger import Logger, LogLevel


class CardInput:
    def __init__(self, card_id="UnknownCard"):
        self.card_id = card_id


class Card:
    def __init__(self, card_input):
        self.card_input = card_input

    def __repr__(self):
        return "Card({})".format(self.card_input.card_id)


class DeckCard:
    def __init__(self, card, position_in_deck):
        self.card = card
        self.position = position_in_deck


class DeckInput:
    def __init__(self, deck_id="UnknownDeck", log_name="master", log_level=LogLevel.DEBUG):
        self.deck_id = deck_id
        self.log_name = log_name
        self.log_level = log_level


class Deck:
    def __init__(self, deck_input):
        self.deck_input = deck_input
        self._logger = Logger(deck_input.log_name, deck_input.log_level)
        self.__cards = []

    def __repr__(self):
        return "Deck({})".format(self.deck_input.deck_id)

    def push_back(self, deck_card):
        self._logger("{}: Added {}".format(self, deck_card), log_level=LogLevel.TEST)
        self.__cards.append(deck_card)

    def draw(self):
        # pop the first one
        ret = self.__cards.pop()
        self._logger("{}: Drawn {}".format(self, ret))

        # put it back at the end of the deck
        self.__cards.append(ret)

        return ret

    def shuffle(self):
        self._logger("{}: Shuffling".format(self))
        shuffle(self.__cards)