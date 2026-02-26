byteList = []
pointer = 0
pointerFileMode = 0

currentMode = 0
for i in range(1000):
    byteList.append(0)

commands = []
commandIndex = 0
jumps = []
lastJumps = []

with open("input.iusearchbtw", "r") as f:
    tempCommands = f.read().split("\n")
    for command in tempCommands:
        if command.startswith("#"):
            continue
        command = command.split(" ")
        commands.extend(command)

with open('input.txt', 'r') as file:
    content = file.read()
    fileByteList = [ord(char) for char in content]
    fileByteList.append(0)

while commandIndex < len(commands):
    

    currentCommand = commands[commandIndex].lower()
    if currentCommand not in ["i", "use", "arch", "by", "the", "way", "[", "]", ""]:
        exit(f"No such command: {currentCommand} at index {commandIndex}")

    if currentCommand == "the":
        currentMode = (currentMode + 1) % 2

    if currentMode == 0:
        if currentCommand == "i":
            byteList[pointer] += 1
        elif currentCommand == "use":
            byteList[pointer] -= 1
        elif currentCommand == "arch":
            pointer += 1
        elif currentCommand == "by":
            pointer -= 1
        elif currentCommand == "way":
            print(chr(byteList[pointer]), end="")
    elif currentMode == 1:
        if currentCommand == "arch":
            pointerFileMode += 1
        elif currentCommand == "by":
            pointerFileMode -= 1
        elif currentCommand == "way":
            if 0 <= pointerFileMode < len(fileByteList):  # Ensure pointerFileMode is within bounds
                byteList[pointer] = fileByteList[pointerFileMode]

    jump = False
    if currentCommand == "[":
        zero = False
        if currentMode == 0:
            if byteList[pointer] == 0:
                zero = True
        elif currentMode == 1:
            if fileByteList[pointerFileMode] == 0:
                zero = True
        if zero and len(lastJumps) > 0:
            jump = True
            commandIndex = lastJumps[-1] + 1
            lastJumps.pop()
        else:
            jumps.append(commandIndex)
    if currentCommand == "]":
        jump = True
        if jumps:
            lastJumps.append(commandIndex)
            commandIndex = jumps[-1]
            jumps.pop()
    if not jump:
        commandIndex += 1