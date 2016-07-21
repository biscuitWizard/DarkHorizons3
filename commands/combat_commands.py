from commands.command import Command
from world import combat_rules


class CombatCommand(Command):
    skill = ""
    fatigue = 0
    cooldown = 0

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


class CmdShoot(CombatCommand):
    key = "+shoot"
    skill = "Blaster"
    fatigue = 5
    counters = [CmdPass, CmdDodge, CmdQuickshot]

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['NotEngaged', 'IsRanged',
                                                                              'NeedsTarget', 'TargetNotSelf',
                                                                              'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        target = self.caller.search(self.args)
        combat_rules.start_combat(self.caller, target, self)


class CmdStrike(CombatCommand):
    key = "+strike"
    skill = ""
    fatigue = 5

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['NotEngaged', 'IsMelee',
                                                                              'NeedsTarget', 'TargetNotSelf',
                                                                              'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return


class CmdThrow(CombatCommand):
    key = "+throw"
    skill = "Thrown"
    fatigue = 8

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['NotEngaged', 'IsThrowable',
                                                                              'NeedsTarget', 'TargetNotSelf',
                                                                              'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return


class CmdInject(CombatCommand):
    key = "+inject"
    skill = "Brawl"
    fatigue = 8

    def func(self):
        pass


class CmdAbort(CombatCommand):
    key = "+abort"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsAttacker'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        engagement = self.caller.ndb.engagement
        engagement.location.msg_contents("{0} aborts their attack.".format(self.caller.name))
        engagement.clean_engagement()


class CmdPass(CombatCommand):
    key = "+pass"
    fatigue = -5

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdDodge(CombatCommand):
    key = "+dodge"
    skill = "Dodge"
    fatigue = 5

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)

    def get_fatigue(self):
        engagement = self.caller.ndb.engagement
        if engagement.attack_action.key == "+strike":
            return 10
        return 5


class CmdParry(CombatCommand):
    key = "+parry"
    skill = "Melee"
    fatigue = 5

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender', 'IsMelee',
                                                                              'TargetIsMelee'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdQuickshot(CombatCommand):
    key = "+quickshot"
    skill = "Quickdraw"
    fatigue = 10
    cooldown = 2

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender',
                                                                              'IsRanged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdRiposte(CombatCommand):
    key = "+riposte"
    skill = "Melee"
    fatigue = 10
    cooldown = 2

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender', 'IsMelee',
                                                                              'TargetIsMelee'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdBlock(CombatCommand):
    key = "+block"
    skill = "Brawl"  # Melee is wielding melee weapon.
    fatigue = 5

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)

    def get_skill(self):
        if combat_rules.cmd_check(self.caller, self.args, self.key, ['IsMelee']):  # will return error if false
            return "Brawl"  # Result if wielding blaster or brawling.
        return "Melee"


class CmdCounter(CombatCommand):
    key = "+counter"
    skill = ""
    fatigue = 10
    cooldown = 2

    def func(self):
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
        cmd_check = combat_rules.cmd_check(self.caller, self.args, self.key, ['TargetIsEngaged', 'TargetIsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, self)


class CmdReload(CombatCommand):
    key = "+reload"
    skill = ""
    fatigue = ""

    def func(self):
        combat_rules.resolve_combat(self.caller, self)


class CmdCover(CombatCommand):
    key = "+cover"
    skill = ""
    fatigue = ""

    def func(self):
        pass

