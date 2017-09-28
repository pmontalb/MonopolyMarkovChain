from GameEngine.BoardGame.Board import BoardItem, BoardItemInput, Board, BoardInput
from GameEngine.GameUtility.Dice import Dice
from GameEngine.CardUtility.CardCollection import Deck, DeckInput, Card, CardInput
from enum import Enum


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
    def __init__(self, card_id="UnknownMonopolyCard", go_to=None, pos_shift=0, capital_change=0):
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
    def __init__(self, name="UnknownName", buy_cost=None, group=None, passage_cost=None):
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


class MonopolyBoardInput(BoardInput):
    def __init__(self):
        # the board is seen as a column vector of 40 cells
        super(MonopolyBoardInput, self).__init__(40, 1)


class MonopolyBoard(Board):
    def __init__(self, board_input):
        super(MonopolyBoard, self).__init__(board_input)
        self.dice = Dice()

        self.community_chest = Deck(DeckInput())
        self.__make_community_chest_deck()

        self.chance = Deck(DeckInput())
        self.__make_chance_deck()

    @property
    def go_position(self):
        return 0

    @property
    def prison_position(self):
        return 10

    def _make_board(self):
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Go", None, Group.Go, -200)))  # 0

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Vilnius", 60, Group.Brown)))  # 1
        self._table.append(
            MonopolyBoardItem(MonopolyBoardItemInput("Community Chest", group=Group.DrawCommunityChest)))  # 2
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Riga", 60, Group.Brown)))  # 3

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Income Tax", None, Group.Tax, 200)))  # 4
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Amsterdam Airport", 200, Group.Airport)))  # 5

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Sofia", 100, Group.Blue)))  # 6
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Chance", group=Group.DrawChance)))  # 7
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Bucharest", 100, Group.Blue)))  # 8
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Warsaw", 120, Group.Blue)))  # 9

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Prison", group=Group.Prison)))  # 10

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Budapest", 140, Group.Pink)))  # 11
        self._table.append(
            MonopolyBoardItem(MonopolyBoardItemInput("European Parliament", 150, Group.EuropeanBuilding)))  # 12
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Ginevra", 140, Group.Pink)))  # 13
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Helsinki", 160, Group.Pink)))  # 14

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Frankfurt Airport", 200, Group.Airport)))  # 15

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Stockholm", 180, Group.Orange)))  # 16
        self._table.append(
            MonopolyBoardItem(MonopolyBoardItemInput("Community Chest", group=Group.DrawCommunityChest)))  # 17
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Vienna", 180, Group.Orange)))  # 18
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Lisbon", 200, Group.Orange)))  # 19

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Parking", group=Group.Parking)))  # 20

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Madrid", 200, Group.Red)))  # 21
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Chance", group=Group.DrawChance)))  # 22
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Athene", 220, Group.Red)))  # 23
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Dublin", 220, Group.Red)))  # 24

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Paris Airport", 200, Group.Airport)))  # 25

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Copenhagen", 240, Group.Yellow)))  # 26
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("London", 260, Group.Yellow)))  # 27
        self._table.append(
            MonopolyBoardItem(MonopolyBoardItemInput("Palace of Justice", 150, Group.EuropeanBuilding)))  # 28
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Luxemburg", 280, Group.Yellow)))  # 29

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Go To Prison", group=Group.GoToPrison)))  # 30

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Brussels", 300, Group.Green)))  # 31
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Amsterdam", 300, Group.Green)))  # 32
        self._table.append(
            MonopolyBoardItem(MonopolyBoardItemInput("Community Chest", group=Group.DrawCommunityChest)))  # 33
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Rome", 320, Group.Green)))  # 34

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("London Airport", 200, Group.Airport)))  # 35
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Chance", group=Group.DrawChance)))  # 36

        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Berlin", 350, Group.Purple)))  # 37
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Super Tax", None, Group.Tax, 100)))  # 38
        self._table.append(MonopolyBoardItem(MonopolyBoardItemInput("Paris", 400, Group.Purple)))  # 39

    def __make_community_chest_deck(self):
        pass

    def __make_chance_deck(self):
        pass

    def advance(self, player):
        if player.position == self.prison_position:
            if player.turns_in_prison == 3:
                player.turns_in_prison = 0
            else:
                # if in prison, it cannot move for 3 turns
                player.turns_in_prison += 1
                return

        first_launch = self.dice.launch()
        second_launch = self.dice.launch()
        new_pos = player.position + first_launch + second_launch

        player.position = new_pos % self.n_rows  # table it's a ring buffer in this case

        if player.double_count == 3:
            player.position = self.prison_position
            player.turns_in_prison = 0
            player.double_count = 0
        else:
            while first_launch == second_launch:
                player.double_count += 1
                self.advance(player)

        self.positional_trigger(player)

    def positional_trigger(self, player):
        cell = self[player.position]

        if cell.group == Group.GoToPrison:
            player.position = self.prison_position
            player.turns_in_prison = 0
            return

        if cell.group not in [Group.DrawChance, Group.DrawCommunityChest]:
            return

        card = self.community_chest.draw() if cell.group == Group.DrawChance else self.chance.draw()
        if card.go_to is not None:
            player.position = card.go_to
            return

        player.position = (player.position + card.pos_shift) % self.n_rows
        player.money += card.capital_change
        player.leave_prison_tickets += card.leave_prison



