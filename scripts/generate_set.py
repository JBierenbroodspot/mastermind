# ----------------------------------------------------------------------------------------------------------------------
#  SPDX-License-Identifier: BSD 3-Clause                                                                               -
#  Copyright (c) 2022 Jimmy Bierenbroodspot.                                                                           -
# ---------------------------------------------------------------------------------------------------------------------
"""
Generates a set of all legal combinations and saves it in combinations.json.
"""
import typing
import json
import itertools
import argparse


def main() -> None:
    values: typing.Set[int]
    width: int
    json_io: typing.TextIO

    # Set up argument parser
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--seq_length', '-l', help='Amount of possible values', type=int, default=6)
    parser.add_argument('--width', '-w', help='Amount of values in a single combination', type=int, default=4)
    parser.add_argument('--file', '-f', help='Full path to output file', type=str, default='./combinations.json')
    arguments: argparse.Namespace = parser.parse_args()

    width = arguments.width
    sequence_length = arguments.seq_length

    with open(arguments.file, 'w+') as json_io:
        json_io.write(json.dumps(generate_permutations_with_replacement(width, sequence_length)))


def generate_permutations_with_replacement(width: int, seq_length: int) -> typing.List[typing.Tuple[int, ...]]:
    """
    Generates a list containing all seq_length**width possible permutations

    :param width: The length of each combination.
    :param seq_length: The amount of each possible types
    :return: A list containing all possible permutations with replacement.
    """
    return [permutation for permutation in itertools.product(range(seq_length), repeat=width)]


if __name__ == "__main__":
    main()
