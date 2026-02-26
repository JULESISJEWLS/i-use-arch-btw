import argparse
import uuid

config = {
    'i': 'add',       # +
    'arch': 'sub',    # -
    'by': 'right',    # >
    'the': 'left',    # <
    'use': 'execute', # 
    'way': 'switch',  # change mod
}

modes =  {
    "0": {
        "add": "call incrementByte",
        "sub": "call decrementByte",
        "right": "call moveRight",
        "left": "call moveLight",
        "execute": "call printByte"
    }
}

def compile(inStr: str, itContent: str) -> str:
    fileBytes = [ord(char) for char in itContent] + [0]
    fileBytes = ", ".join(map(str, fileBytes))
    commands = []
    tempCommands = inStr.split("\n")

    for command in tempCommands:

        command = command.strip()
        if not command:
            continue

        command = command.split('#')[0].strip()
        if not command:
            continue

        command_parts = command.split()
        commands.extend(command_parts)

    currentMode = 0
    

    for command in commands:
        configCommand = config.get(command, "")
        currentCommand = modes[currentMode].get(configCommand, "")
        if currentCommand == "add":
            # do something
            continue
    
    fout = f"""
    section .data
        bytes db 1000 dup(0)
        pointer dd 0
        fileBytes db {fileBytes}
        filePointer dd 0

    section .text
        global _start

    _start:
        _code:
            ; code
            jmp _exit

        printByte:
            mov al, [bytes + [pointer]]
            mov eax, 4
            mov ebx, 1
            mov ecx, eax
            mov edx, 1
            int 0x80
            ret

        moveRight:
            inc [pointer]
            ret

        moveLeft:
            dec [pointer]
            ret

        incrementByte:
            inc byte [bytes + [pointer]]
            ret

        decrementByte:
            dec byte [bytes + [pointer]]
            ret

        moveFilePointerRight:
            inc [filePointer]
            ret

        moveFilePointerLeft:
            dec [filePointer]
            ret

        incrementFileByte:
            inc byte [fileBytes + [filePointer]]
            ret

        decrementFileByte:
            dec byte [fileBytes + [filePointer]]
            ret

        setPointerLocationToFilePointerLocation:
            mov al, [fileBytes + [filePointer]]
            mov [bytes + [pointer]], al
            ret

    _exit:
        mov eax, 1
        xor ebx, ebx
        int 0x80
    """


def main(argData: dict) -> None:
    try:
        data = ""
        with open(argData['inputFlag']['value'], 'r') as infile:
            i = infile.read()
        with open(argData['inputTxtFlag']['value'], 'r') as intFile:
            it = intFile.read()
        with open(argData['outputFlag']['value'], 'w') as outfile:
            outfile.write(compile(i, it))

    except Exception as e:
        print(f"Error processing files: {e}")

if __name__ == "__main__":
    argData = {
        'inputFlag': {
            'flag': '-i',
            'longFlag': '--inputFlag',
            'type': str,
            'default': 'main.iusearchbtw',
            'help': "Path to the input script file (default: 'main.iusearchbtw')."
        },
        'inputTxtFlag': {
            'flag': '-itxt',
            'longFlag': '--inputTxtFlag',
            'type': str,
            'default': 'input.txt',
            'help': "Path to the input text file (default: 'input.txt')."
        },
        'outputFlag': {
            'flag': '-o',
            'longFlag': '--outputFlag',
            'type': str,
            'required': True,
            'help': "Path to the output file. This flag is required."
        }
    }

    parser = argparse.ArgumentParser(description="Process input and output files.")

    for argName, argDetails in argData.items():
        parser.add_argument(
            argDetails['flag'], 
            argDetails['longFlag'], 
            type=argDetails['type'], 
            default=argDetails.get('default'), 
            required=argDetails.get('required', False), 
            help=argDetails['help']
        )

    args = parser.parse_args()

    for argName, argDetails in argData.items():
        argDetails['value'] = getattr(args, argName)

    main(argData)