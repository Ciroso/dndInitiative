import random
import os.path
import pickle
from termcolor import colored
import re
import operator


class Hero:
    def __init__(self, AttributeList):
        self.type = "hero"
        self.nome = AttributeList[0]
        self.ca = AttributeList[1]
        self.id = AttributeList[2]
        self.iniziativa = 0


    def printName(self, removeMode):
        if removeMode:
            print(colored("Nome:", "blue"), self.nome)
        else:
            print(
                colored("Iniziativa: ", "blue"), self.iniziativa,
                colored("Nome:", "blue"), self.nome + "\t\t" +
                                           colored("Ca:", "blue"), self.ca)


class Enemy:
    def __init__(self, Attributelist):
        self.type = "enemy"
        self.nome = Attributelist[0]
        self.ca = Attributelist[1]
        self.id = "-"
        self.hp = self.hpCalc(Attributelist[2])
        self.iniziativa = 0
        self.ricorrenza = 0
        self.alive = True

    def hpCalc(self, DV):
        try:
            if isinstance(DV, str):
                tempDV = DV.split()
                tempHP = 0
                for i in range(0, int(tempDV[0])):
                    tempHP += random.randint(0, int(tempDV[1]))
                return tempHP + int(tempDV[2])
            else:
                return DV
        except:
            print("Devi fornire 'Numero dadi' 'tipo di dado' 'mod', invece tu hai fornito " + DV)

    def printName(self, removeMode):
        if removeMode:
            print(colored("Nome:", "red"), self.nome + str(self.ricorrenza))
        else:
            if self.alive:
                colour = "red"
            else:
                colour = "grey"
            print(
                colored("Iniziativa: ", colour), self.iniziativa,
                colored("Nome:", colour), self.nome + str(self.ricorrenza) + "\t\t",
                colored("Ca:", colour), self.ca,
                colored("HP:", colour), self.hp)

    def verifyricorrenza(self, table):
        newRicorrenza = 0
        for i in range(0, len(table)):
            if self.nome == table[i].nome:
                newRicorrenza += 1
        self.ricorrenza = newRicorrenza

    def rollInitiative(self):
        self.iniziativa = random.randint(1, 20)


def start():
    session = []
    if os.path.isfile('lastBackup'):
        if input("Trovata vecchia partita, vuoi caricarla? y/n\n") in {"y", "", "Y"}:
            session = pickle.load(open("lastbackup", "rb"))
            actualTable(session, False)
            if input("Vuoi azzerare l'iniziativa? y/n\n") in {"y", "Y"}:
                for s in session:
                    s.iniziativa = 0
    managePlayer(session)
    iniziativaTime(session)

    roundManager(session)

    makeBackup(session)

    actualTable(session, False)
    print("PLAY")

def roundManager(table):
    round = 0
    print("Round: ", round)



def dealDamage(table):



def iniziativaTime(table):
    for c in table:
        if c.iniziativa == 0:
            if c.type == "enemy":
                c.rollInitiative()
            else:
                print("Iniziativa per ", c.nome, end=" ")
                c.iniziativa = int(input())
        makeBackup(table)
    table.sort(key=operator.attrgetter('iniziativa'))
    table.reverse()
    fixInitiative(table)
    for c in table:
        c.iniziativa = truncate(c.iniziativa, 1)


def fixInitiative(table):
    for i in range(0, len(table) - 1):
        if table[i].iniziativa == table[i + 1].iniziativa:
            table[i].iniziativa += 0.1
            print(table[i].iniziativa)
            fixInitiative(table)


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier




def makeBackup(table):
    pickle.dump(table, open("lastbackup", "wb"))


def readFile(L, table):
    f = open(L, "r")
    tempRead = f.read().splitlines()
    f.close()
    splittedRead = []
    for i in range(0, len(tempRead)):
        splittedRead.append(re.split('(?<!\(.),(?!.\))', tempRead[i]))
        print(str(i) + " " + str(splittedRead[i][0]))

    selectedChar = input("Quale?\n")
    if selectedChar == "0":
        selectedChar = "1 2 3 4 5 6"
    selectedChar = selectedChar.split()

    for i in selectedChar:
        if L == "party":
            table.append(Hero(splittedRead[int(i)]))
        else:
            enemyAppender(splittedRead[int(i)], table)


def throwDice(Qdv, dv, mod):
    tempdv = 0
    for i in range(0, int(Qdv)):
        tempdv += random.randint(int(dv))
    return tempdv + int(mod)


def managePlayer(table):
    wannaAdd = True
    while wannaAdd:
        req = input("A-ggiungi, R-imuovi, M-odifica, V-isualizza o E-sci?\n")
        if req in {"A", "a", "aggiungi"}:
            reqA = input("P-arty, E-nemy, O-ther player \n")
            if reqA in {"P", "p", "party"}:
                readFile("party", table)
            elif reqA in {"E", "e", "enemy"}:
                readFile("enemy", table)
            elif reqA in {"O", "o", "other"}:
                enemyAppender([input("Nome: "), input("CA: "), input("dv ( esempio 2 12 +3) con 12 = dv: ")], table)
        if req in {"R", "r", "rimuovi"}:
            actualTable(table, True)
            table.pop(int(input("Chi?\n")))
        if req in {"M", "m", "modifica"}:
            print("modifica")
        if req in {"V", "v", "visualizza", "show"}:
            actualTable(table, False)
        if req in {"E", "e", "esci", "exit", ""}:
            wannaAdd = False


def enemyAppender(lista, table):
    table.append(Enemy(lista))
    table[-1].verifyricorrenza(table)


def actualTable(table, removeMode):
    counter = 0
    for i in table:
        if removeMode:
            print(colored(counter, "yellow"), end=" ")
            counter += 1
        i.printName(removeMode)


if __name__ == "__main__":
    start()

    # print("~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~")
    # print("~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~")
