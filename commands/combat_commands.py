from commands.command import Command
from world import combat_rules

_COMMAND_RESPONSES = []


def register_response(command):
    _COMMAND_RESPONSES.append(command)


def get_valid_responses(attacker, defender, attack_action):
    valid_responses = []

    for response_command in _COMMAND_RESPONSES:
        if response_command.is_valid_response(attacker, defender, attack_action):
            valid_responses.append(response_command)
    return valid_responses


class CombatCommand(Command):
    skill = ""
    fatigue = 0
    cooldown = 0
    weapons = []  # The command executor's weapon.
    verb = "ASSIGNVERB"

    attacker_hit_status = None  # Whether the attacker has been hit, missed, or lucky missed
    defender_hit_status = None  # Whether the defender has been hit, missed, or lucky missed

    def get_fatigue(self):
        """
        Method to get the fatigue used for this action.
        Returns:
            Returns an integer that represents the advantage cost.
        """
        return self.fatigue

    def get_skill(self):
        """
        Method to get the skill used for this action.
        Returns:
            Returns a string that is the skill name.
        """
        return self.skill

    def get_cooldown(self):
        return self.cooldown

    def on_message_format(self, attacker, defender, **kwargs):
        """
        Overrides the default message to be displayed on resolving a combat action
        with the return-variable supplied by this method.
        Args:
            attacker: The object that initiated the attack.
            defender: The object on the defending side of the conflict.
            **kwargs: A list of arguments relevant to the command. Commonly:
                attacker_weapon: The attacker's weapon. (or weapons if mult.)
                defender_weapon: The defender's weapon (or weapons if mult.)
                defender_hitloc: Where the defender has been hit.
                defender_damage: Damage the defender has taken.

        Returns:
            String with the value of the message. If None or 'pass',
            the system ignore the output of this function.
        """
        return "|r[|yCOMBAT|r]|n You {0} at {1} with your {2}!".format(self.verb, defender.name, self.weapons[0].name)

    def on_message_oformat(self, attacker, defender):
        # Default message: Attacker shoots at Xeebo with his/her Firefly Pistol!
        return "|r[|yCOMBAT|r]|n {0} {1}s at {2} with [^p {3}!".format(attacker.name, self.verb, defender.name,
                                                               self.weapons[0].name)


class ResponseCombatCommand(CombatCommand):
    @staticmethod
    def is_valid_response(attacker, defender, attack_action):
        return True

    def __init__(self):
        register_response(self)


