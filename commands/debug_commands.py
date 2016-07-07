from commands.command import Command

class CmdAddItem(Command):
    key = "+item/add"
    locks = "cmd:all()"

    def func(self):
        self.caller.add_item(1, 10)