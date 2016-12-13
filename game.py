# -*- coding: utf-8 -*-
"""
Created on Sat Nov 05 00:58:31 2016

@author: Somak
"""
import numpy as np
"""
There are four Ways men pass through life; 
as warriors, artisans, farmers, and merchants. 
The Farmer sees Spring through to Fall with an eye on the passing seasons
The Merchant obtains ingredients and utilizes them, always living by profit
The Warrior masters the virtue of his weapons, with a taste for strategy
The Artisan is proficient and can map, then execute their projects
"""
from numpy.random import rand

class Person(object): # base person
    def __init__(self):
        # set base stats
        self.name = "unknown"
        self.tool = None
        self.skill = 1.0
        self.physicality = 1.0
        self.luck = 1.0
        self.health = 5.0
        self.specialRoll = False
        self.verbose = True
    
    def reset(self):
        self.tool = None
        self.skill = 1.0
        self.physicality = 1.0
        self.luck = 1.0
        self.health = 5.0
        self.specialRoll = False
        
    def attack(self, opponent, attack="hits"):
        # reset specialRoll
        if self.specialRoll:
            self.specialRoll = False
        
        # special roll odds
        if rand() + (self.luck/7) > 1: 
            self.specialRoll = True
        
        # check for loss
        if self.health < 0:
            if self.verbose: print "%s: You got me, %s" %(self.name, opponent.name)
            return
        
        # how hard do you hit basically
        baseDamage = self.physicality * self.skill * (self.luck/4)
        
        # set crit
        if rand() < (self.luck + self.skill - opponent.skill)/5:
            crit = 2.0
        else:
            crit = 1.0
            
        # determine weapon buff
        #baseDamage = arm(self.tool, baseDamage)
        
        # how much damage your opponent takes all said and done
        endurance = (self.health - opponent.health)
        
        # calc hit / defense rates
        hit = baseDamage * crit
        defense = opponent.skill * opponent.physicality
        
        if endurance > 0: hit -= endurance/2
        else: defense -= -endurance/2
        
        damage = hit * (10-defense)/10
        opponent.health -= damage
        
        # readable output
        if self.verbose: 
            print self.name, attack, opponent.name
            print opponent.name, "took", damage, "and is at", opponent.health, "\n"
            
    def firstStrike(self):
        return rand() * self.luck/2 * self.skill
        
class Farmer(Person):
    def __init__(self):
        super(Farmer, self).__init__()
        self.tool = "Spade"
        self.physicality = 3.0
    
    def reset(self):
        super(Farmer, self).reset()
        self.tool = "Spade"
        self.physicality = 3.0
    
    def attack(self, opponent):
        super(Farmer, self).attack(opponent)
        if self.specialRoll:
            self.physicality += .05
            self.health += .1
        
class Merchant(Person):
    def __init__(self):
        super(Merchant, self).__init__()
        self.tool = "Phone"
        self.skill = 1.5
        self.luck = 2.5
    
    def reset(self):
        super(Merchant, self).reset()
        self.tool = "Phone"
        self.skill = 1.5
        self.luck = 2.5
        
    def attack(self, opponent):
        super(Merchant, self).attack(opponent, "scranbles to strike")
        if self.specialRoll:
            super(Merchant, self).attack(opponent, "scranbles to strike")
            super(Merchant, self).attack(opponent, "scranbles to strike")
            self.luck += .1

class Warrior(Person):
    def __init__(self):
        super(Warrior, self).__init__()
        self.tool = "Katana"
        self.skill = 2.0
        self.physicality = 2.0
    
    def reset(self):
        super(Warrior, self).reset()
        self.tool = "Katana"
        self.skill = 2.0
        self.physicality = 2.0
    
    def attack(self, opponent):
        super(Warrior, self).attack(opponent, "strikes")
        if self.specialRoll:
            self.skill += .1 
            self.physicality += .1
            self.health -= .1

class Artisan(Person):
    def __init__(self):
        super(Artisan, self).__init__()
        self.tool = "Pick"
        self.skill = 2.0
        self.luck = 1.5
        self.physicality = 1.5
    
    def reset(self):
        super(Artisan, self).reset()
        self.tool = "Pick"
        self.skill = 2.0
        self.luck = 1.5
        self.physicality = 1.5
        
    def attack(self, opponent):
        super(Artisan, self).attack(opponent, "lunges at")
        if self.specialRoll:
            self.skill += .05
            self.luck += .25
            super(Artisan, self).attack(opponent, "lunges at")

