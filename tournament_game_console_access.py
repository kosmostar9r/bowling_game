import argparse
import bowling_tournament as bt
""" Console script for bowling_tournament.py module """


def str_to_bool(string):  # не понимаю, почему передача type=bool не работает в аргументе
    """
        little module for converting string to boolean
        :param string: input need to convert
        :return: True/False
        """
    if isinstance(string, bool):
        return string
    if string.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif string.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


tournament_parser = argparse.ArgumentParser("Script for analyzing tournament results. "
                                            "Enter input file with player's results and output file where to write"
                                            "the competition's results")

tournament_parser.add_argument('-i', '--input_file', required=True, help='Full path to file needed to be analyzed')
tournament_parser.add_argument('-o', '--output_file', help='Full path to file where to write results')
tournament_parser.add_argument('-m', '--make_table', type=str_to_bool, help='Choose True or False. Need to print'
                                                                            'tournament table or not')
tournament_parser.add_argument('-l', '--local_rules', type=str_to_bool,
                               help='Choose rules for counting game result:'
                                    'pick True if you want to use local,'
                                    'pick False for tournament rules')

tournament_files = vars(tournament_parser.parse_args())
tournament_checker = bt.BowlingTournament(**tournament_files)
tournament_checker.analyze_input_file()
print(f"Saved at {tournament_files['output_file']}")

# input example
# python3 tournament_game_console_access.py -i tournament.txt -o tournament_result.txt
# python3 tournament_game_console_access.py -i tournament.txt -o tournament_result.txt -m false -l false
