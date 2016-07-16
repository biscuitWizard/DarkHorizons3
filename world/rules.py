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