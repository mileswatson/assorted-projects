ALPHAS = list("abcdefghijklmnopqrstuvwxyz")
DIGITS = list("0123456789")
SPLITTERS = list("{(")
JOINERS = list("})")
SEPARATORS = list(",;")
UNARYOPS = list() #list("!@~")
DUALOPS = list(":+=") #list(":+-*/<>=")
REPEATABLETYPES = ["ALPHA", "DIGIT", "DUALOP"]

ALLOWEDCHARS = ALPHAS + DIGITS + SPLITTERS + JOINERS + SEPARATORS + UNARYOPS + DUALOPS

REGISTERS = [
    "rax",
    "rbx",
    "rcx",
    "rdx",
    "rdi",
    "rsi",
    "r8",
    "r9",
    "r10",
    "r11"
]

def chartype(char):
    if char in ALPHAS:
        return "ALPHA"
    if char in DIGITS:
        return "DIGIT"
    if char in SPLITTERS:
        return "SPLITTER"
    if char in JOINERS:
        return "JOINER"
    if char in SEPARATORS:
        return "SEPARATOR"
    if char in UNARYOPS:
        return "UNARYOP"
    if char in DUALOPS:
        return "DUALOP"
    else:
        return "UNKNOWN"

GKEYWORDS = ["func", "global"]
LKEYWORDS = ["local", "return"]

class Token:
    def __init__(self, tokentype, value):
        self.tokentype = tokentype
        self.value = value
    def __str__(self):
        return self.tokentype+" "+self.value

def load(filename):
    f = open(filename)
    string = f.read()
    f.close()
    return string

def clean(dirty):
    return "".join([char if char in ALLOWEDCHARS else "" for char in dirty])

def lex(pure):
    parts = []
    currentPart = ""
    lastType = ""
    for char in pure:
        currentType = chartype(char)
        if lastType == currentType and currentType in REPEATABLETYPES:
            currentPart += char
        else:
            tokenType = lastType
            if lastType == "ALPHA":
                tokenType = "IDENTIFIER"
            elif lastType == "DIGIT":
                tokenType = "NUMBER"
            if currentPart in GKEYWORDS:
                tokenType = "GKEYWORD"
            if currentPart in LKEYWORDS:
                tokenType = "LKEYWORD"
            parts.append(Token(tokenType, currentPart))
            lastType = currentType
            currentPart = char
    tokenType = currentType
    if currentType == "ALPHA":
        tokenType = "IDENTIFIER"
    elif currentType == "DIGIT":
        tokenType = "NUMBER"
    if currentType in GKEYWORDS:
        tokenType = "GKEYWORD"
    if currentType in LKEYWORDS:
        tokenType = "LKEYWORD"
    parts.append(Token(tokenType, currentPart))
    return parts[1:]

def nest(tokens):
    # codeBlock, currentStatement
    structure = [ [[],[]] ]
    layer = 0
    for token in tokens:
        if token.value == "{":
            structure.append([[],[]])
            layer += 1
        elif token.value == "}":
            structure[layer-1][1].append(structure[layer][0])
            structure = structure[:-1]
            layer -= 1
            structure[layer][0].append(structure[layer][1])
            structure[layer][1] = []
        elif token.value == ";":
            structure[layer][0].append(structure[layer][1])
            structure[layer][1] = []
        elif token.value == "(":
            structure.append([[],[]])
            layer += 1
        elif token.value == ")":
            if len(structure[layer][1]) > 0:
                structure[layer][0].append(structure[layer][1])
                structure[layer][1] = []
            structure[layer-1][1].append(structure[layer][0])
            structure = structure[:-1]
            layer -= 1
        elif token.value == ",":
            structure[layer][0].append(structure[layer][1])
            structure[layer][1] = []
        else:
            structure[layer][1].append(token)
    return structure[0][0]


def recursiveString(array, depth=1):
    return "\t"*(depth-1)+"{"+"\n"+"\n".join([recursiveString(i, depth+1) if type(i) == list else "\t"*depth+str(i) for i in array])+"\n"+"\t"*(depth-1)+"}"

def globalParse(nested):
    dataSection = ["section .data"]
    textSection = [
        "section .text",
        "global _start",
        "_start:",
        "call main",
        "mov rbx, rax",
        "mov rax, 1",
        "int 80h"
    ]
    for statement in nested:
        if statement[0].value == "global":
            for expression in statement[2]:
                dataSection += [expression[0].value + ": dq 0"]
        else:
            scope = dict()
            numArgs = len(statement[2])
            textSection  += [statement[0].value + ":"   ]                      # declares function start
            textSection += ["push rbp", "mov rbp, rsp","sub rsp, "+str(numArgs*8)]     # sets up stack
            for i in range(numArgs):
                textSection += ["mov DWORD PTR [rbp-" + str((i+1)*8) + "], " + REGISTERS[i]]
                scope[statement[2][i][0].value] = str((i+1)*8)
            textSection += blockParse(statement[4], scope)
            textSection += ["mov rsp, rbp","pop rbp","ret"]
    return "\n".join(dataSection + [""] + textSection)

def blockParse(nested, scope):
    scope = dict(scope)
    print(recursiveString(nested))
    print("\n\n\n")
    code = []
    for expression in nested:
        #print(recursiveString(expression))
        A = expression[0]
        operator = expression[1]
        B = expression[2]
        if operator.value == ":":
            if A.value == "local":
                for identifier in B:
                    scope[identifier[0].value] = str((len(scope)+1)*8)
                code += ["sub rsp, "+str(len(B)*8)]
            elif A.value == "return":
                code += expressionParse(B, scope, False, 0)[0]
        
    return code

def expressionParse(nested, scope, addr=False, reg=0):
    code = []
    for exp in nested:
        print(recursiveString(exp))
        if len(exp) == 1:
            A = exp[0]
            if A.tokentype == "NUMBER":
                code += ["mov "+REGISTERS[reg]+", "+A.value]
            elif A.tokentype == "IDENTIFIER":
                if A.value in scope:
                    code += []
        elif len(exp) == 2:
            pass
        elif len(exp) == 3:
            A = exp[0]
            operator = exp[1]
            B = exp[2]
    return code, reg

def tokenParse(token, scope, addr=False, reg=0):
    if token.tokentype == "NUMBER":
        return ["mov "+REGISTERS[reg]+", "+token.value]
    elif token.tokentype == "IDENTIFIER":
        if token.value in scope:
            if addr==True:
                return ["mov "+REGISTERS[reg]+", "+]

dirty = load("program.poccl")
#print(dirty)

pure = clean(dirty)
#print(pure)

tokens = lex(pure)
#print(recursiveString(tokens))

nested = nest(tokens)
#print(recursiveString(nested))

instructions = globalParse(nested)
print(instructions)

#print(recursiveString(nested))
