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
import os
import logging
import argparse

Code: typing.Tuple[int, ...] = typing.TypeVar('Code')


def setup_logging() -> None:
    """Initializes logging by configuring logging and setting the logging location.

    :return: None.
    """
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


def compare_codes(secret: Code, to_compare: Code) -> typing.Tuple[int, int]:
    """Takes two tuples and returns whether a colour is the correct colour and in the correct position or incorrect
     position but correct colour.

    :param secret: The secret code to compare against.
    :param to_compare: Input code to compare with.
    :return: A tuple where the first index is correct order, correct position and the second is incorrect position but
    correct colour.
    """
    correct_order: int = 0
    incorrect_order: int = 0
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
            correct_order += 1

    # The frequencies are compared to each other and once a match is found incorrect_order is incremented by the lowest
    # frequency.
    for colour in frequencies[0]:
        if colour in frequencies[1]:
            incorrect_order += min(frequencies[0][colour], frequencies[1][colour])
    logging.debug(f'{frequencies}\t{incorrect_order}\t{correctness}')
    # Since we know that an equal amount of correct pairs are marked as incorrect order
    incorrect_order -= correct_order

    return correct_order, incorrect_order


# All bools start with is, right?
def is_won(correctness: typing.Tuple[int, int], board_width: int) -> bool:
    """Compares the left of correctness against the width of the board.

    :param correctness: A tuple that contains the amount of colours in the correct position on the first index.
    :param board_width: Width of the board.
    :return: True if the first index is the same as the board width.
    """
    return correctness[0] == board_width


def take_code(colours: typing.Tuple[int, ...], message: str, code_length: int) -> Code:
    """Asks user to input a colour code.

    :param colours: All possible colours to choose from.
    :param message: Message to display.
    :param code_length: Expected seq_length of the code.
    :return: A list containing a colour code.
    """
    code: Code
    colour: str

    # This loop will continue until KeyboardInterrupt is thrown or a correct code has been entered.
    while True:
        # Here input is taken from the user. The string is then made uppercase, whitespaces are removed, and it is split
        # by the delimiter ','. Then maps this list with int (mapping applies a function to every item in an iterable
        # and in this case int is the function) which is converted to a tuple.
        code = tuple(map(int, input(message).upper().replace(' ', '').split(',')))
        if len(code) == code_length:
            # all() will return True if everything within its parameter is also True.
            if all((colour in colours) for colour in code):
                return code


def game(colours: typing.Tuple[int, ...],
         game_length,
         board_width) -> typing.Generator[typing.Tuple[int, int, bool], None, None]:
    """A game of mastermind where you compare user input against a computer generated code where the correctness of this
    code will be yielded after every round.

    :param colours: All possible colours to choose from.
    :param game_length: Amount of rounds.
    :param board_width: Width of the board.
    :return: The amount of correct positions, correct colour but incorrect position and whether the game is won or not.
    """
    guess: Code
    won: bool
    correctness: typing.Tuple[int, int]
    secret_code: Code = generate_secret_code(colours, board_width)
    logging.debug(f'Secret code is:\t{secret_code}')

    for _ in range(game_length):
        guess = take_code(colours, 'Choose colours.\n>>\t', board_width)
        logging.debug(f'Guessed code is:\t{guess}')

        correctness = compare_codes(secret_code, guess)
        won = is_won(correctness, board_width)
        logging.debug(colours, f'Correctness for this round:\t{correctness}')

        if won:
            logging.debug('Game is won')
            yield *correctness, won
            return
        yield *correctness, won
    logging.debug('Game is lost')
    yield 0, 0, False


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
    parser.add_argument('--debug', help='Enable or disable debugging, default False', type=bool, default=False)
    arguments = parser.parse_args()

    if arguments.debug:
        setup_logging()

    colours = tuple(number for number in range(arguments.colours))
    game_length = arguments.length
    game_width = arguments.width

    for game_round in game(colours, game_length, game_width):
        print(game_round)


if __name__ == "__main__":
    main()
