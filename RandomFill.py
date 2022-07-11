from ItemDict import ItemDictMaker
from LogicParser import LogicReader
import random
import Patcher
import os
class RandomFiller:
    def __init__(self, seed):
        random.seed(seed)
        self.generation_progress = 0


    def place_early_morph(self, itemDict):
        morph_locations = ["38b", "c44"]
        rand = random.randint(0, len(morph_locations)-1)
        rand = morph_locations[rand]
        itemDict[int(rand, 0x10)] = 0x10

    def place_early_movement(self, itemDict):
        asteroid_locations = ["38b",  "c44", "c3d", "f7e", "9ff"]
        potential_movement = [0x0c, 0x0e, 0x0f, 0x13, 0x11, 0x14, 0x0e]
        success = False
        while not success:
            rand = random.randint(0, len(asteroid_locations)-1)
            rand = asteroid_locations[rand]
            movement = random.randint(0, len(potential_movement)-1)
            movement = potential_movement[movement]
            if itemDict[int(rand, 0x10)] == 0:
                itemDict[int(rand, 0x10)] = movement
                success = True
        return movement

    def generate_game(self, missiles, supers, powbombs, shields, energy):
        itemDict = itemd.generateItemDict()
        dictList = list(itemDict.keys())
        itempool = [*range(0x02, 0x1b)]
        itempool.remove(0x10)
        self.place_early_morph(itemDict)
        movement = self.place_early_movement(itemDict)
        itempool.remove(movement)
        for i in range(missiles):
            itempool.append(0x1f)
        for i in range(supers):
            itempool.append(0x20)
        for i in range(powbombs):
            itempool.append(0x22)
        for i in range(shields):
            itempool.append(0x21)
        for i in range(energy):
            itempool.append(0x1e)
        for i in range(5):
            success = False
            while not success:
                loc = random.randint(0, len(self.gear_locations)-1)
                if itemDict[int(self.gear_locations[loc], 0x10)] == 0:
                    itemDict[int(self.gear_locations[loc], 0x10)] = 0x24
                    success = True
        for i in range(11):
            success = False
            while not success:
                loc = random.randint(0, len(self.keycard_locations)-1)
                if itemDict[int(self.keycard_locations[loc], 0x10)] == 0:
                    itemDict[int(self.keycard_locations[loc], 0x10)] = 0x23
                    success = True
        
        while len(itempool) > 0:
            success = False
            while not success:
                rand = random.randint(0, len(itempool)-1)
                loc = random.randint(0, len(dictList)-1)
                if itemDict[dictList[loc]] == 0:
                    itemDict[dictList[loc]] = itempool[rand]
                    del itempool[rand]
                    success = True
        return itemDict

    def check_if_completable(self, itemDict):
        items = []
        lr = LogicReader("requirements.txt")
        oldLocations = set([])
        locations = set([])
        completable = True
        while len(locations) != len(lr.get_locations()):
            locations = lr.calc_accessible_locations(items, itemDict)
            if len(locations) > self.generation_progress:
                self.generation_progress = len(locations)
                os.system('cls')
                print("Progress: " + str(self.generation_progress))
                
            if oldLocations == locations:
                completable = False
                break
            oldLocations = locations.copy()
            items = []
            for loc in locations:
                item = itemDict[int(loc, 0x10)]
                items.append(item)
        return completable

    def get_gear_locations(self, missiles, supers, powbombs, shields, energy):
        items = [*range(0x02, 0x1b)]
        for i in range(missiles):
            items.append(0x1f)
        for i in range(supers):
            items.append(0x20)
        for i in range(powbombs):
            items.append(0x22)
        for i in range(shields):
            items.append(0x21)
        for i in range(energy):
            items.append(0x1e)
        for i in range(11):
            items.append(0x23)
        lr = LogicReader("requirements.txt")
        accessible_locations = lr.calc_accessible_locations_seedless(items)
        return accessible_locations

    def get_keycard_locations(self, missiles, supers, powbombs, shields, energy):
        items = [*range(0x02, 0x1b)]
        for i in range(missiles):
            items.append(0x1f)
        for i in range(supers):
            items.append(0x20)
        for i in range(powbombs):
            items.append(0x22)
        for i in range(shields):
            items.append(0x21)
        for i in range(energy):
            items.append(0x1e)
        for i in range(5):
            items.append(0x24)
        lr = LogicReader("requirements.txt")
        accessible_locations = lr.calc_accessible_locations_seedless(items)
        return accessible_locations
    
    def generate_spoiler_log(self, itemDict, seed, missiles, supers, powbombs, shields, energy):
        workingDir = os.getcwd()
        with open(workingDir + '/spoiler_' + str(seed) + '.txt', 'w') as f:
            f.write("This file is not intended to be readable... yet\n")
            f.write("Seed: " + str(seed) + "\n")
            f.write("Missiles: " + str(missiles) + "\n")
            f.write("Supers: " + str(supers) + "\n")
            f.write("Power Bombs: " + str(powbombs) + "\n")
            f.write("Shields: " + str(shields) + "\n")
            f.write("E-Tanks: " + str(energy) + "\n")
            items = []
            lr = LogicReader("requirements.txt")
            locations = set([])
            oldLocations = set([])
            sphere = -1
            while len(locations) != len(lr.get_locations()):
                sphere += 1
                f.write("Sphere " + str(sphere) + ":\n")
                locations = lr.calc_accessible_locations(items, itemDict)
                items = []
                for loc in locations:
                    item = itemDict[int(loc, 0x10)]
                    items.append(item)
                    if not loc in oldLocations:
                        f.write(hex(int(loc, 0x10)) + ": " + hex(item) + "\n")
                oldLocations = locations.copy()
                

def randomise(seed, missiles, supers, powbombs, shields, energy):
    global itemd
    if seed == "":
            seed = random.randint(0, 999999999)
    itemd = ItemDictMaker()
    filler = RandomFiller(seed)
    filler.gear_locations = filler.get_gear_locations(missiles, supers, powbombs, shields, energy)
    filler.keycard_locations = filler.get_keycard_locations(missiles, supers, powbombs, shields, energy)
    completable = False
    while not completable:
        itemDict = filler.generate_game(missiles, supers, powbombs, shields, energy)
        completable = filler.check_if_completable(itemDict)
    filler.generate_spoiler_log(itemDict, seed, missiles, supers, powbombs, shields, energy)
    print("Finished Generating")
    print("Making Output File")
    return itemDict

