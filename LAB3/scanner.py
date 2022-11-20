from hashtable import HashTable

import re

class Scanner:

    def __init__(self):
        self.operators = ["+", "-", "==", "/", "//", "<=", ">=", "!=", "!", "=", "*"]
        self.separators = [" ", ";", "(", ")", "\n", "[", "]", ",", "\t",".",""]
        self.constant = r'^(0|[+-]?[1-9][0-9]*)$'
        self.identifier = r'^[a-zA-Z]([a-zA-Z]|[0-9])*$'
        self.items = []


    def separate(self, line, lineNumber):

        index = 0
        current = ""
        while index < len(line):

            c = line[index]

            if self.isOperator(c):
                self.items.append((current,lineNumber))
                current, index = self.checkOp(line, index)
                self.items.append((current,lineNumber))
                current = ""
            else:
                if self.isSeparator(c) :
                    self.items.append((current,lineNumber))
                    current = ""
                else:
                    current += c
            index += 1




    def checkOp(self, line, index):

        current = ""

        while line[index] != "\n" and self.isOperator(line[index]):
            current += line[index]
            index += 1

        return current, index-1

    def isOperator(self, c):
        for op in self.operators:
            if c in op:
                return True
        return False

    def isSeparator(self, c):
        for sep in self.separators:
            if c in sep:
                return True
        return False


def run():

    with open("p3.txt", "r") as p:

        tokenFile = open("token.in","r")
        tokenFile = tokenFile.read()
        tokenFile = tokenFile.split("\n")
        p = p.read()
        lines = p.split("\n")

        scanner = Scanner()
        ST = HashTable()
        PIF = []

        lineNumber = 0
        for l in lines:
            lineNumber += 1
            scanner.separate(l, lineNumber)

        for p in scanner.items:
            if p[0] == "":
                scanner.items.remove(p)

        index = 0

        error = False

        for p in scanner.items:

            aux = p[0]
            if aux in scanner.separators or aux in scanner.operators or aux in tokenFile:
                PIF.append((aux, 0))
            else:
                if re.search(scanner.constant, aux) !=  None or re.search(scanner.identifier, aux) != None: 
                    if ST.get(aux) == -1:
                        index += 1
                        ST.insert(aux, index)
                    insertIndex = ST.get(aux)
                    PIF.append(("id", insertIndex))
                else:
                    error = True
                    print(f"Lexical error at {p[0]} line {p[1]}")

        pifOut = open("PIF.out","w")
        stOUT = open("ST.out","w")

        if error == False:
            print("Lexically correct")

        stOUT.write("Symbol table using hash table \n")
        stOUT.write(str(ST))
        for p in PIF:
            pifOut.write(str(p)+"\n")


run()
