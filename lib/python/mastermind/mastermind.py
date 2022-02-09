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

Code: typing.Tuple[str, ...] = typing.TypeVar('Code')
COLOURS: typing.Tuple[str, ...] = (
    'RED', 'GREEN', 'BLUE', 'YELLOW',
    'BROWN', 'ORANGE', 'WHITE', 'BLACK',
)

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


def generate_secret_code(length: int) -> Code:
    """Creates a `Code` tuple with random colours taken from the COLOURS constant.

    :param length: Length of generated code.
    :return: A tuple with 4 random colours.
    """
    return tuple(random.choices(COLOURS, k=length))


def compare_codes(secret: Code, to_compare: Code, code_length: int) -> typing.List[str]:
    """Takes two tuples and returns whether a colour is in the right position and right colour, wrong position or right
    colour or both wrong.

    :param secret: The secret code to compare against.
    :param to_compare: Input code to compare with.
    :param code_length: Expected length of the codes.
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

    for colour in colour_dict_list[0]:
        if colour in colour_dict_list[1]:
            correctness.extend(['INCORRECT_ORDER'] * min(colour_dict_list[0][colour], colour_dict_list[1][colour]))

    # Since we know that an equal amount of correct pairs are marked as incorrect order
    if len(correctness) != 0:
        correctness = correctness[:-correct_pairs]

    # If the list is smaller than 4 the combined list is topped off with wrongs.
    if len(correctness) < code_length:
        for _ in range(code_length - len(correctness)):
            correctness.append('WRONG')
    return correctness


# All bools start with is, right?
def is_won(correctness: typing.List[str]) -> bool:
    """Checks if a list contains all correct orders.

    :param correctness: A list that can either contain
    :return: True if correctness contains 4 correct orders, false if not.
    """
    # all() returns True if every item in an iterable returns True, or if the iterable is empty.
    return all(item == 'CORRECT_ORDER' for item in correctness)


def take_code(message: str, code_length: int) -> Code:
    """Asks user to input a colour code.

    :param message: Message to display.
    :param code_length: Expected length of the code.
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
            if all((colour in COLOURS) for colour in code):
                return tuple(code)


def game(game_length: int = 10, board_width: int = 4) -> typing.Generator[str, None, None]:
    """A game of mastermind where you compare user input against a computer generated code where the correctness of this
    code will be shown after every round.

    :param game_length: Amount of rounds.
    :param board_width: Width of the board.
    :return: True if won, False if user lost.
    """
    guess: Code
    correctness: typing.List[str]
    secret_code: Code = generate_secret_code(board_width)
    logging.debug(f'Secret code is:\t{secret_code}')

    for _ in range(game_length):
        guess = take_code('Choose colours.\n>>\t', board_width)
        logging.debug(f'Guessed code is:\t{guess}')

        correctness = compare_codes(secret_code, guess, board_width)
        logging.debug(f'Correctness for this round:\t{correctness}')

        if is_won(correctness):
            logging.debug('Game is won')
            yield f'{correctness}\nWon'
            return
        yield f'{correctness}'
    logging.debug('Game is lost')
    yield 'Lost'


def main() -> None:
    for game_round in game():
        print(game_round)


if __name__ == "__main__":
    main()