def arm(tool, baseDamage):
        if tool=="Katana": baseDamage *= 4
        elif tool=="Spade": baseDamage *= 2.25
        elif tool=="Pick": baseDamage *= 2
        return baseDamage
        
def fight(fighter1, fighter2):
    fighter1.reset()
    fighter2.reset()
    if fighter1.verbose and fighter2.verbose:
        print fighter1.name, "is at", fighter1.health
        print "and", fighter2.name, "is at", fighter2.health, "\n"
        health1, health2 = fighter1.health, fighter2.health    
        # determine who strikes first before setting fight cycle    
        if fighter1.firstStrike > fighter2.firstStrike:
            first = fighter1
            second = fighter2
        else:
            first = fighter2
            second = fighter1
        print "**", first.name, "attacks! **"
        while first.health > 0 and second.health > 0:
            first.attack(second)
            second.attack(first)
        # once someone loses, reset health and print winner 
        if second.health < 0:
            first.health = health1
            second.health = health2
            print "**", first.name + " wins **\n"
            return first
        elif first.health < 0:
            first.health = health1
            second.health = health2
            print "**", second.name + " wins **\n"
            return second
        elif second.health == 0:
            first.health = health1
            second.health = health2
            print "**", first.name + " wins **\n"
            return first
        else:
            first.health = health1
            second.health = health2
            print "**", second.name + " wins **\n"
            return second
    else:
        health1, health2 = fighter1.health, fighter2.health    
        # determine who strikes first before setting fight cycle    
        if fighter1.firstStrike > fighter2.firstStrike:
            first = fighter1
            second = fighter2
        else:
            first = fighter2
            second = fighter1
        while first.health > 0 and second.health > 0:
            first.attack(second)
            second.attack(first)
        # once someone loses, reset health and print winner 
        # tie goes to the faster guy / significant win
        if second.health < 0:
            first.health = health1
            second.health = health2
            return first
        elif first.health < 0:
            first.health = health1
            second.health = health2
            return second
        elif second.health == 0:
            first.health = health1
            second.health = health2
            return first
        else:
            first.health = health1
            second.health = health2
            return second

def simpleSim(n):
    shogun, artisan, farmer, merchant = 0.0, 0.0, 0.0, 0.0
    for i in range(n):
        Jeff, Tom = Farmer(), Merchant()
        Jeff.name, Tom.name = "Farmer Jeff", "Merchant Tom"
        Dan, Mike = Warrior(), Artisan()
        Dan.name, Mike.name = "Shogun Dan", "Artisan Mike"
        Jeff.verbose = False
        Tom.verbose = False
        Dan.verbose = False
        Mike.verbose = False
        if fight(fight(Dan, Jeff), fight(Mike, Tom)).name == "Shogun Dan":
            shogun += 1.0
        elif fight(fight(Dan, Jeff), fight(Mike, Tom)).name == "Merchant Tom":
            merchant += 1.0
        elif fight(fight(Dan, Jeff), fight(Mike, Tom)).name == "Artisan Mike":
            artisan += 1.0
        else:
            farmer += 1.0
   
    for i, j in zip([shogun, artisan, farmer, merchant],
                    ['Warrior', 'Artisan', 'Farmer', 'Merchant']):
        print j + ": ", i/(n/100), "%"
    print "\n"

Jeff, Tom = Farmer(), Merchant()
Jeff.name, Tom.name = "Farmer Jeff", "Merchant Tom"
Dan, Mike = Warrior(), Artisan()
Dan.name, Mike.name = "Shogun Dan", "Artisan Mike"

"""
The four characters fight each other in a single elimination tournament, 
printing their attacks as they go
"""
fight(fight(Mike, Tom), fight(Dan, Jeff))


'''
This simulates 1000 randomly generated tournaments 3 times and shows 
the total victories for each class for 3 runthroughs overall

This helps illustrate the level of balance among the classes.

Currently it's roughly at:

Warrior:  32.5 %
Artisan:  24.2 %
Farmer:  26.4 %
Merchant:  16.9 %


Warrior:  32.8 %
Artisan:  22.4 %
Farmer:  27.1 %
Merchant:  17.7 %


Warrior:  34.2 %
Artisan:  21.9 %
Farmer:  26.6 %
Merchant:  17.3 %

considering this is a rudimentary fighting engine for what I'd like to 
make more than a fighting game, I'm pretty okay with this spread for
engagements if there abilities go the other way in the case of different
kinds of competition
'''
#for i in range(3): simpleSim(1000)
