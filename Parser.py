import random
class LogicReader:
    def __init__(self):
        self.definitions = set([])
        self.requirements = {}
        self.accessible_locations = []

    def get_requirements(self, filepath):
        with open(filepath, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if not line or line[0] == "#":
                    continue
                
                while '  ' in line:
                    line = line.replace('  ', ' ')
                
                if line.startswith(".def "):
                    line = line[5:]
                    definition = True
                else:
                    definition = False
                
                label, reqs = line.split(' ', 1)

                if definition:
                    self.definitions.add(label)
                reqs = reqs.replace(' ', '')
                self.requirements[label] = reqs

    #label is location to evaluate
    #items is a set containing current accessible items
    #currentItem is the current item being placed
    def evaluate_requirements(self, label, items, currentItem=set([])):
        reqs = self.requirements[label]
        if reqs == "*":
            return True
        for or_cond in reqs.split('|'):
            subreqs = []
            for and_cond in or_cond.split('&'):
                #Escape Check Logic
                if and_cond[0] == "E":
                    if and_cond[1:] in self.definitions:
                        subreqs.append(self.evaluate_requirements(and_cond[1:], items.union(currentItem)))
                    else:
                        subreqs.append(int(and_cond[1:], 0x10) in items.union(currentItem))
                
                elif and_cond in self.definitions:
                    subreqs.append(self.evaluate_requirements(and_cond, items))
                else:
                    subreqs.append(int(and_cond, 0x10) in items)
            if all(subreqs):
                return True
        return False

    def get_locations(self):
        return [loc for loc in self.requirements.keys() if not loc in self.definitions]

    def calc_accessible_locations(self, items, currentItem=set([])):
        self.accessible_locations = []
        for loc in self.get_locations():
            if self.evaluate_requirements(loc, items, currentItem):
                self.accessible_locations.append(loc)

    def is_progression(self, items, item):
        self.old_accessible = self.accessible_locations
        self.calc_accessible_locations(items.union(item))
        ret = len([loc for loc in self.accessible_locations if not loc in self.old_accessible]) > 0
        self.accessible_locations = self.old_accessible
        return ret

    def calc_placeable_locations(self, items, item):
        self.calc_accessible_locations(items, item)

    def delete_item_loc(self, label):
        del self.requirements[label]


