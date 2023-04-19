# ----------------------------------------------------------------------------------------------------------------------
#  SPDX-License-Identifier: BSD 3-Clause                                                                               -
#  Copyright (c) 2022 Jimmy Bierenbroodspot.                                                                           -
# ----------------------------------------------------------------------------------------------------------------------
"""
Mastermind solving algorithm using B. Kooi's new strategy algorithm.

This code is developed using pseudocode found in the following article:
Kooi, B. (2005). Yet another mastermind strategy. ICGA Journal, 28(1), 13-20.
"""
import typing
import collections

import initialization as init
import src.python.mastermind.mastermind as game


def main() -> None:
    game_simulation: typing.Generator[typing.Tuple[int, int, bool], game.Code, None]
    guess: game.Code
    answer: typing.Tuple[int, int, bool]
    categories: typing.Set[game.Code]
    partition_counts: typing.Dict[game.Code, int]
    largest_category: game.Code
    game_round: int = 0
    combinations: init.Json = init.get_combinations()

    game_simulation = game.simulate_game(
        init.COLOURS, init.GAME_LENGTH, init.GAME_WIDTH
    )
    for _ in game_simulation:
        game_round += 1

        # Find all categories left in the combinations and count the partitions.
        categories = get_all_categories(combinations)
        partition_counts = {
            category: get_partition_count(combinations, category)
            for category in categories
        }
        # Find the largest category.
        largest_category = max(partition_counts, key=partition_counts.get)
        guess = next(
            combination
            for combination in combinations
            if get_category(combination) == largest_category
        )
        answer = game_simulation.send(guess)
        print(f"Guessed: {guess}; answer: {answer}")

        # Check if the game is won
        if answer[2]:
            print(f"Game won in {game_round} guesses!")
            break

        combinations = init.reduce(combinations, guess, answer[:2])
    else:
        print("Game lost.")


def get_category(combination: game.Code) -> game.Code:
    """Decides the category of a combination. In most papers these categories are describes as: AAAA, AAAB, AABB, AABC
    and ABCD.

    :param combination: A Code combination of any width.
    :return: A list that substitutes the letters in a category for integers in such that AABC == [0, 0, 1, 2].
    """
    # Creates a list of values within the counter, we do not actually know to which number each value belongs.
    combination_counts: typing.List[int] = sorted(
        collections.Counter(combination).values(), reverse=True
    )
    category: game.Code = []  # This could've been a comprehension...

    # Appends the amount each colour (number) appears in the combination.
    for counter, combination_count in enumerate(combination_counts):
        category.extend([counter] * combination_count)

    return tuple(category)


def get_partition_count(
    possible_combinations: init.Json, combination: game.Code
) -> int:
    """Finds the amount a given combination can be partitioned in by comparing the codes and calculating the possible
    answer.

    :param possible_combinations: A list with unique Code combinations.
    :param combination: A Code combination.
    :return: The amount of possible partitions.
    """
    # Comprehensions are fun, aren't they?
    return len(
        collections.Counter(
            [
                game.compare_codes(combination, possible_combination)
                for possible_combination in possible_combinations
            ]
        )
    )


def get_all_categories(
    possible_combinations: init.Json,
) -> typing.Set[typing.Tuple[int]]:
    """Gets all categories in a list of combinations.

    :param possible_combinations: A list of possible combinations.
    :return: A set with one of every available category.
    """
    return {
        tuple(get_category(possible_combination))
        for possible_combination in possible_combinations
    }


if __name__ == "__main__":
    main()
