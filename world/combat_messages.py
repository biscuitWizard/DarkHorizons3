import re

_COMBAT_RESOLVE_MAP = {
    "strike": {
        "default": {  # Pass, Dodge, Etc
            "success": "[^attacker [^a_verbs at [^defender with [^p [^a_wep, but misses.",
            "failure": "[^attacker hits [^defender with [^p [^a_wep."
        },
        "block": {
            "success": "[^defender blocks [^attacker's [^a_wep with their [^d_wep.",
            "failure": "[^defender tries to block with [^p [^d_wep, but [^attacker hits them with their [^a_wep."
        },
        "riposte": {
            "success": "Success Message",
            "failure": "Failure Message",
            "disrupt": "Disrupt Message"
        }
    },
    "shoot": {
        "default": {  # Pass, Dodge, Etc
            "success": "Success Message",
            "failure": "[^attacker [^a_verbs at [^defender with [^p [^a_wep and hits."
        },
        "quickshot": {
            "success": "[^defender [^a_verbs at [^attacker disrupting [^attacker's attack, but missing them.",
            "failure": "[^defender raises their [^d_wep to fire, but [^attacker's attack hits them.",
            "disrupt": "[^defender [^a_verbs at [^attacker with their [^d_wep, "
                       "hitting [^attacker and disrupting their attack."
        },
        "force_deflect": {
            "success": "Success Message",
            "failure": "Failure Message",
            "disrupt": "Disrupt Message"
        }
    }
}

_RE_COMBAT_TOKENS = re.compile(r'\[\^(attacker|defender|a_wep|d_wep|a_verb)')


class CombatMessageResolver:
    def __init__(self, attacker, defender, attack_action, defend_action, hit_results):
        self.attacker = attacker
        self.defender = defender
        self.attack_action = attack_action
        self.defend_action = defend_action
        self.hit_results = hit_results

    def parse(self):

        if len(self.hit_results) == 0:
            result_success = "success"
        elif all(hit_result.disrupted for hit_result in self.hit_results):
            result_success = "disrupt"
        else:
            result_success = "failure"

        combat_local_map = _COMBAT_RESOLVE_MAP[self.attack_action.key.strip('+')]
        if hasattr(combat_local_map, self.defend_action.verb):
            combat_local_map = combat_local_map[self.defend_action.key.strip('+')]
        else:
            combat_local_map = combat_local_map["default"]

        message = _RE_COMBAT_TOKENS.sub(self._get_combat_token, combat_local_map[result_success])
        return "|r[|yCOMBAT|r]|n {}".format(message)

    def _get_combat_token(self, regex_match):

        typ = regex_match.group()[2:]
        if typ == "attacker":
            return self.attacker.name
        elif typ == "defender":
            return self.defender.name
        elif typ == "a_wep":
            return self.attack_action.weapons[0].name
        elif typ == "d_wep":
            return self.defend_action.weapons[0].name
        elif typ == "a_verb":
            return self.attack_action.verb

        return "[Anomalous match: {}]".format(typ)



