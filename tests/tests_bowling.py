# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock

import bowling as bw


class BowlingTest(unittest.TestCase):

    def setUp(self):
        self.game = bw.Bowling('1/X3-5/X8154-57/X')
        self.first_state = bw.FirstState
        self.second_state = bw.SecondState
        self.local_game = bw.LocalGame
        self.tournament_game = bw.ChampGame
        self.new_first_state = bw.NewRulesFirst
        self.new_second_state = bw.NewRulesSecond

    def test_change_state_first_second(self):
        self.game.symbol = '5'
        self.game.frames_counter = 3
        self.game.frame_result = 0

        self.game.change_state(self.first_state())
        self.game._state.regular_throw()

        self.assertEqual(self.game.frame_result, 5)
        self.assertEqual(self.game.frames_counter, 4)
        self.assertTrue(isinstance(self.game._state, self.second_state))

    def test_change_state_second_first(self):
        self.game.symbol = '4'
        self.game.frame_result = 5
        self.game.total_result = 14

        self.game.change_state(self.second_state())
        self.game._state.regular_throw()

        self.assertEqual(self.game.frame_result, 0)
        self.assertEqual(self.game.total_result, 23)
        self.assertTrue(isinstance(self.game._state, self.first_state))

    def test_strike(self):
        self.game.symbol = 'X'
        self.game.frames_counter = 3
        self.game.frame_result = 0
        self.game.total_result = 23

        self.game.change_state(self.first_state())
        self.game._state.strike()

        self.assertEqual(self.game.frames_counter, 4)
        self.assertEqual(self.game.frame_result, 0)
        self.assertEqual(self.game.total_result, 43)
        self.assertTrue(isinstance(self.game._state, self.first_state))

    def test_spare(self):
        self.game.symbol = '/'
        self.game.frame_result = 8
        self.game.total_result = 50

        self.game.change_state(self.second_state())
        self.game._state.spare()

        self.assertEqual(self.game.frame_result, 0)
        self.assertEqual(self.game.total_result, 65)
        self.assertTrue(isinstance(self.game._state, self.first_state))

    def test_new_rs_first_state(self):
        self.game.symbol = '4'
        self.game.total_result = 14
        self.game.frames_counter = 3
        self.game.bonus = 34
        self.game.after_strike_second = True
        self.game.after_strike_first = True
        self.game.after_spare = False

        self.game.game_state(self.tournament_game())
        self.game.change_state(self.new_first_state())
        self.game._state.regular_throw()

        self.assertEqual(self.game.frame_result, 4)
        self.assertEqual(self.game.total_result, 14)
        self.assertEqual(self.game.frames_counter, 4)
        self.assertEqual(self.game.bonus, 42)
        self.assertEqual(self.game.after_strike_first, False)
        self.assertEqual(self.game.after_strike_second, True)
        self.assertEqual(self.game.after_spare, False)
        self.assertTrue(isinstance(self.game._state, self.new_second_state))

    def test_new_rs_second_state(self):
        self.game.symbol = '5'
        self.game.frame_result = 3
        self.game.total_result = 14
        self.game.bonus = 16
        self.game.after_strike_second = True

        self.game.game_state(self.tournament_game())
        self.game.change_state(self.new_second_state())
        self.game._state.regular_throw()

        self.assertEqual(self.game.frame_result, 0)
        self.assertEqual(self.game.total_result, 22)
        self.assertEqual(self.game.bonus, 21)
        self.assertEqual(self.game.after_strike_second, False)
        self.assertTrue(isinstance(self.game._state, self.new_first_state))

    def test_new_spare(self):
        self.game.symbol = '/'
        self.game.frame_result = 8
        self.game.total_result = 50
        self.game.bonus = 13
        self.game.after_strike_second = True

        self.game.game_state(self.tournament_game())
        self.game.change_state(self.new_second_state())
        self.game._state.spare()

        self.assertEqual(self.game.frame_result, 0)
        self.assertEqual(self.game.total_result, 60)
        self.assertEqual(self.game.bonus, 15)
        self.assertEqual(self.game.after_strike_second, False)
        self.assertTrue(isinstance(self.game._state, self.new_first_state))

    def test_new_strike(self):
        self.game.symbol = 'X'
        self.game.frames_counter = 3
        self.game.frame_result = 0
        self.game.total_result = 23
        self.game.bonus = 54
        self.game.after_strike_first = True
        self.game.after_spare = True

        self.game.game_state(self.tournament_game())
        self.game.change_state(self.new_first_state())
        self.game._state.strike()

        self.assertEqual(self.game.frames_counter, 4)
        self.assertEqual(self.game.frame_result, 0)
        self.assertEqual(self.game.total_result, 33)
        self.assertEqual(self.game.bonus, 74)
        self.assertEqual(self.game.after_strike_second, True)
        self.assertEqual(self.game.after_strike_first, True)
        self.assertEqual(self.game.after_spare, False)
        self.assertTrue(isinstance(self.game._state, self.new_first_state))

    def test_game_state(self):
        self.assertTrue(isinstance(self.game._state, self.first_state))
        self.assertTrue(isinstance(self.game._game_state, self.local_game))

        self.game.game_state(self.tournament_game())

        self.assertTrue(isinstance(self.game._game_state, self.tournament_game))

    def test_check_result(self):
        self.game._game_state.run = Mock()

        self.game.check_result()

        self.game._game_state.run.assert_called_once()

    def test_local_run(self):  # 1/X3-5/X8154-57/X
        self.game._state.spare = Mock()
        self.game._state.strike = Mock()
        self.game._state.regular_throw = Mock()
        self.game.frames_counter = 10

        self.game.game_state(self.local_game())
        self.game._game_state.run()

        self.game._state.spare.assert_called()
        assert self.game._state.spare.call_count == 3
        self.game._state.strike.assert_called()
        assert self.game._state.spare.call_count == 3
        self.game._state.regular_throw.assert_called()
        assert self.game._state.regular_throw.call_count == 11

    def test_tournament_run(self):
        self.game._state.spare = Mock()
        self.game._state.strike = Mock()
        self.game._state.regular_throw = Mock()
        self.game.frames_counter = 10

        self.game.game_state(self.tournament_game())
        self.game._game_state.run()

        self.game._state.spare.assert_called()
        assert self.game._state.spare.call_count == 3
        self.game._state.strike.assert_called()
        assert self.game._state.spare.call_count == 3
        self.game._state.regular_throw.assert_called()
        assert self.game._state.regular_throw.call_count == 11

    def test_local_run_counting(self):
        new_game = bw.Bowling('X4/34')

        new_game.game_state(self.local_game())
        new_game._game_state.run()

        self.assertEqual(new_game.total_result, 42)

    def test_tournament_run_counting(self):
        new_game = bw.Bowling('X4/34', local_rules=False)

        new_game.game_state(self.tournament_game())
        new_game._game_state.run()

        self.assertEqual(new_game.total_result, 40)


if __name__ == '__main__':
    unittest.main()