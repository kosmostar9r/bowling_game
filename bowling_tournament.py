# -*- coding: utf-8 -*-
import os
import bowling as bw


class BowlingTournament:
    """
    Class for processing data get from tournament file. File contains players and their game result.
    Class returns file contains player name, game result, game points and also can make tournament table.
    """

    def __init__(self, input_file, output_file='tournament_result.txt', make_table=False, local_rules=True):
        """
        :param input_file: file with game results
        :param output_file: file where to write down results
        :param make_table: optional param, if it needs to write down tournament table in console
        :param local_rules: which rules use for counting results
        """
        self.input_file = os.path.normpath(input_file)
        self.output_file = os.path.normpath(output_file)
        self.make_table = make_table
        self.tournament_results = {}
        self.player_played = {}
        self.player_winner = {}
        self.tour_counter = 0
        self.game_played = 0
        self.local_rules = local_rules

    def analyze_input_file(self):
        """ Analyzing input_file"""
        with open(self.input_file, mode='r', encoding='UTF8') as file:
            for line in file:
                if line.startswith('### Tour'):
                    self.tour_counter += 1
                    with open(self.output_file, 'a', encoding='UTF8') as report_file:
                        report_file.write(f'### Tour {self.tour_counter}\n')
                    continue
                if line.startswith('winner'):
                    self._winner()
                    continue
                self._analyze_input_line(line=line)
            if self.make_table:
                self.tournament_table()

    def _analyze_input_line(self, line):
        """ Going through each line in file"""
        line = line.rstrip()
        if line:
            line = line.split()
            self.player_name = line[0]
            self.player_result = line[1]
            bwl = bw.Bowling(self.player_result, local_rules=self.local_rules)
            bwl.check_result()
            self.player_result_count = bwl.total_result
            self.tournament_results[self.player_name] = []
            self.tournament_results[self.player_name].append(self.player_result)
            self.tournament_results[self.player_name].append(self.player_result_count)
            self._tour_result()

    def _tour_result(self):
        with open(self.output_file, 'a', encoding='UTF8') as report_file:
            report_file.write(f'{self.player_name} {self.tournament_results[self.player_name][0]}'
                              f' {self.tournament_results[self.player_name][1]}\n')

    def _winner(self):
        """ Who is round winner"""
        values_list = list(self.tournament_results.items())
        values_list.sort(key=lambda i: i[1][1], reverse=True)
        self.tournament_results = dict(values_list)
        for item in self.tournament_results.items():
            if item[0] in self.player_winner:
                self.player_winner[item[0]] += 1
            else:
                self.player_winner[item[0]] = 1
            break
        for item in self.tournament_results.items():
            if item[0] in self.player_winner:
                self.player_winner[item[0]] += 0
            else:
                self.player_winner[item[0]] = 0
            if item[0] in self.player_played:
                self.player_played[item[0]] += 1
            else:
                self.player_played[item[0]] = 1
        for item in self.tournament_results.items():
            with open(self.output_file, 'a', encoding='UTF8') as report_file:
                report_file.write(f'winner is {item[0]}\n')
            break

    def _tournament_table_making(self):
        for item in self.player_played.items():
            print(f'|{item[0]:^15}|{self.player_played[item[0]]:^20}|{self.player_winner[item[0]]:^20}|')

    def tournament_table(self):
        print(f'+{"-" * 15:^15}+{"-" * 20:^20}+{"-" * 20:^20}+')
        print(f'|{"Player":^15}|{"Game played":^20}|{"Total victories":^20}|')
        print(f'+{"-" * 15:^15}+{"-" * 20:^20}+{"-" * 20:^20}+')
        self._tournament_table_making()
        print(f'+{"-" * 15:^15}+{"-" * 20:^20}+{"-" * 20:^20}+')


if __name__ == '__main__':
    bt = BowlingTournament('tournament.txt', make_table=True, local_rules=False)
    bt.analyze_input_file()
