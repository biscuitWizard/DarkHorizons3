from world import rules
from evennia import create_script
from typeclasses.scripts import EngagementScript
from decimal import *

def start_combat(caller, target, action):
    engagement = create_script(EngagementScript, obj=caller)
    engagement.start_engagement(caller, target, caller.location)

    engagement.location.msg_contents(
        "[GAME] {0} pewpews at the poor {1}".format(engagement.attacker.name, engagement.defender.name))
    engagement.defender.msg(
        "[GAME] {0} is shooting at you!!\n\t+pass - +dodge - +quickshot".format(engagement.attacker.name))

def resolve_combat(caller, action):
    engagement = caller.ndb.engagement
    engagement.pause()

    critical_momentum = engagement.defender.status.get_critical_momentum()
    defender_armor = engagement.defender.equipment.get_armor()
    # defender_toughness = engagement.defender.stats.get_trait("Endurance") / Decimal(10)
    defender_toughness = 3
    attacker_weapons = engagement.attacker.equipment.get_weapons()

    total_hits = 0
    damage_list = list()
    critical_made = False
    for weapon in attacker_weapons:
        attack_roll = rules.trait_roll(engagement.attacker.stats.get_trait("Dodge"), 0)
        defense_roll = rules.trait_roll(engagement.defender.stats.get_trait("Dodge"), 0)
        if attack_roll - defense_roll > 0:
            hit_location = rules.dice_roll(100, 1)
            damage_roll = rules.dice_roll(weapon.get_tag("Damage"))
            damage = damage_roll - defender_armor + critical_momentum

            if damage < 1:
                # We were extremely ineffective.
                engagement.location.msg_contents("The shot doesn't pierce their armor!")
                continue

            engagement.defender.status.hurt(damage, hit_location)
            total_hits += 1
            damage_list.add(damage)

            if damage > defender_toughness:
                critical_made = True

    if total_hits > 0 and critical_momentum > 0 and Sum(damage_list) - defender_toughness > 0:
        if critical_made:
            critical = None  # Apply a critical from the status effect table.
        else:
            critical = None  # Apply a non-critical status effect from the table.

    display_outcome(engagement, action, total_hits, damage_list, critical)
    engagement.clean_engagement()

def cmd_check(caller, args, action, conditions):
    """"A function that can be called to test a variety of conditions in combat before executing a command.
    Returns false if everything checks out."""
    # Split the arguments into a list.
    arglist = args.split(None)
    # nargs = len(arglist)
    if 'NotEngaged' in conditions:
        if is_engaged(caller):
            return ("|413Please wait for outstanding attacks to resolve!|n")
    if 'IsEngaged' in conditions:
        if not is_engaged(caller):
            return ("|413You are currently not engaged!|n")
    if 'IsAttacker' in conditions:
        if caller.ndb.engagement.attacker != caller:
            return ("|413You must be the attacker to do that!|n")
    if 'IsDefender' in conditions:
        if caller.ndb.engagement.defender != caller:
            return ("|413You cannot do that.|n")
    if 'IsMelee' in conditions:
        pass
    if 'IsRanged' in conditions:
        pass
    if 'IsThrowable' in conditions:
        pass
    if 'IsLightsaber' in conditions:
        pass
    if 'HasHP' in conditions:
        # if not caller.db.HP:
        #    return ("|413You can't %s, you've been defeated!|n" % action)
        pass
    # Conditions requiring a target start here.
    if 'NeedsTarget' in conditions:
        if not arglist:
            return ("|413You need to specify a target!|n")
        if caller.search(arglist[0], quiet=True):
            target = caller.search(arglist[0], quiet=True)[0]
        else:
            target = False
        if not target:
            return ("|413That is not a valid target!|n")
        if not rules.is_ic(target):
            return ("|413That is not a valid target!|n")
        if 'TargetNotSelf' in conditions:
            if target == caller:
                return ("|413You can't %s yourself!|n" % action)
        if 'TargetNotEngaged' in conditions:
            if is_engaged(target):
                return ("|413%s is already engaged. Please way for their attacks to resolve.|n" % target)
    return False

def is_engaged(character):
    if not hasattr(character.ndb, 'engagement') or not character.ndb.engagement:
        return False
    if character.ndb.engagement.attacker == character or character.ndb.engagement.defender == character:
        return True
    return False

def calc_momentum(character):
    if not hasattr(character.db, 'wounds'):
        return 0
    return sum(character.db.wounds.values()) / 15

def display_outcome(engagement, action, total_hits, damage_list, critical):
    engagement.location.msg_contents("Bang zoom.")