class CmdShoot(CombatCommand):
    key = "+shoot"
    skill = "Blaster"
    fatigue = 5
    verb = "shoot"

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['NotEngaged', 'IsRanged',
                                                                              'NeedsTarget', 'TargetNotSelf',
                                                                              'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        target = self.caller.search(self.args)
        combat_rules.start_combat(self.caller, target, self, get_valid_responses(self.caller, target, self))

class CmdStrike(CombatCommand):
    key = "+strike"
    skill = ""
    fatigue = 5
    verb = "strike"

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['NotEngaged', 'IsMelee',
                                                                              'NeedsTarget', 'TargetNotSelf',
                                                                              'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        target = self.caller.search(self.args)
        combat_rules.start_combat(self.caller, target, self, get_valid_responses(self.caller, target, self))


class CmdThrow(CombatCommand):
    key = "+throw"
    skill = "Thrown"
    fatigue = 8
    verb = "throw"

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['NotEngaged', 'IsThrowable',
                                                                              'NeedsTarget', 'TargetNotSelf',
                                                                              'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        target = self.caller.search(self.args)
        combat_rules.start_combat(self.caller, target, self, get_valid_responses(self.caller, target, self))


class CmdInject(CombatCommand):
    key = "+inject"
    skill = "Brawl"
    fatigue = 8
    verb = "inject"

    def func(self):
        pass


class CmdAbort(CombatCommand):
    key = "+abort"

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsAttacker'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        engagement = self.caller.ndb.engagement
        engagement.location.msg_contents("{0} aborts their attack.".format(self.caller.name))
        engagement.clean_engagement()


class CmdPass(ResponseCombatCommand):
    key = "+pass"
    fatigue = -5
    bypass_advantage = True

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdDodge(ResponseCombatCommand):
    key = "+dodge"
    skill = "Dodge"
    fatigue = 5

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)

    def get_fatigue(self):
        engagement = self.caller.ndb.engagement
        if engagement.attacker_action.key == "+strike":
            return 10
        return 5


class CmdParry(ResponseCombatCommand):
    key = "+parry"
    skill = "Melee"
    fatigue = 5

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender', 'IsMelee',
                                                                              'TargetIsMelee'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdQuickshot(ResponseCombatCommand):
    key = "+quickshot"
    skill = "Quickdraw"
    fatigue = 10
    cooldown = 2

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender',
                                                                              'IsRanged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)

    def on_before_attack_resolution(self, engagement):
        weapon = self.caller.equipment.get_weapons()[0]
        combat_rules.resolve_weapon_attack(engagement.defender, engagement.attacker, weapon, self.skill,
                                           engagement.attacker_action.skill)

    def on_message_format(self, attacker, defender, **kwargs):
        defender_weapon = kwargs["defender_weapon"]
        # defender_damage = kwargs["defender_damage"]
        # defender_hitloc = kwargs["defender_hitloc"]
        attacker_weapon = kwargs["attacker_weapon"]
        attacker_damage = kwargs["attacker_damage"]
        attacker_hitloc = kwargs["attacker_hitloc"]

        result = ""

        if self.attacker_hit_status == 1 and self.defender_hit_status <= 0:
            result += "{0} raises {2} {3} to fire, but {1}'s " \
                      "{4} {5} {2} {6}.".format(defender.name, attacker.name, "her",
                                                defender_weapon, attacker_weapon, attacker_damage,
                                                attacker_hitloc)
        elif self.attacker_hit_status <= 0 and self.defender_hit_status == 1:
            result += "{0} shoots at {1} with {2} {5}, disrupting {3} attack and {6} " \
                      "{1}.".format(defender.name, attacker.name, "her", "his",
                                    attacker_weapon.db_name, defender_weapon.db_name,
                                    "vivisects")
        elif self.attacker_hit_status == 1 and self.defender_hit_status == 1:
            result += "{0} shoots at {1} with {2} {5}, but {1}'s {4} hits and {6} " \
                      "{0}.".format(defender.name, attacker.name, "her", "his",
                                    attacker_weapon.db_name, defender_weapon.db_name,
                                    "vivisects")
        elif self.attacker_hit_status <= 0 and self.defender_hit_status <= 0:
            result += "{0} shoots at {1} with {2} {5}, disrupting {1}'s attack " \
                      "but missing {3}.".format(defender.name, attacker.name, "her", "his",
                                                attacker_weapon.db_name, defender_weapon.db_name,
                                                "vivisects")
        return result


class CmdRiposte(ResponseCombatCommand):
    key = "+riposte"
    skill = "Melee"
    fatigue = 10
    cooldown = 2

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender', 'IsMelee',
                                                                              'TargetIsMelee'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdBlock(ResponseCombatCommand):
    key = "+block"
    skill = "Brawl"  # Melee is wielding melee weapon.
    fatigue = 5

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)

    def get_skill(self):
        if combat_rules.cmd_check(self.caller, self.args, self.key, ['IsMelee']):  # will return error if false
            return "Brawl"  # Result if wielding blaster or brawling.
        return "Melee"


class CmdCounter(ResponseCombatCommand):
    key = "+counter"
    skill = ""
    fatigue = 10
    cooldown = 2

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdInterfere(CombatCommand):
    key = "+interfere"
    aliases = ["+shield", "+protect"]
    skill = "Athletics"
    fatigue = 10

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['TargetIsEngaged', 'TargetIsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdReload(CombatCommand):
    key = "+reload"
    fatigue = 3

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        combat_rules.resolve_intermediary_action(self.caller, self)


class CmdCover(CombatCommand):
    key = "+cover"
    skill = ""
    fatigue = ""

    def func(self):
        self.weapons = self.caller.equipment.get_weapons()
        pass
