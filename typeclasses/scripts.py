"""
Scripts

Scripts are powerful jacks-of-all-trades. They have no in-game
existence and can be used to represent persistent game systems in some
circumstances. Scripts can also have a time component that allows them
to "fire" regularly or a limited number of times.

There is generally no "tree" of Scripts inheriting from each other.
Rather, each script tends to inherit from the base Script class and
just overloads its hooks to have it perform its function.

"""

from evennia import DefaultScript, create_script


class Script(DefaultScript):
    """
    A script type is customized by redefining some or all of its hook
    methods and variables.

    * available properties

     key (string) - name of object
     name (string)- same as key
     aliases (list of strings) - aliases to the object. Will be saved
              to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     desc (string)      - optional description of script, shown in listings
     obj (Object)       - optional object that this script is connected to
                          and acts on (set automatically by obj.scripts.add())
     interval (int)     - how often script should run, in seconds. <0 turns
                          off ticker
     start_delay (bool) - if the script should start repeating right away or
                          wait self.interval seconds
     repeats (int)      - how many times the script should repeat before
                          stopping. 0 means infinite repeats
     persistent (bool)  - if script should survive a server shutdown or not
     is_active (bool)   - if script is currently running

    * Handlers

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this
                        self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not
                        create a database entry when storing data

    * Helper methods

     start() - start script (this usually happens automatically at creation
               and obj.script.add() etc)
     stop()  - stop script, and delete it
     pause() - put the script on hold, until unpause() is called. If script
               is persistent, the pause state will survive a shutdown.
     unpause() - restart a previously paused script. The script will continue
                 from the paused timer (but at_start() will be called).
     time_until_next_repeat() - if a timed script (interval>0), returns time
                 until next tick

    * Hook methods (should also include self as the first argument):

     at_script_creation() - called only once, when an object of this
                            class is first created.
     is_valid() - is called to check if the script is valid to be running
                  at the current time. If is_valid() returns False, the running
                  script is stopped and removed from the game. You can use this
                  to check state changes (i.e. an script tracking some combat
                  stats at regular intervals is only valid to run while there is
                  actual combat going on).
      at_start() - Called every time the script is started, which for persistent
                  scripts is at least once every server start. Note that this is
                  unaffected by self.delay_start, which only delays the first
                  call to at_repeat().
      at_repeat() - Called every self.interval seconds. It will be called
                  immediately upon launch unless self.delay_start is True, which
                  will delay the first call of this method by self.interval
                  seconds. If self.interval==0, this method will never
                  be called.
      at_stop() - Called as the script object is stopped and is about to be
                  removed from the game, e.g. because is_valid() returned False.
      at_server_reload() - Called when server reloads. Can be used to
                  save temporary variables you want should survive a reload.
      at_server_shutdown() - called at a full server shutdown.

    """
    pass


class SkirmishScript(DefaultScript):
    """
    A skirmish is a group of engagements that are happening in a single location.
    It has a responsibility of tracking all active combatants in a room. When all
    combatants leave the room (or disconnect), the script removes itself.

    In game balance, this is used to adjust fatigue costs in group battles.
    """
    key = "skirmish_script"
    desc = "Used on a room to describe active combat that is happening."
    persistent = True
    interval = 0
    repeats = 0

    combatants = []
    combatant_advantages = dict()

    def add_combatant(self, combatant):
        """

        Args:
            combatant:

        Returns:

        """
        if combatant.id not in self.combatant_advantages:
            self.combatants.append(combatant)
            self.combatant_advantages.append(combatant.id, max([100 - combatant.status.get_wound_sum(), 0]))

    def remove_combatant(self, combatant):
        """

        Args:
            combatant:

        Returns:

        """
        self.combatants.remove(combatant)
        del self.combatant_advantages[combatant.id]
        if self.combatants.count() == 0:
            self.stop()  # delete the script.

    def adjust_advantage(self, combatant, amount):
        """

        Args:
            combatant:
            amount:

        Returns:

        """
        pass

    def get_advantage(self, combatant):
        """

        Args:
            combatant:

        Returns:

        """
        pass

class EngagementScript(DefaultScript):
    key = "engagement_script"
    desc = "Used during an active fight between two characters"
    start_delay = True
    interval = 10
    repeats = 1

    attacker = None  # Who initiated the fight
    defender = None  # Who's the target
    location = None  # Where the fight is happening
    skirmish = None  # What skirmish this engagement belongs to.

    attack_action = None  # Command object for the attack action.
    defender_action = None  # Command object for the defend action.

    def start_engagement(self, attacker, defender, location):
        self.attacker = attacker
        self.defender = defender
        self.location = location

        if not location.skirmish:
            skirmish = create_script(EngagementScript, obj=location)
            location.skirmish = skirmish
            self.skirmish = skirmish
        else:
            self.skirmish = location.skirmish

        self._init_character(attacker)
        self._init_character(defender)

    def clean_engagement(self):
        self._cleanup_character(self.attacker)
        self._cleanup_character(self.defender)
        self.stop()

    def at_repeat(self):
        "Called once after the initial wait delay."
        self.defender.msg('[GAME] You waited too long. Boom! Combat over.')
        self.attacker.msg('[GAME] Your prey took too look to respond. Combat expired.')

        self._cleanup_character(self.attacker)
        self._cleanup_character(self.defender)
        self.stop()

    def _init_character(self, character):
        character.ndb.engagement = self
        character.locaton.skirmish.add_combatant(character)
        if not hasattr(character, 'wounds'):  # If a character doesn't have wounds, give empty ones.
            character.db.wounds = dict()
            for part in self.character.status.get_body_locations():
                character.db.wounds.append(part, list())

    def _cleanup_character(self, character):
        del character.ndb.engagement
        self.attacker.scripts.delete(self.key)
