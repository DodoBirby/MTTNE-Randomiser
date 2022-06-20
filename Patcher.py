import shutil
import os

half_n = 2**31
n = half_n * 2
def normalise(value):
    return (value + half_n) % n - half_n

def patch(infile, outfile, itemDict):
    workingDir = os.getcwd()
    tempfile = shutil.copy(infile, workingDir + "/temp.dat")
    dictList = list(itemDict)
    with open(tempfile, "rb+") as f:
        for i in dictList:
            f.seek(i)
            value = int.to_bytes(itemDict[i], 1, 'little')
            f.write(value)


#Encoding code, basically assembler
    counter = 0
    mult = 84
    exp = 225

    with open(tempfile, "rb") as f:

        size = os.path.getsize(tempfile)
        if os.path.exists(outfile):
            os.remove(outfile)
        output = open(outfile, "ab")
        while counter < size:
            char = f.read(1)
            char = int.from_bytes(char, 'little')
            counter += 1
            ecx = mult
            eax = 0x66666667
            edx = eax * ecx >> 32
            edx = edx // 2
            eax = ecx
            eax = eax // 2**31
            ebx = edx
            ebx -= eax
            ecx = exp
            eax = 0x4bda12f7
            edx = eax * ecx >> 32
            edx = edx // 2**3
            eax = ecx
            eax = eax // 2**31
            edx -= eax
            eax = edx
            dl = ebx % 256
            dl -= eax % 256
            signextended = char
            if char >= 0x80:
                signextended = 0xffffff << 8
                signextended += char
                signextended = int.to_bytes(signextended, 4, 'little')
                signextended = int.from_bytes(signextended, 'little', signed=True)
            eax = char - dl
            storage = eax % 256
            mult += signextended
            eax = (signextended + 7) * counter
            exp += eax
            exp = normalise(exp)
            output.write(int.to_bytes(storage, 1, 'little'))
        output.close()
    os.remove(tempfile)


