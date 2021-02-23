# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

AVAILABLE_SYMBOLS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '-', 'X', 'x', '/')
POINTS = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '/': 15,
    '-': 0,
    'x': 20,
    'X': 20,
}


class Bowling:
    """
    Class that get bowling game result and count points of it according to rules that user want to use.
    The game contains 10 frames, each frame has a maximum of two throws.
    """
    _state = None
    _game_state = None

    def __init__(self, result, local_rules=True):
        """
        :param result: bowling game result
        :param local_rules: counting result rules: local(True) or tournament(False)
        """
        self.game_result_to_check = result
        self.game_result = []
        self.total_result = 0
        self.frame_result = 0
        self.frames_counter = 0
        self.bonus = 0
        self.spare_points = 0
        self.symbol = None
        self.after_strike_first = False
        self.after_strike_second = False
        self.after_spare = False
        if local_rules:
            self.game_state(LocalGame())
            self.change_state(FirstState())
        else:
            self.game_state(ChampGame())
            self.change_state(NewRulesFirst())
        for symbol in self.game_result_to_check:
            self.game_result.append(symbol)

    def game_state(self, game_state):
        """ Changing counting rules"""
        self._game_state = game_state
        self._game_state.game_context = self

    def change_state(self, state):
        """ Changing throw states"""
        self._state = state
        self._state.context = self

    def check_result(self):
        """ Checking if user input is correct"""
        try:
            for symbol in self.game_result:
                if symbol not in AVAILABLE_SYMBOLS:
                    raise ValueError(f'Symbol {symbol} is not available')
            if len(self.game_result) < 10 or len(self.game_result) > 20:
                raise ValueError(f'Incorrect amount of symbols, expected from 10 to 20,'
                                 f' got {len(self.game_result)}')
        except ValueError as err:
            print(f'{err}')
        else:
            try:
                self._game_state.run()
                if self.frames_counter != 10:
                    raise ValueError(
                        f'The game should have 10 frames, there is only {self.frames_counter}')
            except ValueError as err:
                print(f'{err}')
            except AttributeError as err:
                print(f'{err}')

    def print_result(self):
        print(f'Point for game score {self.game_result_to_check} is {self.total_result}')

    """ Methods to plug in counting methods"""
    def regular_throw(self):
        self._state.regular_throw()

    def strike(self):
        self._state.strike()

    def spare(self):
        self._state.spare()

    def game_mode(self):
        self._game_state.run()


class State(ABC):
    """
    Abstract class for choosing throw states.
    Each frame of game has a maximum of 2 throws.
    Each throw can be described with 2 states: first throw and second throw.
    """

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abstractmethod
    def regular_throw(self):
        pass

    @abstractmethod
    def strike(self):
        pass

    @abstractmethod
    def spare(self):
        pass


class FirstState(State):
    """
    Class describes a behaviour of first throw with local game rules.
    """

    def regular_throw(self):
        self.context.frames_counter += 1
        self.context.frame_result += POINTS[self.context.symbol]
        self.context.change_state(SecondState())

    def strike(self):
        self.context.frames_counter += 1
        self.context.frame_result += 20
        self.context.total_result += self.context.frame_result
        self.context.frame_result = 0

    def spare(self):
        raise AttributeError("First throw can't be spare")


class SecondState(State):
    """
    Class describes a behaviour of second throw with local game rules.
    """

    def regular_throw(self):
        self.context.frame_result += POINTS[self.context.symbol]
        if self.context.frame_result > 10:
            raise ValueError("Frame result can't be more than 10 if it is not strike/spare")
        self.context.total_result += self.context.frame_result
        self.context.frame_result = 0
        self.context.change_state(FirstState())

    def strike(self):
        raise AttributeError("Second throw can't be strike")

    def spare(self):
        self.context.frame_result = 15
        self.context.total_result += self.context.frame_result
        self.context.frame_result = 0
        self.context.change_state(FirstState())


