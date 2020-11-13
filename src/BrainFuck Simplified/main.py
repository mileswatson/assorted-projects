slotnames = dict()
file = open("brainfuck.bfs", "r")
source = file.read()
file.close()

source = source.replace(" ", "~").replace("\n", "~").replace("\t", "~")
location = 0
tempstr = ""
for char in source:
    if char in "<>+-.,[]#()~@0123456789":
        if tempstr != "":
            if not tempstr in slotnames:
                slotnames[tempstr] = location
                location += 1
            tempstr = ""
    else:
        tempstr += char
if tempstr != "":
    if not tempstr in slotnames:
        slotnames[tempstr] = location
        location += 1
currentlocation = 0
finalsource = ""
tempstr = ""
i = 0
while i < len(source):
    char = source[i]
    if char in "<>+-.,[]#()0123456789@~":
        if tempstr in slotnames:
            x = slotnames[tempstr] - currentlocation
            currentlocation = slotnames[tempstr]
            # print(x)
            if x > 0:
                for j in range(x):
                    finalsource += ">"
            else:
                for j in range(-x):
                    finalsource += "<"
            tempstr = ""
        if char == "(":
            subsrc = ""
            iterstring = "0"
            while source[i] not in "0123456789)":
                i += 1
                if source[i] in "<>+-.,[]#":
                    subsrc += source[i]
            while source[i] != ")":
                if source[i] in "0123456789":
                    iterstring += source[i]
                i += 1
            finalsource += subsrc * int(iterstring)
        elif char == "@":
            i += 1
            finalsource += "+" * ord(source[i].encode("ascii"))
        elif char != "~":
            finalsource += char
        if char == "<":
            currentlocation -= 1
        elif char == ">":
            currentlocation += 1
    else:
        tempstr += char
    i += 1
while "+-" in finalsource or "-+" in finalsource or "<>" in finalsource or "><" in finalsource:
    finalsource = finalsource.replace("+-", "").replace("-+", "").replace("<>", "").replace("><", "")
compiled = ""
i = 0
for char in finalsource:
    compiled += char
    i += 1
    if i == 50:
        i = 0
        compiled += "\n"
file = open("brainfuckcompiled.bf", "w")
file.write(compiled)
file.close()