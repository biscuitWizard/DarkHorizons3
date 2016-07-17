import random

def is_ic(character):
    """Determines whether the given object is in character"""
    return True

def trait_roll(traitValue, modifier):
    return random.randrange(-5, 5)

def dice_roll(sides, count = 1):
    result = 0
    for x in range(0, count):
        result += random.randrange(1, sides)

    return result

def dice_roll_str(dice_str):
    """
    A method for rolling dice. Is capable of calculating traits and doing simple math.
    Args:
        dice_str: a string that contains a dice roll code. ex: 2d6

    Returns:
        The result of the dice roll.
    """
    return dice_roll(6,2)