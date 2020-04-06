import random
import os.path
import pickle
from termcolor import colored
import re


class Hero:
    def __init__(self, AttributeList):
        self.type = "hero"
        self.nome = AttributeList[0]
        self.ca = AttributeList[1]
        self.id = AttributeList[2]
        self.iniziativa = 0

    def showMe(self):
        print(colored("Nome: ", "blue"), self.nome + " " + self.id, colored("\nCa: ", "blue"), self.ca,
              colored("\nIniziativa: ", "blue"), self.iniziativa, "\n")


class Enemy:
    def __init__(self, Attributelist):
        self.type = "enemy"
        self.nome = Attributelist[0]
        self.ca = Attributelist[1]
        self.id = "-"
        self.hp = self.hpCalc(Attributelist[2])
        self.iniziativa = 0
        self.ricorrenza = 0

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

    def showMe(self):
        print(colored("Nome: ", "red"), self.nome + str(self.ricorrenza) + " " + self.id, colored("\nCa: ", "red"),
              self.ca, colored("\nHP: ", "red"),
              self.hp, colored("\nIniziativa: ", "red"), self.iniziativa, "\n")

    def verifyricorrenza(self, table):
        newRicorrenza = 0
        for i in range(0, len(table)):
            if self.nome == table[i].nome:
                newRicorrenza += 1
        self.ricorrenza = newRicorrenza


def start():
    session = []
    if os.path.isfile('lastBackup'):
        if input("Trovata vecchia partita, vuoi caricarla? y/n\n") in {"y", ""}:
            session = pickle.load(open("lastbackup", "rb"))
            actualTable(session, False)
    managePlayer(session)
    roundManager(session)
    makeBackup(session)

    print("PLAY")
    # os.remove("lastbackup")


def roundManager(table):
    print("round", table)


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

    selectedChar = input("Quale?\n").split()
    for i in selectedChar:
        if L == "party":
            table.append(Hero(splittedRead[int(i)]))
        else:
            table.append(Enemy(splittedRead[int(i)]))
            table[-1].verifyricorrenza(table)


def throwDice(Qdv, dv, mod):
    tempdv = 0
    for i in range(0, int(Qdv)):
        tempdv += random.randint(int(dv))
    return tempdv + int(mod)


def managePlayer(table):
    wannaAdd = True
    while wannaAdd:
        req = input("A-ggiungi, R-imuovi, M-odifica, V-isualizza o E-sci?\n")
        if req in {"A", "a", "aggiungi", ""}:
            reqA = input("P-arty, E-nemy, O-ther player \n")
            if reqA in {"P", "p", "party"}:
                readFile("party", table)
            elif reqA in {"E", "e", "enemy"}:
                readFile("enemy", table)
            elif reqA in {"O", "o", "other"}:
                table.append(Enemy)
        if req in {"R", "r", "rimuovi"}:
            actualTable(table, True)
            table.pop(int(input("Chi?\n")))
        if req in {"M", "m", "modifica"}:
            print("modifica")
        if req in {"V", "v", "visualizza", "show"}:
            actualTable(table, False)
        if req in {"E", "e", "esci", "exit", ""}:
            wannaAdd = False


def actualTable(table, removeMode):
    for i in table:
        if removeMode:
            print(i)
        i.showMe()


if __name__ == "__main__":
    start()

    # print("~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~")
    # print("~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~")
