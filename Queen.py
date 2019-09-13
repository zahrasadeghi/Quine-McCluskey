class QueenMcKlusky:
    def __init__(self, numberOfVariables):
        self.table = {}
        self.alternativeTable = {}
        self.answer = set([])
        self.numberOfVariables = numberOfVariables
        self.minterms = []
        self.finalMinterms = []

    def setMinterms(self, minterms):
        for i in range(0, len(minterms)):
            self.setMinterm(minterms[i])

    def setMinterm(self, number):
        number = str(bin(number))[2:]
        number = (self.numberOfVariables - len(number)) * "0" + number
        self.answer.add(number)
        self.minterms +=[number]
        numberOfOnes = number.count("1")
        if numberOfOnes in self.table.keys():
            self.table[numberOfOnes] += [number]
        else:
            self.table[numberOfOnes] = [number]

    def calculate(self):
        while self.table != {}:
            for i in self.table.keys():
                if i + 1 not in self.table.keys():
                    continue
                self.checkAdjacentTables(i)
            self.table = self.alternativeTable
            self.alternativeTable = {}
        self.makeFinalTable()
        self.findFinalAnswer()
        print self.finalMinterms

    def checkAdjacentTables(self, i):
        for firstNumber in self.table[i]:
            for secondNumber in self.table[i+1]:
                if self.checkIfHamingDistanceIsOne(firstNumber, secondNumber):
                    self.removeAndReplace(firstNumber, secondNumber,i)

    def checkIfHamingDistanceIsOne(self, firstNumber, secondNumber):
        c = 0
        for i in range(len(firstNumber)):
            if firstNumber[i] != secondNumber[i]:
                c += 1
        if c == 1:
            return True
        return False

    def removeAndReplace(self, firstNumber, secondNumber, index):
        finalNumber = ""
        for i in range(len(firstNumber)):
            if firstNumber[i] != secondNumber[i]:
                finalNumber += "-"
            else:
                finalNumber += firstNumber[i]
        self.answer.add(finalNumber)
        if index in self.alternativeTable.keys():
            self.alternativeTable[index] += [finalNumber]
        else:
            self.alternativeTable[index] = [finalNumber]
        if firstNumber in self.answer:
            self.answer.remove(firstNumber)
        if secondNumber in self.answer:
            self.answer.remove(secondNumber)

    def makeFinalTable(self):
        self.finalTable = {}
        for finalMinTerm in self.answer:
            for minterm in self.minterms:
                if self.checkIsThisMintermInIt(finalMinTerm, minterm):
                    if finalMinTerm in self.finalTable.keys():
                        self.finalTable[finalMinTerm] += [minterm]
                    else:
                        self.finalTable[finalMinTerm] = [minterm]
            self.finalTable[finalMinTerm] = set(self.finalTable[finalMinTerm])

    def checkIsThisMintermInIt(self,finalMinTerm, minterm):
        for i in range(len(finalMinTerm)):
            if finalMinTerm[i] == minterm[i] or finalMinTerm[i] == '-':
                continue
            else:
                return False
        return True

    def findFinalAnswer(self):
        arrOfKeys = sorted(self.finalTable, key=lambda k: len(self.finalTable[k]), reverse=True)
        for key in arrOfKeys:
            if len(self.finalTable[key]) != 0:
                self.finalMinterms += [key]
                self.removeFromOtherSets(self.finalTable[key])
                self.finalTable[key] = set([])
        self.convertBinaryToChar()

    def removeFromOtherSets(self, arr):
        for key in self.finalTable.keys():
            if self.finalTable[key] != arr:
                self.finalTable[key] -= arr

    def convertBinaryToChar(self):
        print self.finalMinterms
        for index in range(len(self.finalMinterms)):
            string = ""
            for i in range(len(self.finalMinterms[index])):
                if self.finalMinterms[index][i] == '1':
                    string += chr(ord('a')+i)
                elif self.finalMinterms[index][i] == '0':
                    string += (chr(ord('a') + i)+"'")
            self.finalMinterms[index] = string


m = QueenMcKlusky(input("enter number of variables:"))
m.setMinterms(input("enter the minterms:"))
m.calculate()