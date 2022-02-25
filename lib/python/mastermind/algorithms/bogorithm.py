# ----------------------------------------------------------------------------------------------------------------------
#  SPDX-License-Identifier: BSD 3-Clause                                                                               -
#  Copyright (c) 2022 Jimmy Bierenbroodspot.                                                                           -
# ----------------------------------------------------------------------------------------------------------------------
"""A mastermind algorithm that tries to use the fundamentals of bogosort to solve a game of mastermind. It pops a random
combination from the pool of possible combinations and checks if it is the correct code, then repeats. This is obviously
horrifically inefficient.
    This algorithm needs at best 1 guess and at most n^r, where n = the amount of objects and r = the sample size, guesses.
Because the probability of each amount of guesses to win the game (k) is equally distributed the average amount of
guesses needed by this algorithm is n^r/2. For a standard game of mastermind (n = 6 and r = 4) is this 6^4/2 = 1296/2 =
648 and since this number for most algorithms is around 3 or 4 makes bogorithm orders of magnitude worse than most
algorithms out there.
    This could be improved on by reducing the incompatible codes from the pool of possible guesses. This makes it the
simple algorithm but with a random guess rather than the first pick from the pool.
"""
import typing
import random

import lib.python.mastermind.mastermind as game
import initialization as init

# Overwrite game length to max amount of guesses.
init.GAME_LENGTH = 1296


def main() -> None:
    game_simulation: typing.Generator[typing.Tuple[int, int, bool], game.Code, None]
    answer: typing.Tuple[int, int, bool]
    guess: game.Code
    game_round: int = 0
    possible_combinations: typing.List[game.Code] = init.get_combinations()

    game_simulation = game.simulate_game(init.COLOURS, init.GAME_LENGTH, init.GAME_WIDTH)
    for _ in game_simulation:
        game_round += 1

        guess = possible_combinations.pop(random.randint(0, len(possible_combinations) - 1))
        answer = game_simulation.send(guess)

        if answer[2]:
            print(f"Game won in {game_round} guesses!")
            break
    else:
        print('Game lost.')


if __name__ == '__main__':
    main()
