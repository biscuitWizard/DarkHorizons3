from world import rules
from evennia import create_script
from typeclasses.scripts import EngagementScript
from gamedb.models import HitEffect
from decimal import *


def start_combat(caller, target, action):
    prefix = "|r[|yCOMBAT|r]|n"
    engagement = create_script(EngagementScript, obj=caller)
    engagement.start_engagement(caller, target, caller.location)
    engagement.attacker_action = action

    engagement.location.msg_contents(
        "{2} {0} pewpews at the poor {1}".format(engagement.attacker.name, engagement.defender.name, prefix))
    engagement.defender.msg(
        "{1} {0} is shooting at you!!\n\t+pass - +dodge - +quickshot".format(engagement.attacker.name, prefix))


def resolve_combat(caller, action):
    engagement = caller.ndb.engagement
    skirmish = engagement.skirmish
    engagement.defender_action = action
    engagement.pause()


    attacker_weapons = engagement.attacker.equipment.get_weapons()
    defender_skill = engagement.defender_action.skill
    attacker_skill = engagement.attacker_action.skill


    # Update the advantage for the defender and attacker.
    skirmish.adjust_advantage(engagement.attacker, engagement.attacker_action.get_fatigue() * -1)
    skirmish.adjust_advantage(engagement.defender, engagement.defender_action.get_fatigue() * -1)

    total_hits = 0
    damage_list = list()
    critical = None

    action.on_before_attack_resolution(engagement)

    for weapon in attacker_weapons:
        # On before attack hook for combat API.
        if not action.on_before_attack(engagement):
            continue

        resolve_weapon_attack()

    action.on_after_attack_resolution(engagement, total_hits, damage_list)

    #  if total_hits > 0 and critical_momentum > 0 and sum(damage_list) - defender_toughness > 0:
    #      critical = resolve_status_effect(engagement.defender, critical[0], critical[1], critical[2])

    display_outcome(engagement, total_hits, damage_list, critical)
    engagement.clean_engagement()

def resolve_weapon_attack(attacker, defender, weapon, attack_skill, defense_skill):
    """

    Args:
        attacker:
        defender:
        weapon:
        attack_skill:
        defense_skill:

    Returns:

    """
    engagement = attacker.ndb.engagement
    defender_armor = defender.equipment.get_armor()
    # defender_toughness = engagement.defender.stats.get_trait("Endurance") / Decimal(10)
    defender_toughness = 3

    hit_roll = roll_to_hit(engagement.skirmish, attacker, defender, attack_skill, defense_skill)

    if hit_roll == 1:  # Hit
        # Oh noes. They've been hit.
        # Do an API call to see if the command has anything it wants to do.
        engagement.attacker_action.on_attack_hit(engagement, weapon)
        engagement.defender_action.on_attack_hit(engagement, weapon)

        hit_location = engagement.defender.status.get_hit_location(rules.dice_roll(100, 1))
        damage_roll = rules.dice_roll_str(weapon.get_tag("Damage"))
        damage = damage_roll - defender_armor

        if damage < 1:
            # We were extremely ineffective.
            engagement.location.msg_contents("The shot doesn't pierce their armor!")
            return

        engagement.defender.status.hurt(damage, hit_location)
        total_hits += 1
        damage_list.append(damage)

        # First glancing hits populate the critical field.
        # If this later becomes a critical hit, that's fine.
        if damage - defender_toughness > 0 and critical is None:
            critical = (hit_location, weapon.get_tag("Damage_Type"), True)

        # Glancing hits always have a chance to turn into critical hits.
        if damage > defender_toughness and (critical is None or critical[2] == True):
            critical = (hit_location, weapon.get_tag("Damage_Type"), False)
    elif hit_roll == 0:  # Miss
        engagement.attacker_action.on_attack_miss(engagement, weapon)
        engagement.defender_action.on_attack_miss(engagement, weapon)
    elif hit_roll == -1:  # Lucky Miss
        engagement.attacker_action.on_advantage_miss(engagement, weapon)
        engagement.defender_action.on_advantage_miss(engagement, weapon)

def roll_to_hit(skirmish, attacker, defender, attacker_skill, defender_skill):
    """
    Function to roll a contested skill die and return a result.
    Returns:
        -1: Lucky Miss
        0: Miss
        1: Hit
    """
    attack_roll = rules.trait_roll(attacker.stats.get_trait(attacker_skill),
                                   attacker.status.get_combat_modifier())
    defense_roll = rules.trait_roll(defender.stats.get_trait(defender_skill),
                                    defender.status.get_combat_modifier())
    if attack_roll - defense_roll > 0:
        advantage_roll = rules.dice_roll(100, 1)
        if advantage_roll >= skirmish.get_advantage(defender):
            return 1
        else:
            return -1
    else:
        return 0


def resolve_status_effect(target, hit_location, damage_type, is_glancing):
    """
    Function to resolve a status effect against a target. Calling this
    method will randomly select a status effect (based on is_glancing)
    and apply that status effect to the target.
    Args:
        target: The target to apply the status effect to.
        hit_location: Where the target was hit.
        damage_type: The type of damage for the weapon that scored the critical.
        is_glancing: Whether or not this was a critical status effect.

    Returns:
        The status effects that were applied.
    """
    critical_roll = 0
    if is_glancing:
        critical_roll = rules.dice_roll(6, 1)
    else:
        critical_roll = rules.dice_roll(6, 2)

    hit_effects = HitEffect.objects.filter(db_body_part__icontains=hit_location,
                                           db_trigger_index=critical_roll,
                                           db_damage_type__icontains=damage_type)
    for hit_effect in hit_effects:
        duration = rules.dice_roll_str(hit_effect.db_status_duration)
        target.status.apply_status_effect(hit_effect.db_status_effect, duration)

    return hit_effects


