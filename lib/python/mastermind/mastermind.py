"""
# ----------------------------------------------------------------------------------------------------------------------
#  SPDX-License-Identifier: BSD 3-Clause                                                                               -
#  Copyright (c) 2022 Jimmy Bierenbroodspot.                                                                           -
# ----------------------------------------------------------------------------------------------------------------------

A game of mastermind designed to be as modular as possible. If this module is directly executed you can play a
rudimentary game of mastermind in the terminal. You can enter your combination using comma-separated colour names. This
way is clunky and low-effort since this is not the intended UI.
"""
import typing
import random
import collections
import sys
import os
import logging
import argparse

Code: typing.Tuple[str, ...] = typing.TypeVar('Code')

# Set logging, logging location and logging format
if 'debug' in sys.argv:
    log_location: str = os.path.join(os.getcwd(), 'logs', 'mastermind-debug.log')
    os.makedirs(os.path.dirname(log_location), exist_ok=True)
    logging.basicConfig(
        filename=log_location,
        encoding='utf-8',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='a+',
    )


def generate_secret_code(colours: typing.Tuple[int, ...], length: int) -> Code:
    """Creates a `Code` tuple with random colours taken from the colours.

    :param colours: All possible colours to choose from.
    :param length: Length of generated code.
    :return: A tuple with 4 random colours.
    """
    return tuple(random.choices(colours, k=length))


def compare_codes(secret: Code, to_compare: Code, code_length: int) -> typing.List[str]:
    """Takes two tuples and returns whether a colour is in the right position and right colour, wrong position or right
    colour or both wrong.

    :param secret: The secret code to compare against.
    :param to_compare: Input code to compare with.
    :param code_length: Expected seq_length of the codes.
    :return: A list that shows how many colors are in the right position, wrong position and how many of which both are
    wrong.
    """
    # Used to store the amount of colours in correct order to account for these also getting flagged as incorrect order.
    correct_pairs: int
    correctness: typing.List[str] = []
    # Counter here is used to create a dictionary-like object with the frequency of every colour.
    frequencies: typing.List[typing.Counter] = [
        collections.Counter(secret),
        collections.Counter(to_compare),
    ]

    # Enumerate() creates <class 'enumerate'> type object which consists of index, value tuple pairs for each item in an
    # iterable. Here I create two enumerate objects and compare them against each other. If there is a match it means
    # both the colour and the index, thus position, are the same which means a colour is in the right position.
    for index, colour in enumerate(secret):
        if (index, colour) in enumerate(to_compare):
            correctness.append('CORRECT_ORDER')
    # Fun fact! Since __len__ simply returns a stored value the time complexity of len() is O(1).
    correct_pairs = len(correctness)

    # The frequencies are compared to each other and once a match is found INCORRECT_ORDER is added the lowest frequency
    # amount of time.
    for colour in frequencies[0]:
        if colour in frequencies[1]:
            correctness.extend(['INCORRECT_ORDER'] * min(frequencies[0][colour], frequencies[1][colour]))
    logging.debug(f'{frequencies}\t{correct_pairs}\t{correctness}')
    # Since we know that an equal amount of correct pairs are marked as incorrect order
    if correct_pairs != 0:
        correctness = correctness[:-correct_pairs]

    # If the list is smaller than board with the combined list is topped off with wrongs.
    correctness.extend(['WRONG'] * (code_length - len(correctness)))
    print(correctness)
    return correctness


# All bools start with is, right?
def is_won(correctness: typing.List[str]) -> bool:
    """Checks if a list contains all correct orders.

    :param correctness: A list that can either contain
    :return: True if correctness contains 4 correct orders, false if not.
    """
    # all() returns True if every item in an iterable returns True, or if the iterable is empty.
    return all(item == 'CORRECT_ORDER' for item in correctness)


def take_code(colours: typing.Tuple[int, ...], message: str, code_length: int) -> Code:
    """Asks user to input a colour code.

    :param colours: All possible colours to choose from.
    :param message: Message to display.
    :param code_length: Expected seq_length of the code.
    :return: A list containing a colour code.
    """
    code: typing.List[str]
    colour: str

    # This loop will continue until KeyboardInterrupt is thrown or a correct code has been entered.
    while True:
        # Here input is taken from the user. The string is then made uppercase, whitespaces are removed, and it is split
        # by the delimiter ','.
        code = input(message).upper().replace(' ', '').split(',')
        if len(code) == code_length:
            # all() will evaluate to True if every colour in the input code is inside the COLOUR constant.
            if all((colour in colours) for colour in code):
                return tuple(code)


def game(colours: typing.Tuple[int, ...], game_length, board_width) -> typing.Generator[str, None, None]:
    """A game of mastermind where you compare user input against a computer generated code where the correctness of this
    code will be shown after every round.

    :param colours: All possible colours to choose from.
    :param game_length: Amount of rounds.
    :param board_width: Width of the board.
    :return: True if won, False if user lost.
    """
    guess: Code
    correctness: typing.List[str]
    secret_code: Code = generate_secret_code(colours, board_width)
    logging.debug(f'Secret code is:\t{secret_code}')

    for _ in range(game_length):
        guess = take_code(colours, 'Choose colours.\n>>\t', board_width)
        logging.debug(f'Guessed code is:\t{guess}')

        correctness = compare_codes(secret_code, guess, board_width)
        logging.debug(colours, f'Correctness for this round:\t{correctness}')

        if is_won(correctness):
            logging.debug('Game is won')
            yield f'{correctness}\nWon'
            return
        yield f'{correctness}'
    logging.debug('Game is lost')
    yield 'Lost'


def main() -> None:
    colours: typing.Tuple[int, ...]
    arguments: argparse.Namespace
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    game_length: int
    game_width: int
    game_round: str

    # Setup argument parser
    parser.add_argument('--colours', '-c', help='Amount of possible colours, default 6', type=int, default=6)
    parser.add_argument('--length', '-l', help='Amount of rounds before lose condition, default 8', type=int, default=8)
    parser.add_argument('--width', '-w', help='Length of codes, default 4', type=int, default=4)
    arguments = parser.parse_args()

    colours = tuple(number for number in range(arguments.colours))
    game_length = arguments.length
    game_width = arguments.width

    for game_round in game(colours, game_length, game_width):
        print(game_round)


if __name__ == "__main__":
    main()
