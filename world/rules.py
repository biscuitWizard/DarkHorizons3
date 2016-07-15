import random

def is_ic(character):
    """Determines whether the given object is in character"""
    return True

def calc_trait(character):
    levels = 10
    multiplier = 3
    is_major = 1

    trait_value = 0
    for level in range(1, levels):
        plateau = multiplier / 100
        if not is_major:
            plateau = plateau / 2

        trait_value += (100 - trait_value) * plateau

    return trait_value

def trait_roll(traitValue, modifier):
    return random.randrange(-5, 5)

def dice_roll(sides, count = 1):
    result = 0
    for x in range(0, count):
        result += random.randrange(1, sides)

    return result