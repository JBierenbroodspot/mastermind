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
import typing

import lib.python.mastermind.mastermind as game
import initialization as init


def main() -> None:
    game_simulation: typing.Generator[typing.Tuple[int, int, bool], game.Code, None]
    guess: game.Code
    answer: typing.Tuple[int, int, bool]
    game_round: int = 0
    possible_combinations: init.Json = init.get_combinations()

    game_simulation = game.simulate_game(init.COLOURS, init.GAME_LENGTH, init.GAME_WIDTH)
    for _ in game_simulation:
        game_round += 1

        guess = get_guess(possible_combinations)
        answer = game_simulation.send(guess)
        print(f"Guessed: {guess}; answer: {answer}")

        # Check if the game is won
        if answer[2]:
            print(f'Game won in {game_round + 1} guesses!')
            break

        possible_combinations = init.reduce(possible_combinations, guess, answer[:2])
    else:
        print('Game lost.')


def get_guess(possible_combinations: init.Json) -> typing.List[int]:
    """Choose a random item from possible_combinations.

    :param possible_combinations: A sequence of possible combinations.
    :return: A random item from possible_combinations.
    """
    return random.choice(possible_combinations)


if __name__ == "__main__":
    main()
