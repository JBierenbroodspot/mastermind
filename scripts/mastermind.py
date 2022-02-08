import typing
import random

Code: typing.Union[typing.Tuple[str, str, str, str], typing.Tuple[str, ...]] = typing.TypeVar('Code')
COLOURS: typing.Tuple[str, ...] = (
    'RED', 'GREEN', 'BLUE', 'YELLOW',
    'BROWN', 'ORANGE', 'WHITE', 'BLACK',
)


def generate_secret_code() -> Code:
    """Creates a `Code` tuple with random colours taken from the COLOURS constant.

    :return: A tuple with 4 random colours.
    """
    return tuple(random.choices(COLOURS, k=4))


def compare_codes(secret: Code, to_compare: Code) -> typing.List[str]:
    """Takes two tuples and returns whether a colour is in the right position and right colour, wrong position or right
    colour or both wrong.

    :param secret: The secret code to compare against.
    :param to_compare: Input code to compare with.
    :return: A list that shows how many colors are in the right position, wrong position and how many of which both are
    wrong.
    """
    correct_order: typing.List[str]  # Correct colour and correct order
    incorrect_order: typing.List[str]  # Correct colour and wrong order
    combined_lists: typing.List[str]
    index: str
    colour: str

    # Enumerate() creates <class 'enumerate'> type object which consists of index, value tuple pairs for each item in an
    # iterable. Here I create two enumerate objects and compare them against each other. If there is a match it means
    # both the colour and the index, thus position, are the same which means a colour is in the right position.
    correct_order = [
        'CORRECT_ORDER' for (index, colour) in enumerate(secret) if (index, colour) in enumerate(to_compare)
    ]
    # Here secret and to_compare are compared to each other and adds 'INCORRECT_ORDER' to the list for every match. This
    # ignores positions, but we can assume that for every correct order there is exactly one incorrect order. So after
    # the comprehension we slice the list to its length minus the length of correct_order.
    incorrect_order = [
        'INCORRECT_ORDER' for colour in to_compare if colour in secret
    ][:-len(correct_order)]
    combined_lists = correct_order + incorrect_order

    # If the list is smaller than 4 the combined list is topped off with wrongs.
    if len(combined_lists) < 4:
        for _ in range(4 - len(combined_lists)):
            combined_lists.append('WRONG')

    return combined_lists


def is_won(correctness: typing.List[str]) -> bool:
    """Checks if a list contains all correct orders.

    :param correctness: A list that can either contain
    :return: True if correctness contains 4 correct orders, false if not.
    """
    correct_list: typing.List[str] = ['CORRECT_ORDER', 'CORRECT_ORDER', 'CORRECT_ORDER', 'CORRECT_ORDER']
    return correctness == correct_list


def take_code(message: str) -> Code:
    """Asks user to input a colour code.

    :param message: Message to display.
    :return: A list containing a colour code.
    """
    code: typing.List[str]
    colour: str

    for _ in range(4):
        while True:
            code = input(message).upper().replace(' ', '').split(',')
            if all((colour in COLOURS) for colour in code):
                return tuple(code)


def game(game_length: int = 10) -> bool:
    """A game of mastermind where you compare user input against a computer generated code where the correctness of this
    code will be shown after every round.

    :param game_length: Amount of rounds.
    :return: True if won, False if user lost.
    """
    guess: Code
    correctness: typing.List[str]
    secret_code: Code = generate_secret_code()
    # print('DEBUG:', secret_code)

    for _ in range(game_length):
        guess = take_code('Choose colour.\n>>\t')
        correctness = compare_codes(secret_code, guess)
        if is_won(correctness):
            return True
        print(correctness)
    return False


def main() -> None:
    print(game())


if __name__ == "__main__":
    main()
