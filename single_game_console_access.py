""" Console script for bowling.py module """
import argparse
import bowling as bw


def str_to_bool(string):
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


bowling_parser = argparse.ArgumentParser('Input your bowling game result. It should consist of 10 frames with '
                                         'correct game rules. Example - 3271-/44X--2/X43-8')

bowling_parser.add_argument('-r', '--result', required=True, help='Game result in 1 string without spaces.'
                                                                  'Example - 9-4/529/8/XX-6311/')
bowling_parser.add_argument('-l', '--local_rules', type=str_to_bool,
                            help='Choose rules for counting game result:'
                                 'pick True if you want to use local,'
                                 'pick False for tournament rules')

bowling_result = vars(bowling_parser.parse_args())
game_checker = bw.Bowling(**bowling_result)
game_checker.check_result()
game_checker.print_result()


# input example
# python3 single_game_console_access.py -r 1/X3-5/X8154-57/X -l true
# python3 single_game_console_access.py -r 1/X3-5/X8154-57/X -l false