def cmd_check(caller, args, action, conditions):
    """"A function that can be called to test a variety of conditions in combat before executing a command.
    Returns false if everything checks out."""
    # Split the arguments into a list.
    arglist = args.split(None)
    # nargs = len(arglist)
    if 'NotEngaged' in conditions:
        if is_engaged(caller):
            return "|413Please wait for outstanding attacks to resolve!|n"
    if 'IsEngaged' in conditions:
        if not is_engaged(caller):
            return "|413You are currently not engaged!|n"
    if 'IsAttacker' in conditions:
        if caller.ndb.engagement.attacker != caller:
            return "|413You must be the attacker to do that!|n"
    if 'IsDefender' in conditions:
        if caller.ndb.engagement.defender != caller:
            return "|413You cannot do that.|n"
    if 'IsMelee' in conditions:
        weapons = caller.equipment.get_weapons()
        for weapon in weapons:
            tag = weapon.get_tag("Weapon_Type")
            if tag not in ["Melee", "Unarmed", "Lightsaber"]:
                return "|413You need a melee weapon to do that.|n"
    if 'IsRanged' in conditions:
        weapons = caller.equipment.get_weapons()
        for weapon in weapons:
            tag = weapon.get_tag("Weapon_Type")
            if tag != "Ranged":
                return "|413You need a ranged weapon to do that.|n"
    if 'IsThrowable' in conditions:
        weapons = caller.equipment.get_weapons()
        for weapon in weapons:
            tag = weapon.get_tag("Weapon_Type")
            if tag != "Throwing":
                return "|413You need a thrown weapon to do that.|n"
    if 'IsLightsaber' in conditions:
        weapons = caller.equipment.get_weapons()
        for weapon in weapons:
            tag = weapon.get_tag("Weapon_Type")
            if tag != "Lightsaber":
                return "|413You need a lightsaber to do that.|n"
    if 'IsUnarmed' in conditions:
        weapons = caller.equipment.get_weapons()
        for weapon in weapons:
            tag = weapon.get_tag("Weapon_Type")
            if tag != "Unarmed":
                return "|413You need to be unarmed to do that.|n"
    if 'HasHP' in conditions:
        # if not caller.db.HP:
        #    return ("|413You can't %s, you've been defeated!|n" % action)
        pass
    # Conditions requiring a target start here.
    if 'NeedsTarget' in conditions:
        if not arglist:
            return "|413You need to specify a target!|n"
        if caller.search(arglist[0], quiet=True):
            target = caller.search(arglist[0], quiet=True)[0]
        else:
            target = False
        if not target:
            return "|413That is not a valid target!|n"
        if not rules.is_ic(target):
            return "|413That is not a valid target!|n"
        if 'TargetNotSelf' in conditions:
            if target == caller:
                return "|413You can't %s yourself!|n" % action
        if 'TargetNotEngaged' in conditions:
            if is_engaged(target):
                return "|413%s is already engaged. Please way for their attacks to resolve.|n" % target
        if 'TargetIsMelee' in conditions:
            weapons = target.equipment.get_weapons()
            for weapon in weapons:
                tag = weapon.get_tag("Weapon_Type")
                if tag not in ["Melee", "Unarmed", "Lightsaber"]:
                    return "|413They need to be attacking with a melee weapon to do that.|n"
        if 'TargetIsRanged' in conditions:
            weapons = target.equipment.get_weapons()
            for weapon in weapons:
                tag = weapon.get_tag("Weapon_Type")
                if tag != "Ranged":
                    return "|413They need to be attacking with a ranged weapon to do that.|n"
    return False


def is_engaged(character):
    if not hasattr(character.ndb, 'engagement') or not character.ndb.engagement:
        return False
    if character.ndb.engagement.attacker == character or character.ndb.engagement.defender == character:
        return True
    return False


def display_outcome(engagement, total_hits, damage_list, critical):
    prefix = "|r[|yCOMBAT|r]|n"
    attacker_weapons = engagement.attacker.equipment.get_weapons()
    if total_hits == 0:
        engagement.attacker.msg("{4} You {0} at {1} with your {2}, but {1} {3}s!".format(engagement.attacker_action,
                                                                                     engagement.defender.name,
                                                                                     attacker_weapons[0].db_name,
                                                                                     engagement.defender_action,
                                                                                     prefix))
        engagement.location.msg_contents("{4} {0} shoots at {1} with their {2}, but {1} {3}s!".format(engagement.attacker_action,
                                                                                                  engagement.defender.name,
                                                                                                  attacker_weapons[0].db_name,
                                                                                                  engagement.defender_action,
                                                                                                  prefix),
                                         exclude=engagement.attacker)
        return
    engagement.location.msg_contents("{0} Oh snap! Hit!\nHits: {1}\nDamage: {2}\nDamage Dice: {3}\nWeapon: {4}".format(prefix, total_hits, damage_list[0], attacker_weapons[0].get_tag("Damage"), attacker_weapons[0].db_name))
