# ----------------------------------------------------------------------------------------------------------------------
#  SPDX-License-Identifier: BSD 3-Clause                                                                               -
#  Copyright (c) 2022 Jimmy Bierenbroodspot.                                                                           -
# ----------------------------------------------------------------------------------------------------------------------
"""
Mastermind solving algorithm using L. Sterling's and E. Shapiro's simple algorithm.

This code is developed using pseudocode found in the following book:
Sterling, L., & Shapiro, E. (1994). The art of Prolog: advanced programming techniques (2nd ed.). MIT Press.
"""
from __future__ import annotations
import random
import json
import typing

import lib.python.mastermind.mastermind as game
import scripts.generate_set as generate_set

# These constants are declared here because they remain the same value in the entire module since there is no way to
# customize them yet
GAME_WIDTH: int = 4
GAME_LENGTH: int = 8
COLOURS: typing.Tuple[int, ...] = tuple(num for num in range(6))

# Create generic Json type for ease of use, this has no actual functionality other than showing that something is a
# json serialized object.
Json: typing.Generic = typing.TypeVar('Json')


def main() -> None:
    game_simulation: typing.Generator[typing.Tuple[int, int, bool], game.Code, None]
    guess: game.Code
    answer: typing.Tuple[int, int, bool]
    game_round: int = 0
    possible_combinations: Json = get_combinations()

    # Generate dataset with possible combinations
    generate_set.main()

    game_simulation = game.simulate_game(COLOURS, GAME_LENGTH, GAME_WIDTH)
    for _ in game_simulation:
        game_round += 1

        guess = get_guess(possible_combinations)
        answer = game_simulation.send(guess)

        # Check if the game is won
        if answer[2]:
            print(f'Game won in {game_round + 1} guesses!')
            break

        possible_combinations = reduce(possible_combinations, guess, answer[:2])
    else:
        print('Game lost.')


def get_combinations() -> Json:
    """Retrieves a list of all possible combinations from combinations.json.

    :return: A Json serialized object with all possible combinations.
    """
    json_io: typing.TextIO
    json_string: str

    with open('./combinations.json', 'r') as json_io:
        json_string = json_io.read()

    return set(json.loads(json_string))


def get_guess(possible_combinations: Json) -> typing.List[int]:
    """Choose a random item from possible_combinations.

    :param possible_combinations: A sequence of possible combinations.
    :return: A random item from possible_combinations.
    """
    return random.choice(possible_combinations)


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


if __name__ == "__main__":
    main()
