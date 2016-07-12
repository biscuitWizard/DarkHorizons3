from commands.command import Command
from evennia import create_script
from typeclasses.scripts import EngagementScript

class CmdShoot(Command):
    key = "+shoot"
    locks = "cmd:all()"

    def func(self):
        engagement = create_script(EngagementScript, obj=self.caller)

        #script = next(engagement for engagement in self.caller.scripts if engagement.key == "engagement_script")
        engagement.aggressor = self.caller
        engagement.defender = self.caller  # Replace later TODO
        engagement.location = self.caller.location

        engagement.location.msg_contents("[GAME] {0} pewpews at the poor {1}".format(engagement.aggressor.name, engagement.defender.name))
        engagement.defender.msg("[GAME] {0} is shooting at you!!\n\t+pass - +dodge - +quickshot".format( engagement.aggressor.name))

        #engagement.start(force_restart=True)

class CmdStrike(Command):
    key = "+strike"
    locks = "cmd:all()"

    def func(self):
        pass

class CmdThrow(Command):
    key = "+throw"
    locks = "cmd:all()"

    def func(self):
        pass

class CmdPass(Command):
    key = "+pass"
    locks = "cmd:all()"

    def func(self):
        pass

class CmdDodge(Command):
    key = "+dodge"
    locks = "cmd:all()"

    def func(self):
        pass

class CmdParry(Command):
    key = "+parry"
    locks = "cmd:all()"

    def func(self):
        pass

class CmdQuickshot(Command):
    key = "+quickshot"
    locks = "cmd:all()"

    def func(self):
        pass

class CmdRiposte(Command):
    key = "+riposte"
    locks = "cmd:all()"

    def func(self):
        pass

class CmdBlock(Command):
    key = "+block"
    locks = "cmd:all()"

    def func(self):
        pass

class CmdCounter(Command):
    key = "+counter"
    locks = "cmd:all()"

    def func(self):
        pass
