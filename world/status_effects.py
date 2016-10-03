class StatusEffect:
    def __init__(self, name, value, duration):
        self.name = name
        self.value = value
        self.duration = duration
        self.remaining = duration

    def resolve_round(self):
        pass

    def resolve_effect(self):
        pass

    def calc_trait_modifier(self, trait):
        """
        Calculates if this StatusEffect modifies the specified trait.
        Args:
            trait: The trait's name.

        Returns:
            An integer that will be added to the user's final skill level.
        """
        return 0


class LimbStatusEffect(StatusEffect):
    def __init__(self, name, value, duration, limb):
        super(LimbStatusEffect, name, value, duration)
        self.limb = limb


class OnFireStatusEffect(LimbStatusEffect):
    def resolve_round(self):
        pass


class MangledLimbStatusEffect(LimbStatusEffect):
    pass


class SeveredLimbStatusEffect(LimbStatusEffect):
    pass


class HidingStatusEffect(StatusEffect):
    pass


class CoverStatusEffect(StatusEffect):
    pass


class BurnedStatusEffect(LimbStatusEffect):
    pass