class NewRulesFirst(State):
    """
    Class describes a behaviour of second throw with tournament game rules.
    """

    def regular_throw(self):
        self.context.frames_counter += 1
        self.context.frame_result += POINTS[self.context.symbol]
        if self.context.after_strike_second:
            self.context.bonus += POINTS[self.context.symbol]
            self.context.after_strike_second = False
        if self.context.after_strike_first:
            self.context.bonus += POINTS[self.context.symbol]
            self.context.after_strike_first = False
            self.context.after_strike_second = True
        if self.context.after_spare:
            self.context.bonus += POINTS[self.context.symbol]
            self.context.after_spare = False
        self.context.change_state(NewRulesSecond())

    def strike(self):
        self.context.frames_counter += 1
        self.context.frame_result += 10
        self.context.total_result += self.context.frame_result
        if self.context.after_strike_second:
            self.context.bonus += 10
            self.context.after_strike_second = False
        if self.context.after_strike_first:
            self.context.bonus += 10
            self.context.after_strike_first = False
            self.context.after_strike_second = True
        if self.context.after_spare:
            self.context.bonus += 10
            self.context.after_spare = False
        self.context.after_strike_first = True
        self.context.frame_result = 0

    def spare(self):
        raise AttributeError("First throw can't be spare")


class NewRulesSecond(State):
    """
    Class describes a behaviour of second throw with tournament game rules.
    """

    def regular_throw(self):
        self.context.frame_result += POINTS[self.context.symbol]
        self.context.total_result += self.context.frame_result
        if self.context.after_strike_second:
            self.context.bonus += POINTS[self.context.symbol]
            self.context.after_strike_second = False
        self.context.frame_result = 0
        self.context.change_state(NewRulesFirst())

    def strike(self):
        raise AttributeError("Second throw can't be strike")

    def spare(self):
        self.context.spare_points = 10 - self.context.frame_result
        self.context.frame_result = 10
        self.context.total_result += self.context.frame_result
        if self.context.after_strike_second:
            self.context.bonus += self.context.spare_points
            self.context.after_strike_second = False
        self.context.frame_result = 0
        self.context.after_spare = True
        self.context.change_state(NewRulesFirst())


class GameState(ABC):
    """
    Abstract class for choosing game mode: local or tournament
    """

    @property
    def game_context(self):
        return self._game_context

    @game_context.setter
    def game_context(self, game_context):
        self._game_context = game_context

    @abstractmethod
    def run(self):
        pass


class LocalGame(GameState):
    """
    Class that counts points of bowling game using local rules
    Rules: «Х» – strike always 20 points, «4/» - spare always 15 points, «34» – sum 3+4=7, «-4» - sum 0+4=4
    Example: '1/X3-5/X8154-57/X' - 15 + 20 + 3 + 15 + 20 + 9 + 9 + 5 + 15 + 20 = 131
    """

    def run(self):

        for sym in self.game_context.game_result:
            self.game_context.symbol = sym
            if self.game_context.symbol == '/':
                self.game_context._state.spare()
            elif self.game_context.symbol == 'x' or self.game_context.symbol == 'X':
                self.game_context._state.strike()
            else:
                self.game_context._state.regular_throw()


class ChampGame(GameState):
    """
    Class that counts points of bowling game using tournament rules
    Rules:
    if there was strike frame points equals to number of pins knocked down this frame + pins knocked in next two throws,
    if there was spare points equals to number of pins knocked down this frame + pins knocked in next one throws,
    if there was strike/spare in the last frame, points equals to number of pins knocked down this frame + 10
    Example: (10 + 10) + (10 + 3) + 3 + (10 + 10) + (10 + 9) + 9 + 9 + 5 + (10 + 10) + (10 + 10) = 138
    """

    def run(self):
        for sym in self.game_context.game_result:
            self.game_context.symbol = sym
            if self.game_context.symbol == '/':
                self.game_context._state.spare()
            elif self.game_context.symbol == 'x' or self.game_context.symbol == 'X':
                self.game_context._state.strike()
            else:
                self.game_context._state.regular_throw()
        if self.game_context.after_strike_second:
            self.game_context.bonus += 10
            self.game_context.after_strike_second = False
        if self.game_context.after_strike_first:
            self.game_context.bonus += 10
            self.game_context.after_strike_first = False
        if self.game_context.after_spare:
            self.game_context.bonus += 10
            self.game_context.after_spare = False
        self.game_context.total_result += self.game_context.bonus


if __name__ == '__main__':
    check = '1/X3-5/X8154-57/X'
    bw_check = Bowling(check, local_rules=False)
    bw_check.check_result()
    bw_check.print_result()
