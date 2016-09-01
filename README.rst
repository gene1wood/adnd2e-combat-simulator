Summary
=======

The AD&D Second edition Combat Simulator will run simple simulated battles to
determine the statistical likelyhood of success or failure by the party. The
simulator does not account for player creativity and uses a very simple method
to determine how the battle will go.

Configuration
=============

Add all details about the combatants into the combatants.yaml file. The
example combatants.example.yaml illustrates the syntax

ac
--

The values in the AC dictionary are added together to detemrine the AC. For
example a shield would have an AC value of 1 because it reduces AC by 1.
Studded leather would have a value of 3 because it gives AC 7. If a
combatant had both (3 + 1), their AC would be 6. Default is no modifier or AC
10.

attack
------

This list enumerates the attacks that the combatant will use. The values are
the names of the attacks in the attacks section. Each combatant uses *all* of
their attacks each round. For example a monster with an attack list of "claw",
"claw", "bite" would make all 3 attacks in a single round.

attacks
-------

This list contains all the possible attacks a combatant might use.

damage
~~~~~~

This can either be a string or a dictionary. If it's a string it applies to
targets of all sizes. If it's a dictionary the size of the target is mapped to
a damage string.

tohit
~~~~~

The values in the To Hit dictionary are added together to determine the total
modifier for the to hit role. For example if a fighter specialized in a bastard
sword and had a magical bastard sword +1, the 1 from specialization and 1 from
magic would be added to the d20 die roll. Default is no modifier.

rof
~~~

Rate of fire can be a number of attacks/shots per round (e.g. 2 or 3) or a
ratio of attacks/shots per round (2/1 or 3/2). Default is 1/1.

qty
---

The number of the given type of monster to include in the battle.

hd
--

The hit dice of the monster. This can be a traditional Hit Die number (e.g. 3)
which is the number of 1d8 dice to roll to determine the monsters hit points,
or it can be a traditional Hit Die number with a modifier (e.g. 3 + 2), or it
can just be a description of dice and modifiers (e.g. 1d6 + 2 or 2d8)

Usage
=====

To simulate the war

::

    battle [BATTLES]

The BATTLES argument indicates how many times to simulate the battle. Default
is 1.