# ----------------------------------------------------------------------------------------------------------------------
#  SPDX-License-Identifier: BSD 3-Clause                                                                               -
#  Copyright (c) 2022 Jimmy Bierenbroodspot.                                                                           -
# ----------------------------------------------------------------------------------------------------------------------
"""A mastermind algorithm that tries to use the fundamentals of bogosort to solve a game of mastermind. It pops a random
combination from the pool of possible combinations and checks if it is the correct code, then repeats. This is obviously
horrifically inefficient and that's why the game length has been set to the maximum amount of combinations since this
algorithm rarely finds the answer below 100 guesses."""
import typing
import random

import lib.python.mastermind.mastermind as game
import initialization as init

# Overwrite game length to max amount of guesses.
GAME_LENGTH = 1296


def main() -> None:
    game_simulation: typing.Generator[typing.Tuple[int, int, bool], game.Code, None]
    answer: typing.Tuple[int, int, bool]
    guess: game.Code
    game_round: int = 0
    possible_combinations: typing.List[game.Code] = init.get_combinations()

    game_simulation = game.simulate_game(init.COLOURS, GAME_LENGTH, init.GAME_WIDTH)
    for _ in game_simulation:
        game_round += 1

        guess = possible_combinations.pop(random.randint(0, len(possible_combinations) - 1))
        answer = game_simulation.send(guess)
        print(f"Guessed: {guess}; answer: {answer}")

        if answer[2]:
            print(f"Game won in {game_round} guesses!")
            break
    else:
        print('Game lost.')


if __name__ == '__main__':
    main()
