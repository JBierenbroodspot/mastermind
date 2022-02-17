# ----------------------------------------------------------------------------------------------------------------------
#  SPDX-License-Identifier: BSD 3-Clause                                                                               -
#  Copyright (c) 2022 Jimmy Bierenbroodspot.                                                                           -
# ----------------------------------------------------------------------------------------------------------------------
"""A module containing some constants, types and functions which are commonly shared between algorithms."""
import typing
import json

import scripts.generate_set as generate_set
import lib.python.mastermind.mastermind as game

# These constants are declared here because they remain the same value in the entire module since I haven't implemented
# a way to customize them yet
GAME_WIDTH: int = 4
GAME_LENGTH: int = 8
COLOURS: typing.Tuple[int, ...] = tuple(num for num in range(6))

# Create generic Json type for ease of use, this has no actual functionality other than showing that something is a
# json serialized object.
Json: typing.Generic = typing.TypeVar('Json')


def get_combinations() -> Json:
    """Retrieves a list of all possible combinations from combinations.json.

    :return: A Json serialized object with all possible combinations.
    """
    json_io: typing.TextIO
    json_string: str

    # Generate dataset with possible combinations
    generate_set.main()

    with open('./combinations.json', 'r') as json_io:
        json_string = json_io.read()

    return json.loads(json_string)


def reduce(possible_combinations: Json, guess: game.Code, score: typing.Tuple[int, int]) -> Json:
    """Compares the score of all combinations in possible_combinations against the given score.

    :param possible_combinations: A list of possible combinations.
    :param guess: A sequence containing integers.
    :param score: A tuple containing 2 integers.
    :return: A list
    """
    # Using a list comprehension is absolutely useless here because game.compare_codes is a relatively expensive
    # function. I just really like writing comprehensions.
    return [
        possible_combination for possible_combination in possible_combinations
        if score == game.compare_codes(guess, possible_combination)
    ]
