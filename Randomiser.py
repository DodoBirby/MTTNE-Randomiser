import random
import os
import sys
def randomiser(seed, missiles, powerBombs, supers, magShields, eTanks):
    if seed != "":
        random.seed(seed)
    else:
        seed = random.randrange(0, sys.maxsize)
        random.seed(seed)
    #Original Missile count is 50
    #missiles = 46
    #powerBombs = 16
    #supers = 20
    #magShields = 14
    #eTanks = 14

    setMissiles = missiles
    setPowerBombs = powerBombs
    setSupers = supers
    setShield = magShields
    setETanks = eTanks

    itemDict = {
    0x13F: 0,
    0x257: 0,
    0x25E: 0,
    0x38B: 0x10,
    0x480: 0,
    0x5BB: 0,
    0x6B7: 0,
    0x6CC: 0,
    0x7B3: 0,
    0x8CB: 0,
    0x9FF: 0,
    0xA0D: 0,
    0xC3D: 0,
    0xC44: 0,
    0xF7E: 0x0c,
    0x10C0: 0,
    0x1199: 0,
    0x11A7: 0,
    0x12B1: 0,
    0x12B8: 0x23,
    0x12BF: 0x23,
    0x12C6: 0,
    0x13C2: 0,
    0x150B: 0,
    0x15F2: 0,
    0x160E: 0x23,
    0x1615: 0,
    0x1750: 0,
    0x1830: 0,
    0x1837: 0,
    0x183E: 0x23,
    0x1948: 0,
    0x1A60: 0,
    0x1B7F: 0x23,
    0x1B86: 0,
    0x1C82: 0,
    0x1C97: 0,
    0x1D9A: 0,
    0x1DBD: 0,
    0x1DC4: 0,
    0x1ECE: 0x23,
    0x1EF1: 0x23,
    0x1FD8: 0x23,
    0x20F0: 0x23,
    0x210C: 0,
    0x2113: 0x23,
    0x21FA: 0,
    0x220F: 0,
    0x268B: 0x23,
    0x2772: 0x24,
    0x2780: 0,
    0x2787: 0,
    0x278E: 0,
    0x29B7: 0x24,
    0x29BE: 0,
    0x2CF8: 0,
    0x2CFF: 0x24,
    0x2E17: 0,
    0x2F2F: 0,
    0x3032: 0,
    0x304E: 0,
    0x314A: 0,
    0x3158: 0,
    0x315F: 0x24,
    0x3166: 0,
    0x3262: 0,
    0x3381: 0x24,
    0x35AA: 0,
    0x35B1: 0,
    0x35BF: 0,
    0x36D0: 0,
    0x37E8: 0,
    0x33B9: 0,
    0x35E2: 0,
    0x3701: 0,
    0x380B: 0,
    0x3915: 0,
    0x3B22: 0,
    0x3C3A: 0,
    0x3C79: 0,
    0x3D6E: 0,
    0x3E94: 0,
    0x3F97: 0,
    0x3FB3: 0,
    0x41C7: 0,
    0x450F: 0,
    0x4620: 0,
    0x462E: 0,
    0x463C: 0,
    0x4731: 0,
    0x475B: 0,
    0x4865: 0,
    0x4A9C: 0,
    0x4AA3: 0,
    0x624: 0,
    0x73C: 0,
    0xCB4: 0,
    0xCBB: 0,
    0xDB0: 0,
    0xEF9: 0,
    0xFF5: 0,
    0x1011: 0,
    0x1130: 0,
    0x122C: 0,
    0x1344: 0,
    0x1416: 0,
    0x153C: 0,
    0x1582: 0,
    0x1597: 0,
    0x164D: 0,
    0x1765: 0,
    0x177A: 0,
    0x179D: 0,
    0x17C0: 0,
    0x18B5: 0,
    0x18C3: 0,
    0x18CA: 0,
    0x19DB: 0,
    0x19FE: 0,
    0x1C12: 0,
    0x1C3C: 0,
    0x1D07: 0,
    0x1D1C: 0,
    0x1D38: 0,
    0x3525: 0,
    0x3970: 0,
    0x3985: 0,
    0x3A9D: 0,
    0x3BB5: 0,
    0x3BCA: 0,
    0x3CD4: 0,
    0x3CDB: 0,
    0x3DDE: 0,
    0x3DF3: 0,
    0x4007: 0,
    0x4134: 0,
    0x4483: 0,
    0x1E11: 0,
    0x1E18: 0,
    0x1F1B: 0,
    0x1F4C: 0,
    0x1F6F: 0,
    0x2079: 0,
    0x224E: 0,
    0x22BE: 0,
    0x23B3: 0,
    0x24D9: 0,
    0x24EE: 0,
    0x25EA: 0,
    0x260D: 0,
    0x2836: 0,
    0x2924: 0,
    0x2940: 0,
    0x2A4A: 0,
    0x2A5F: 0
    }
    dictList = list(itemDict)
    totalMinors = missiles + powerBombs + supers + magShields + eTanks
    while totalMinors > 0:
        totalMinors = missiles + powerBombs + supers + magShields + eTanks
        rand = random.randint(0, 4)
        success = False
        if rand == 0:
            if missiles > 0:
                missiles -= 1
                while not success:
                    rand = random.randint(0, len(itemDict)-1)
                    if itemDict[dictList[rand]] == 0:
                        itemDict[dictList[rand]] = 0x1f
                        success = True
            continue
        if rand == 1:
            if powerBombs > 0:
                powerBombs -= 1
                while not success:
                    rand = random.randint(0, len(itemDict)-1)
                    if itemDict[dictList[rand]] == 0:
                        itemDict[dictList[rand]] = 0x22
                        success = True
            continue
        if rand == 2:
            if supers > 0:
                supers -= 1
                while not success:
                    rand = random.randint(0, len(itemDict)-1)
                    if itemDict[dictList[rand]] == 0:
                        itemDict[dictList[rand]] = 0x20
                        success = True
            continue
        if rand == 3:
            if magShields > 0:
                magShields -= 1
                while not success:
                    rand = random.randint(0, len(itemDict)-1)
                    if itemDict[dictList[rand]] == 0:
                        itemDict[dictList[rand]] = 0x21
                        success = True
            continue
        if rand == 4:
            if eTanks > 0:
                eTanks -= 1
                while not success:
                    rand = random.randint(0, len(itemDict)-1)
                    if itemDict[dictList[rand]] == 0:
                        itemDict[dictList[rand]] = 0x1e
                        success = True
            continue
    #Major time
    majors = [*range(0x02, 0x1B)]
    majors.remove(0x10)
    majors.remove(0x0c)
    majors.append(0x08)
    majors.append(0x08)
    majors.append(0x0d)
    majors.append(0x0d)

    while len(majors) > 0:
        rand = random.randint(0, len(majors)-1)
        curItem = majors[rand]
        del majors[rand]
        success = False
        while not success:
            rand = random.randint(0, len(itemDict)-1)
            if itemDict[dictList[rand]] == 0:
                itemDict[dictList[rand]] = curItem
                success = True


    #Spoiler File
    workingDir = os.getcwd()
    with open(workingDir + '/spoiler_' + str(seed) + ".txt", "w") as f:
        f.write("This file is not intended to be readable... yet\n")
        f.write("Seed: " + str(seed) + "\n")
        f.write("Missiles: " + str(setMissiles) + "\n")
        f.write("Supers: " + str(setSupers) + "\n")
        f.write("Power Bombs: " + str(setPowerBombs) + "\n")
        f.write("Shields: " + str(setShield) + "\n")
        f.write("E-Tanks: " + str(setETanks) + "\n")
        for i in dictList:
            f.write(str(i) + ":" + str(itemDict[i]) + "\n")
    
    return itemDict
    #Patching code
    #with open("decoded.dat", "rb+") as f:
        #for i in dictList:
           # f.seek(i)
          #  value = int.to_bytes(itemDict[i], 1, 'little')
           # f.write(value)
    








