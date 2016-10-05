from commands.command import Command


class CmdIC(Command):
    key = "+ic"

    def func(self):
        pass


class CmdOOC(Command):
    key = "+ooc"

    def func(self):
        pass


class CmdStats(Command):
    key = "+stats"

    def func(self):
        stats = self.caller.stats
        equipment = self.caller.equipment

        body_armor = equipment.get_armor_name('body')
        body_armor = body_armor if body_armor else "Nothing"
        arm_armor = equipment.get_armor_name('arms')
        arm_armor = arm_armor if arm_armor else "Nothing"
        leg_armor = equipment.get_armor_name('legs')
        leg_armor = leg_armor if leg_armor else "Nothing"
        head_armor = equipment.get_armor_name('head')
        head_armor = head_armor if head_armor else "Nothing"

        stat_screen = Text.center(" +STATS: {0} ".format(self.caller.name), 78, '=', '|y', '|r')
        stat_screen += "\n {0}{1} {2}{3}".format(Text.left("Race:", 15, color='|y'), Text.left(stats.get_race(), 19),
                                                 Text.left("Weapon", 8, color='|y'), Text.left(equipment.get_weapons()[0].name, 19))
        stat_screen += "\n {0}{1} {2}{3}".format(Text.left("Level:", 15, color='|y'), Text.left(str(stats.get_level()), 19),
                                                 Text.left("Armor:", 8, color='|y'), Text.left(body_armor, 19))
        stat_screen += "\n {0}{1} {2}{3}".format(Text.left("Experience:", 15, color='|y'), Text.left(str(stats.get_experience()), 19),
                                                 Text.left("Helmet:", 8, color='|y'), Text.left(head_armor, 19))
        stat_screen += "\n {0}{1} {2}{3}".format(Text.left("Condition:", 15, color='|y'), Text.left("Excellent", 19),
                                                 Text.left("Arms:", 8, color='|y'), Text.left(arm_armor, 19))
        stat_screen += "\n {0}{1} {2}{3}".format(Text.left("Escapes Left:", 15, color='|y'), Text.left("0", 19),
                                                 Text.left("Legs:", 8, color='|y'), Text.left(leg_armor, 19))

        stat_screen += "\n" + Text.center(" Character Traits ", 78, '-', '|y', '|r')

        index = 0
        for trait in self.caller.stats.get_traits():
            if index % 2 == 0:
                stat_screen += "\n"
            trait_value = self.caller.stats.get_trait(trait)
            stat_screen += " " + Text.left("{0} [{1}]".format(trait, trait_value), 38, color='|y')

            index += 1

        stat_screen += "\n|r" + ("=" * 78) + "|n"
        self.caller.msg(stat_screen)


class Text:
    @staticmethod
    def center(text, width=78, fill=' ', color=None, fill_color=None):
        left_len = (width - len(text)) / 2
        right_len = width - (left_len + len(text))

        left_fill = fill * left_len
        if fill_color:
            left_fill = fill_color + left_fill + "|n"
        right_fill = fill * right_len
        if fill_color:
            right_fill = fill_color + right_fill + "|n"
        if color:
            text = color + text + "|n"

        return "{0}{1}{2}".format(left_fill, text, right_fill)

    @staticmethod
    def left(text, width, fill=' ', color=None):
        fill_len = width - len(text)

        if len(text) < width:
            if color:
                text = color + text + "|n"
            return text + (fill * fill_len)
        else:
            text = text[:width]
            if color:
                text = color + text + "|n"
            return text

    @staticmethod
    def right(text, width, fill=' ', color=None):
        fill_len = width - len(text)

        if len(text) < width:
            if color:
                text = color + text + "|n"
            return (fill * fill_len) + text
        else:
            text = text[(len(text) - width):]
            if color:
                text = color + text + "|n"
            return text

