"""
# ----------------------------------------------------------------------------------------------------------------------
#  SPDX-License-Identifier: BSD 3-Clause                                                                               -
#  Copyright (c) 2022 Jimmy Bierenbroodspot.                                                                           -
# ----------------------------------------------------------------------------------------------------------------------

A game of mastermind designed to be as modular as possible. If this module is directly executed you can play a
rudimentary game of mastermind in the terminal. This way is clunky and low-effort since this is not the intended UI.
"""
import typing
import random
import collections
import os
import logging
import argparse

Code: typing.Union[typing.Tuple[int, ...], typing.List[int]] = typing.TypeVar('Code')

GAME_HEADER: str = """# ---------------------------------------------- MasterMind -------------------------------------\
--------------------- #
#                                                                                                                      #
# How to play:                                                                                                         #
#   The computer will randomly decide a secret code and you will have to crack that code. You enter a sequence of      #
#   numbers and the computer will tell you how many numbers are the correct number in the right place and how many     #
#   numbers are correct but in the wrong place.                                                                        #
#                                                                                                                      #
# How to customize:                                                                                                    #
#   Run this module with the '--help' parameter to see how to customize the game rules.                                #
#                                                                                                                      #
# Note:                                                                                                                #
#   For ease of use and extendability numbers are substituted for the colours in the original MasterMind game. This    #
#   way you can submit a code by simply entering 0012 for example.                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
"""


def _init_logging() -> None:
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


def _init_arguments() -> argparse.Namespace:
    """Initializes arguments

    :return: An argparse.Namespace object with all parsed arguments.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--colours', '-c', help='Amount of possible colours, default 6', type=int, default=6)
    parser.add_argument('--length', '-l', help='Amount of rounds before lose condition, default 8', type=int, default=8)
    parser.add_argument('--width', '-w', help='Length of codes, default 4', type=int, default=4)
    parser.add_argument('--debug', help='Enable or disable debugging, default False', type=bool, default=False)

    return parser.parse_args()


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
    logging.debug(f'{frequencies}\t{incorrect_order, incorrect_order}')
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


def get_user_input(colours: typing.Tuple[int, ...], message: str, code_length: int) -> Code:
    """Asks user to input a colour code.

    :param colours: All possible colours to choose from.
    :param message: Message to display.
    :param code_length: Expected seq_length of the code.
    :return: A list containing a colour code.
    """
    colour: str
    code: Code = []
    is_correct = False

    while not is_correct:
        code = clean_user_input(input(message))
        # Check if code consists of only allowed values and is of the correct length, all() returns True if all values
        # within are True.
        is_correct = all((colour in colours) for colour in code) and len(code) == code_length
    else:
        return code


def clean_user_input(user_input: str) -> Code:
    """Turns a string into a tuple of int.

    :param user_input: A string containing numeric characters.
    :return: A Code list populated by integers if input is numeric, otherwise an empty list is returned.
    """
    cleaned_code: Code = []
    user_input = user_input.replace(' ', '')  # Remove all whitespace.

    if user_input.isnumeric():
        cleaned_code = [int(character) for character in user_input]

    return cleaned_code


def simulate_game(colours: typing.Tuple[int, ...],
                  game_length: int,
                  board_width: int) -> typing.Generator[typing.Tuple[int, int, bool], Code, None]:
    """A game of mastermind where you compare user input against a computer generated code where the correctness of this
    code will be yielded after every round.

    :param colours: All possible colours to choose from.
    :param game_length: Amount of rounds.
    :param board_width: Width of the board.
    :return: The amount of correct positions, correct colour but incorrect position and whether the game is won or not.

    :example:
    game_simulation = simulate_game(colours, length, board_width)
    for _ in game_simulation:
        guess = [0, 0, 1, 2]
        answer = game_simulation.send(guess)  # Send the guess to the generator and store the answer at the same time

        if answer[2]:  # If the third value is True the game has been won.
            print('game is won!')
    else:  # If the generator stops the game is lost.
        print('game is lost!')
    """
    guess: Code
    won: bool
    correctness: typing.Tuple[int, int]
    secret_code: Code = generate_secret_code(colours, board_width)
    logging.debug(f'Secret code is:\t{secret_code}')

    for _ in range(game_length):
        # Whenever yield is to the right of an equal sign, and you call generator.send() it will assign that value to
        # whatever is left of the equals sign.
        guess = yield
        logging.debug(f'Guessed code is:\t{guess}')

        # Compares the guess against the secret code.
        correctness = compare_codes(secret_code, guess)
        won = is_won(correctness, board_width)
        logging.debug(f'{colours}\tCorrectness for this round:\t{correctness}')

        # If won is True the last correctness is yielded and the generator is terminated.
        if won:
            logging.debug('Game is won')
            yield *correctness, won
            return
        # If the game is not yet won the correctness and False is returned.
        yield *correctness, won
    # If the loop runs out of iterations the game is lost.
    logging.debug('Game is lost')


def main() -> None:
    colours: typing.Tuple[int, ...]
    arguments: argparse.Namespace
    game_length: int
    game_width: int
    game: typing.Generator[typing.Tuple[int, int, bool], Code, None]
    won_game: bool
    game_round: typing.Tuple[int, int, bool] = 0, 0, False

    arguments = _init_arguments()

    if arguments.debug:
        _init_logging()

    colours = tuple(number for number in range(arguments.colours))
    game_length = arguments.length
    game_width = arguments.width

    print(GAME_HEADER)
    # Simulate game
    game = simulate_game(colours, game_length, game_width)
    for _ in game:
        game_round = game.send(get_user_input(colours, 'Choose colours.\n>>\t', game_width))
        print(game_round[:2])

    if game_round[2]:
        print('Congratulations, you won!')
    else:
        print('You lost, better luck next time')


if __name__ == "__main__":
    main()
