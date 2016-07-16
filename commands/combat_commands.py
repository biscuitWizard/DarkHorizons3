from commands.command import Command
from world import combat_rules

def is_engaged(caller):
    if not hasattr(caller.ndb, 'engagement'):
        return False
    if caller.ndb.engagement.attacker == caller or caller.ndb.engagement.defender == caller:
        return True
    return False

class CmdShoot(Command):
    key = "+shoot"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "shoot", ['NotEngaged', 'IsRanged',
                                                                              'NeedsTarget', 'TargetNotSelf',
                                                                              'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        target = self.caller.search(self.args)
        combat_rules.start_combat(self.caller, target, "shoot")

class CmdStrike(Command):
    key = "+strike"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "strike", ['NotEngaged', 'IsMelee',
                                                                              'NeedsTarget', 'TargetNotSelf',
                                                                              'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

class CmdThrow(Command):
    key = "+throw"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "throw", ['NotEngaged', 'IsThrowable',
                                                                             'NeedsTarget', 'TargetNotSelf',
                                                                             'TargetNotEngaged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

class CmdAbort(Command):
    key = "+abort"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "abort", ['IsEngaged', 'IsAttacker'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        engagement = self.caller.ndb.engagement
        engagement.location.msg_contents("{0} aborts their attack.".format(self.caller.name))
        engagement.clean_engagement()

class CmdPass(Command):
    key = "+pass"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "pass", ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, "pass")

class CmdDodge(Command):
    key = "+dodge"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "dodge", ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, "dodge")

class CmdParry(Command):
    key = "+parry"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "parry", ['IsEngaged', 'IsDefender', 'IsMelee',
                                                                             'TargetIsMelee'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, "parry")

class CmdQuickshot(Command):
    key = "+quickshot"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "quickshot", ['IsEngaged', 'IsDefender',
                                                                                 'IsRanged'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, "quickshot")

class CmdRiposte(Command):
    key = "+riposte"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "riposte", ['IsEngaged', 'IsDefender', 'IsMelee',
                                                                               'TargetIsMelee'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, "riposte")

class CmdBlock(Command):
    key = "+block"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "block", ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, "block")

class CmdCounter(Command):
    key = "+counter"

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "counter", ['IsEngaged', 'IsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, "counter")

class CmdInterfere(Command):
    key = "+interfere"
    aliases = ["+shield", "+protect"]

    def func(self):
        cmd_check = combat_rules.cmd_check(self.caller, self.args, "counter", ['TargetIsEngaged', 'TargetIsDefender'])
        if cmd_check:
            self.caller.msg(cmd_check)
            return

        combat_rules.resolve_combat(self.caller, "interfere")

class CmdReload(Command):
    key = "+reload"

    def func(self):
        combat_rules.resolve_combat(self.caller, "reload")