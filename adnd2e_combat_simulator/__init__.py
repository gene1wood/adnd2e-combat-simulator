from __future__ import division
from colorama import init as colorama_init, Fore, Back, Style
# pip install colorama
import random
import yaml # pip install PyYAML
import dice # pip install dice
import copy
import sys

colorama_init(autoreset=True)

class Manager:
    def __init__(self):
        self.SIZES = ['sm', 'l']

    def load_combatants(self):
        try:
            with open('combatants.yaml') as f:
                combatants = yaml.safe_load(f)
        except IOError:
            print("Missing combatants.yaml file")
            print("Make sure to configure your combatants first.")
            exit(1)

        players = combatants['players']
        monsters = combatants['monsters']

        for player in players:
            players[player]['current_hp'] = players[player]['hp']
            if 'size' not in players[player]:
                players[player]['size'] = 'm'

        x = {}
        for monster in monsters:
            if 'qty' not in monsters[monster]:
                monsters[monster]['qty'] = 1
            if monsters[monster]['qty'] > 1:
                for i in range(1, monsters[monster]['qty'] + 1):
                    x["%s %s" %
                      (monster, i)] = copy.deepcopy(monsters[monster])
            elif monsters[monster]['qty'] == 1:
                x[monster] = copy.deepcopy(monsters[monster])
        monsters = x

        for monster in monsters:
            if 'size' not in monsters[monster]:
                monsters[monster]['size'] = 'm'
            hd = [x.strip() for x in monsters[monster]['hd'].split('+')]
            hd_dice = hd[0]
            if 'd' not in hd_dice:
                hd_dice = "%sd8" % hd_dice
            hd_mod = hd[1] if len(hd) == 2 else 0
            monsters[monster]['hp'] = int(dice.roll('%s + %s' %
                                                    (hd_dice, hd_mod)))
            monsters[monster]['current_hp'] = monsters[monster]['hp']

        return players, monsters

    def get_attacks(self, combatant, rnd):
        # type: (dict, int) -> list
        attacks = []
        for attack_type in combatant['attack']:
            attack = next(x for x
                          in combatant['attacks']
                          if x['name'] == attack_type)
            if 'rof' in attack and '/' not in attack['rof']:
                attack['rof'] = '%s/1' % attack['rof']
            else:
                attack['rof'] = '1/1'

            numerator, denominator = [int(x.strip())
                                      for x in attack['rof'].split('/')]
            if rnd % denominator == 0:
                attacks.extend([attack] * (numerator // denominator))
            else:
                attacks.extend(
                    [attack] * (numerator - (numerator // denominator)))
        return attacks

    def fight(self,
              attackers,
              attacker,
              defenders,
              defender,
              rnd):
        # type: (dict, str, dict, str, int) -> int
        damages = []
        for attack in self.get_attacks(attackers[attacker],
                                       rnd):
            tohit = attackers[attacker]['thac0']
            if 'tohit' in attack:
                tohit -= sum(attack['tohit'].values())

            if type(defenders[defender]['ac']) == int:
                tohit -= defenders[defender]['ac']
            elif type(defenders[defender]['ac']) == dict:
                tohit -= 10 - sum(defenders[defender]['ac'].values())
            else:
                raise (Exception("ac doesn't make sense"))

            tohitroll = int(dice.roll('d20'))
            if tohitroll >= tohit or tohitroll == 20:
                if type(attack['damage']) == str:
                    damage = (int(dice.roll(attack['damage'])) *
                              (2 if tohitroll == 20 else 1))
                elif type(attack['damage']) == dict:
                    damage_mod = sum([attack['damage'][x] for x
                                      in attack['damage']
                                      if x not in self.SIZES])
                    if defenders[defender]['size'] not in ''.join(self.SIZES):
                        raise (Exception("Size %s isn't recognized" %
                                         defenders[defender]['size']))
                    for size in self.SIZES:
                        if defenders[defender]['size'] in size:
                            try:
                                damage = int(dice.roll(
                                    attack['damage'][size]))
                                damage += damage_mod
                                damage *= 2 if tohitroll == 20 else 1
                            except:
                                print(type(damage_mod))
                                raise
                else:
                    raise (Exception("damage is unknown"))
            else:
                damage = 0
            damages.append(damage)
            hits_or_misses = (Style.BRIGHT + Fore.YELLOW + 'hits'
                              if damage > 0 else
                              'misses') + Style.RESET_ALL
            hp = (Style.BRIGHT + Fore.YELLOW +
                  "for %s points of damage " % str(damage) + Style.RESET_ALL
                  if damage > 0 else '')
            print("%s(%s/%s) %s %s(%s/%s) with %s %s("
                  "rolled %s to hit %s)" %
                  (attacker,
                   attackers[attacker]['current_hp'],
                   attackers[attacker]['hp'],
                   hits_or_misses,
                   defender,
                   defenders[defender]['current_hp'],
                   defenders[defender]['hp'],
                   attack['name'],
                   hp,
                   tohitroll,
                   tohit))
        return sum(damages)

    def do_battle(self, players, monsters):
        print("%s vs %s" % (players.keys(), monsters.keys()))

        rnd = 0
        while (len(players) > 0 and
               len(monsters) > 0):
            rnd += 1
            players = {x: players[x]
                       for x in players.keys()
                       if players[x]['current_hp'] > 0}
            monsters = {x: monsters[x]
                        for x in monsters.keys()
                        if monsters[x]['current_hp'] > 0}

            for attackers, defenders in [(players, monsters),
                                         (monsters, players)]:
                for attacker in attackers:
                    if len(defenders) > 0:
                        defender = random.choice(list(defenders.keys()))
                        damage = self.fight(attackers,
                                            attacker,
                                            defenders,
                                            defender,
                                            rnd)
                        defenders[defender]['current_hp'] -= damage
                        if defenders[defender]['current_hp'] <= 0:
                            print(Style.BRIGHT + Fore.RED + "%s dies" %
                                  defender)
                            del defenders[defender]
                    else:
                        break
        print("Players left alive are %s" % players.keys())
        print("Monsters left alive are %s" % monsters.keys())
        return ('players' if len(players) > 0 else 'monsters'), rnd

    def do_war(self, battles):
        players, monsters = self.load_combatants()
        results = {'players': 0, 'monsters': 0}
        rounds_list = []
        for i in range(0, battles):
            winner, rounds = self.do_battle(players, monsters)
            results[winner] += 1
            rounds_list.append(rounds)
        print("######################")
        print("Average fight duration : %s rounds" %
              (sum(rounds_list) / len(rounds_list)))
        print("Final results: %s" % results)


def main():
    if len(sys.argv) == 2:
        battles = int(sys.argv[1])
    else:
        battles = 1
    m = Manager()
    m.do_war(battles)

if __name__ == '__main__':
    main()
