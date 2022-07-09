from Parser import LogicReader
import random
import os
from ItemDict import ItemDictMaker
itemd = ItemDictMaker()


class RoutingError(Exception):
    pass



class Generator:
    def __init__(self):
        self.itemDict = itemd.generateItemDict()
        self.items = set([])
        self.missiles = 50
        self.supers = 20
        self.energy = 14
        self.shields = 14
        self.powbombs = 16

    def write_item(self, label, item):
        label = int(label, 0x10)
        self.itemDict[label] = item
        self.items.add(item)

    def write_gear(self, label, item):
        label = int(label, 0x10)
        self.itemDict[label] = item

    def no_logic_generate(self):
        print("Objective Complete: Filling rest of items")
        missiles = self.missiles
        supers = self.supers
        shields = self.shields
        energy = self.energy
        powbombs = self.powbombs
        majorsLeft = self.majorsLeft
        totalMinors = missiles + supers + shields + energy + powbombs
        keylist = list(self.itemDict.keys())
        while totalMinors > 0:
            success = False
            rand = random.randint(0, 4)
            if rand == 0:
                if missiles > 0:
                    missiles -= 1
                    while not success:
                        rand = random.randint(0, len(keylist)-1)
                        rand = keylist[rand]
                        if self.itemDict[rand] == 0:
                            self.itemDict[rand] = 0x1f
                            success = True
            elif rand == 1:
                if supers > 0:
                    supers -= 1
                    while not success:
                        rand = random.randint(0, len(keylist)-1)
                        rand = keylist[rand]
                        if self.itemDict[rand] == 0:
                            self.itemDict[rand] = 0x20
                            success = True
            elif rand == 2:
                if shields > 0:
                    shields -= 1
                    while not success:
                        rand = random.randint(0, len(keylist)-1)
                        rand = keylist[rand]
                        if self.itemDict[rand] == 0:
                            self.itemDict[rand] = 0x21
                            success = True
            elif rand == 3:
                if energy > 0:
                    energy -= 1
                    while not success:
                        rand = random.randint(0, len(keylist)-1)
                        rand = keylist[rand]
                        if self.itemDict[rand] == 0:
                            self.itemDict[rand] = 0x1e
                            success = True
            elif rand == 4:
                if powbombs > 0:
                    powbombs -= 1
                    while not success:
                        rand = random.randint(0, len(keylist)-1)
                        rand = keylist[rand]
                        if self.itemDict[rand] == 0:
                            self.itemDict[rand] = 0x22
                            success = True
            totalMinors = missiles + supers + shields + energy + powbombs
        #Generate Majors
        
        while len(majorsLeft) > 0:
            major = random.randint(0, len(majorsLeft)-1)
            major = majorsLeft[major]
            success = False
            majorsLeft.remove(major)
            while not success:
                rand = random.randint(0, len(keylist)-1)
                rand = keylist[rand]
                if self.itemDict[rand] == 0:
                    self.itemDict[rand] = major
                    success = True

        

    def remove_minor(self, item):
        if item == 0x1f:
            self.missiles -= 1
            return True
        if item == 0x20:
            self.supers -= 1
            return True
        if item == 0x21:
            self.shields -= 1
            return True
        if item == 0x22:
            self.powbombs -= 1
            return True
        return False

    def place_early_morph(self):
        morph_locations = ["38b", "c44"]
        rand = random.randint(0, len(morph_locations)-1)
        rand = morph_locations[rand]
        self.itemDict[int(rand, 0x10)] = 0x10
        self.items.add(0x10)
        return rand

    def generate_spoiler_file(self, missiles, supers, energy, powbombs, shields):
        workingDir = os.getcwd()
        with open(workingDir + '/spoiler_' + str(self.seed) + ".txt", "w") as f:
            f.write("This file is not intended to be readable... yet\n")
            f.write("Seed: " + str(self.seed) + "\n")
            f.write("Missiles: " + str(missiles) + "\n")
            f.write("Supers: " + str(supers) + "\n")
            f.write("Power Bombs: " + str(powbombs) + "\n")
            f.write("Shields: " + str(shields) + "\n")
            f.write("E-Tanks: " + str(energy) + "\n")
            for i in list(self.itemDict.keys()):
                f.write(str(hex(i)) + ":" + str(hex(self.itemDict[i])) + "\n")


    def generate_game(self, seed, missiles, supers, energy, powbombs, shields):
        self.missiles = missiles
        self.supers = supers
        self.energy = energy
        self.powbombs = powbombs
        self.shields = shields
        self.seed = seed
        if self.seed == "":
            self.seed = random.randint(0, 9999999999)
        random.seed(self.seed)
        tries = 0
        lr = LogicReader()
        path = "requirements.txt"
        lr.get_requirements(path)
        self.majorsLeft = [*range(0x02, 0x1b)]
        randomitempool = [*range(0x02, 0x1b), 0x1f, 0x20, 0x21, 0x22, 0x24, 0x24, 0x24, 0x24]
        if self.missiles == 0:
            randomitempool.remove(0x1f)
        if self.shields == 0:
            randomitempool.remove(0x21)
        #Seed is impossible without supers or powerbombs but the customer is always right...
        if self.supers == 0:
            randomitempool.remove(0x20)
        if self.powbombs == 0:
            randomitempool.remove(0x22)
        generating = True
        loc = self.place_early_morph()
        lr.delete_item_loc(loc)
        self.majorsLeft.remove(0x10)
        randomitempool.remove(0x10)
        while generating:
            lr.calc_accessible_locations(self.items)
            rand = random.randint(0, len(randomitempool)-1)
            rand = randomitempool[rand]
            if rand == 0x24:
                if len(lr.accessible_locations) >= 5:
                    if lr.evaluate_requirements("astescape", self.items):
                        randomitempool = [x for x in randomitempool if x != 0x24]
                        for i in range(5):
                            lr.calc_accessible_locations(self.items)
                            loc = random.randint(0, len(lr.accessible_locations)-1)
                            loc = lr.accessible_locations[loc]
                            lr.delete_item_loc(loc)
                            self.write_gear(loc, 0x24)
                        self.items.add(0x24)
                continue
                        
            if lr.is_progression(self.items, set([rand])):
                tries = 0
                print("Progression item placed")
                minor = self.remove_minor(rand)
                randomitempool.remove(rand)
                if not minor:
                    self.majorsLeft.remove(rand)
                lr.calc_placeable_locations(self.items, set([rand]))
                loc = random.randint(0, len(lr.accessible_locations)-1)
                loc = lr.accessible_locations[loc]
                lr.delete_item_loc(loc)
                self.write_item(loc, rand)
            elif tries > 2000:
                raise RoutingError("Failed to generate")
            else:
                tries += 1
                continue
            if lr.evaluate_requirements("endgame", self.items):
                generating = False
        self.no_logic_generate()
        print("Game Generated, creating output file...")
        self.generate_spoiler_file(missiles, supers, energy, powbombs, shields)
        return self.itemDict













