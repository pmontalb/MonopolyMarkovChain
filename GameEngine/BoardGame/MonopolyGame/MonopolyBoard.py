from GameEngine.BoardGame.Board import BoardItem, BoardItemInput, Board, BoardInput
from GameEngine.GameUtility.Dice import Dice
from GameEngine.CardUtility.CardCollection import Deck, DeckInput, Card, CardInput
from Utility.Logger import Logger, LogLevel
from enum import Enum

MAX_TURN_IN_PRISON = 3
MONEY_FROM_GO = 200
MAX_DOUBLE_COUNT = 3


class Group(Enum):
    Brown = 0
    Blue = 1
    Pink = 3
    Orange = 4
    Red = 5
    Yellow = 6
    Green = 7
    Purple = 8
    Airport = 9
    EuropeanBuilding = 10
    Tax = 11
    DrawChance = 12
    DrawCommunityChest = 13
    Go = 14
    Prison = 15
    Parking = 16
    GoToPrison = 17


class MonopolyCardInput(CardInput):
    def __init__(self,
                 card_id="UnknownMonopolyCard",
                 go_to=None,
                 pos_shift=0,
                 capital_change=0):
        super(MonopolyCardInput, self).__init__(card_id)

        self.go_to = go_to

        if go_to is not None and pos_shift != 0:
            raise ValueError("Unexpected input")
        self.pos_shift = pos_shift

        if go_to is not None and capital_change != 0:
            raise ValueError("Unexpected input")
        if pos_shift != 0 and capital_change != 0:
            raise ValueError("Unexpected input")
        self.capital_change = capital_change

        self.leave_prison = "leave prison" in card_id.lower()

    @property
    def description(self):
        return self.card_id


class MonopolyCard(Card):
    def __init__(self, card_input):
        super(MonopolyCard, self).__init__(card_input)

    def __repr__(self):
        return "Card[{} | go({}) | ps({}) | $({}) | lp({})]".format(self.card_input.card_id,
                                                                    self.go_to,
                                                                    self.pos_shift,
                                                                    self.capital_change,
                                                                    self.leave_prison)

    @property
    def go_to(self):
        return self.card_input.go_to

    @property
    def pos_shift(self):
        return self.card_input.pos_shift

    @property
    def capital_change(self):
        return self.card_input.capital_change

    @property
    def leave_prison(self):
        return self.card_input.leave_prison


class MonopolyBoardItemInput(BoardItemInput):
    def __init__(self,
                 name="UnknownName",
                 buy_cost=None,
                 group=None,
                 passage_cost=None):
        super(MonopolyBoardItemInput, self).__init__(name)

        self.buy_cost = buy_cost
        self.group = group
        self.passage_cost = passage_cost

    @property
    def name(self):
        return self.item_id


class MonopolyBoardItem(BoardItem):
    def __init__(self, board_item_input):
        super(MonopolyBoardItem, self).__init__(board_item_input)
        self.own_by = None

    @property
    def buy_cost(self):
        return self.board_item_input.buy_cost

    @property
    def passage_cost(self):
        return self.board_item_input.passage_cost

    @property
    def group(self):
        return self.board_item_input.group

    def __repr__(self):
        return "BoardItem[{} | cost(b={} p={}) | {}]".format(self.board_item_input.item_id,
                                                             self.buy_cost,
                                                             self.passage_cost,
                                                             self.group)


class MonopolyBoardInput(BoardInput):
    def __init__(self, log_name="master", log_level=LogLevel.DEBUG):
        # the board is seen as a column vector of 40 cells
        super(MonopolyBoardInput, self).__init__("MonopolyBoard", 40, 1, log_name, log_level)


