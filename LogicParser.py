class LogicReader:
    def __init__(self, requirefile):
        self.requirements = {}
        self.definitions = set([])
        with open(requirefile, "r") as f:
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
                self.requirements[label] = reqs

    def get_locations(self):
        return [loc for loc in self.requirements.keys() if not loc in self.definitions]

    def evaluate_requirements(self, label, items, currentItem=0):
        reqs = self.requirements[label]
        if reqs == "*":
            return True
        for or_cond in reqs.split('|'):
            subreqs = []
            for and_cond in or_cond.split('&'):
                itemscopy = items.copy()
                if and_cond[0] == "N":
                    num, thing = and_cond[1:].split(' ', 1)
                    num = int(num, 0x10)
                    thing = int(thing, 0x10)
                    count = items.count(thing)
                    subreqs.append(count >= num)
                elif and_cond[0] == 'E':
                    itemscopy.append(currentItem)
                    if and_cond[1:] in self.definitions:
                        subreqs.append(self.evaluate_requirements(and_cond[1:], itemscopy))
                    else:
                        subreqs.append(int(and_cond[1:], 0x10) in itemscopy)
                elif and_cond in self.definitions:
                    subreqs.append(self.evaluate_requirements(and_cond, items))
                else:
                    subreqs.append(int(and_cond, 0x10) in items)
            if all(subreqs):
                return True
        return False

    def calc_accessible_locations(self, items, itemDict):
        accessible_locations = []
        for loc in self.get_locations():
            currentItem = itemDict[int(loc, 0x10)]
            if self.evaluate_requirements(loc, items, currentItem):
                accessible_locations.append(loc)
        return accessible_locations

    def calc_accessible_locations_seedless(self, items):
        accessible_locations = []
        for loc in self.get_locations():
            if self.evaluate_requirements(loc, items):
                accessible_locations.append(loc)
        return accessible_locations