class MonopolyBoard(Board):
    def __init__(self, board_input):
        super(MonopolyBoard, self).__init__(board_input)
        self.dice = Dice()

        self.community_chest = Deck(DeckInput("Community Chest", board_input.log_name, board_input.log_level))
        self.__make_community_chest_deck()
        self.community_chest.shuffle()

        self.chance = Deck(DeckInput("Chance", board_input.log_name, board_input.log_level))
        self.__make_chance_deck()
        self.chance.shuffle()

    @property
    def go_position(self):
        return 0

    @property
    def prison_position(self):
        return 10

    def __append_board_item(self, board_item_input):
        item = MonopolyBoardItem(board_item_input)
        self._logger("{}: #{} Added {}".format(self, len(self._table), item), log_level=LogLevel.TEST)
        self._table.append(item)

    def _make_board(self):
        self.__append_board_item(MonopolyBoardItemInput("Go", None, Group.Go, -200))  # 0

        self.__append_board_item(MonopolyBoardItemInput("Vilnius", 60, Group.Brown))  # 1
        self.__append_board_item(MonopolyBoardItemInput("Community Chest", group=Group.DrawCommunityChest))  # 2
        self.__append_board_item(MonopolyBoardItemInput("Riga", 60, Group.Brown))  # 3

        self.__append_board_item(MonopolyBoardItemInput("Income Tax", None, Group.Tax, 200))  # 4
        self.__append_board_item(MonopolyBoardItemInput("Amsterdam Airport", 200, Group.Airport))  # 5

        self.__append_board_item(MonopolyBoardItemInput("Sofia", 100, Group.Blue))  # 6
        self.__append_board_item(MonopolyBoardItemInput("Chance", group=Group.DrawChance))  # 7
        self.__append_board_item(MonopolyBoardItemInput("Bucharest", 100, Group.Blue))  # 8
        self.__append_board_item(MonopolyBoardItemInput("Warsaw", 120, Group.Blue))  # 9

        self.__append_board_item(MonopolyBoardItemInput("Prison", group=Group.Prison))  # 10

        self.__append_board_item(MonopolyBoardItemInput("Budapest", 140, Group.Pink))  # 11
        self.__append_board_item(MonopolyBoardItemInput("European Parliament", 150, Group.EuropeanBuilding))  # 12
        self.__append_board_item(MonopolyBoardItemInput("Ginevra", 140, Group.Pink))  # 13
        self.__append_board_item(MonopolyBoardItemInput("Helsinki", 160, Group.Pink))  # 14

        self.__append_board_item(MonopolyBoardItemInput("Frankfurt Airport", 200, Group.Airport))  # 15

        self.__append_board_item(MonopolyBoardItemInput("Stockholm", 180, Group.Orange))  # 16
        self.__append_board_item(MonopolyBoardItemInput("Community Chest", group=Group.DrawCommunityChest))  # 17
        self.__append_board_item(MonopolyBoardItemInput("Vienna", 180, Group.Orange))  # 18
        self.__append_board_item(MonopolyBoardItemInput("Lisbon", 200, Group.Orange))  # 19

        self.__append_board_item(MonopolyBoardItemInput("Parking", group=Group.Parking))  # 20

        self.__append_board_item(MonopolyBoardItemInput("Madrid", 200, Group.Red))  # 21
        self.__append_board_item(MonopolyBoardItemInput("Chance", group=Group.DrawChance))  # 22
        self.__append_board_item(MonopolyBoardItemInput("Athene", 220, Group.Red))  # 23
        self.__append_board_item(MonopolyBoardItemInput("Dublin", 220, Group.Red))  # 24

        self.__append_board_item(MonopolyBoardItemInput("Paris Airport", 200, Group.Airport))  # 25

        self.__append_board_item(MonopolyBoardItemInput("Copenhagen", 240, Group.Yellow))  # 26
        self.__append_board_item(MonopolyBoardItemInput("London", 260, Group.Yellow))  # 27
        self.__append_board_item(MonopolyBoardItemInput("Palace of Justice", 150, Group.EuropeanBuilding))  # 28
        self.__append_board_item(MonopolyBoardItemInput("Luxemburg", 280, Group.Yellow))  # 29

        self.__append_board_item(MonopolyBoardItemInput("Go To Prison", group=Group.GoToPrison))  # 30

        self.__append_board_item(MonopolyBoardItemInput("Brussels", 300, Group.Green))  # 31
        self.__append_board_item(MonopolyBoardItemInput("Amsterdam", 300, Group.Green))  # 32
        self.__append_board_item(MonopolyBoardItemInput("Community Chest", group=Group.DrawCommunityChest))  # 33
        self.__append_board_item(MonopolyBoardItemInput("Rome", 320, Group.Green))  # 34

        self.__append_board_item(MonopolyBoardItemInput("London Airport", 200, Group.Airport))  # 35
        self.__append_board_item(MonopolyBoardItemInput("Chance", group=Group.DrawChance))  # 36

        self.__append_board_item(MonopolyBoardItemInput("Berlin", 350, Group.Purple))  # 37
        self.__append_board_item(MonopolyBoardItemInput("Super Tax", None, Group.Tax, 100))  # 38
        self.__append_board_item(MonopolyBoardItemInput("Paris", 400, Group.Purple))  # 39

    def __make_community_chest_deck(self):
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC1", self.go_position, 0, 0)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC2", None, 0, 200)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC3", None, 0, -50)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC4", None, 0, 50)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("Leave Prison 1", None, 0, 0)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC5", self.prison_position, 0, 0)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC6", None, 0, 50)))  # TODO: 50 * n_players
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC7", None, 0, 100)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC8", None, 0, 20)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC9", None, 0, 10)))  # TODO: 10 * n_players
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC10", None, 0, 100)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC11", None, 0, -150)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC12", None, 0, 25)))
        self.community_chest.push_back(
            MonopolyCard(MonopolyCardInput("CC13", None, 0, -40)))  # TODO: 40x houses, 115x hotels
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC14", None, 0, 10)))
        self.community_chest.push_back(MonopolyCard(MonopolyCardInput("CC15", None, 0, 100)))

    def __make_chance_deck(self):
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CH1", self.go_position, 0, 0)))
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CH2", 24, 0, 0)))  # Go to Dublin
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CH3", 11, 0, 0)))  # Go to Budapest
        # self.chance.push_back(MonopolyCard(MonopolyCardInput("CH4", None, 0, 0)))
        # self.chance.push_back(MonopolyCard(MonopolyCardInput("CH5", None, 0, 0)))
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CH6", None, 0, 50)))
        self.chance.push_back(MonopolyCard(MonopolyCardInput("Leave Prison 2", None, 0, 0)))
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CH7", None, -3, 0)))
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CC9", None, self.prison_position, 0)))
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CC10", None, 0, -25)))  # TODO: 25x houses, 100x hotels
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CC11", None, 0, -15)))
        # self.chance.push_back(MonopolyCard(MonopolyCardInput("CC12", None, 0, 0)))
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CC13", 39, 0, 0)))  # Go to Paris
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CC14", None, 0, -50)))  # TODO: 50 * n_players
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CC15", None, 0, 150)))
        self.chance.push_back(MonopolyCard(MonopolyCardInput("CC16", None, 0, 100)))

    def advance(self, player):
        if player.position == self.prison_position:
            if player.turns_in_prison == MAX_TURN_IN_PRISON:
                #self._logger("{} leaves prison".format(player), log_level=LogLevel.DEBUG)
                player.turns_in_prison = 0
            else:
                # if in prison, it cannot move for 3 turns
                player.turns_in_prison += 1
                #self._logger("{} remains in prison".format(player), log_level=LogLevel.DEBUG)
                return

        first_launch = self.dice.launch()
        second_launch = self.dice.launch()
        #self._logger("{} dice launch({} | {})".format(player, first_launch, second_launch), log_level=LogLevel.DEBUG)
        new_pos = player.position + first_launch + second_launch

        player.position = new_pos % self.n_rows  # table it's a ring buffer in this case
        if player.position == self.prison_position:
            player.turns_in_prison = MAX_TURN_IN_PRISON  # fudge for not writing extra piece of logic
        if new_pos > self.n_rows:
            # collect 200
            player.capital += MONEY_FROM_GO

        if player.double_count == MAX_DOUBLE_COUNT:
            #self._logger("{} goes to prison".format(player), log_level=LogLevel.DEBUG)
            player.position = self.prison_position
            player.turns_in_prison = 0
            player.double_count = 0
        else:
            #self._logger("{} goes to {}".format(player, self[player.position]), log_level=LogLevel.DEBUG)
            self.positional_trigger(player)

            if first_launch == second_launch:
                player.double_count += 1
                self.advance(player)

    def positional_trigger(self, player):
        cell = self[player.position]

        if cell.group == Group.GoToPrison:
            player.position = self.prison_position
            player.turns_in_prison = 0
            return

        if cell.group not in [Group.DrawChance, Group.DrawCommunityChest]:
            # deduct any passage cost (i.e. tax, property own by other players, etc.)
            try:
                # this is to be updated with all properties of the same group, houses and hotels
                player.capital -= cell.passage_cost
            except TypeError:
                pass

            # if own by someone, give this money to the player who owns it
            try:
                # if you are in prison you can't receive income!
                if (cell.own_by.position != self.prison_position or
                        (cell.own_by.position == self.prison_position and
                         cell.own_by.turns_in_prison < MAX_TURN_IN_PRISON)):
                    cell.own_by.capital += cell.passage_cost
            except (ValueError, AttributeError):
                pass
            return

        card = self.community_chest.draw() if cell.group == Group.DrawChance else self.chance.draw()
        if card.go_to is not None:
            pos = player.position
            player.position = card.go_to
            if pos > card.go_to != self.prison_position:
                player.capital += MONEY_FROM_GO
            return

        player.position = (player.position + card.pos_shift) % self.n_rows
        player.capital += card.capital_change
        player.leave_prison_tickets += card.leave_prison
