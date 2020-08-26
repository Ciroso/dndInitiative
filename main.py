import random
import os.path
import pickle
from termcolor import colored
import re
import operator


class Session:
    initR = 0
    combatMode = False

    def __init__(self, characterList=None, round=initR, mode=combatMode):
        if characterList is None:
            session = []
        self.characterList = characterList
        self.round = round
        self.combatMode = mode

    def save(self):
        pickle.dump(self, open("lastbackup", "wb"))

    def load(self):
        return pickle.load(open("lastbackup", "rb"))


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
                colored("Nome:", "blue"), self.nome + "\t\t" + colored("Ca:", "blue"),
                self.ca, colored("Iniziativa: ", "blue"), self.iniziativa)


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

        if self.alive:
            colour = "red"
            if removeMode:
                print(colored("Nome:", colour), self.nome + str(self.ricorrenza))
            else:
                print(
                    colored("Nome:", colour), self.nome + str(self.ricorrenza) + "\t\t",
                    colored("Ca:", colour), self.ca,
                    colored("HP:", colour), self.hp,
                    colored("Iniziativa: ", colour), self.iniziativa)
        else:
            colour = "grey"
            if removeMode:
                print(colored(strike("Nome:"), colour), strike(self.nome + str(self.ricorrenza)))
            else:
                print(
                    colored(strike("Nome:"), colour), strike(self.nome + str(self.ricorrenza)) + "\t\t",
                    colored(strike("Ca:"), colour), strike(self.ca),
                    colored(strike("HP:"), colour), strike(str(self.hp)),
                    colored(strike("Iniziativa: "), colour), strike(str(self.iniziativa))
                )

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
        if input("Trovata vecchia partita, vuoi caricarla? Y/n\n") in {"y", "", "Y"}:
            session = pickle.load(open("lastbackup", "rb"))
            actualTable(session, False)
            if input("Vuoi azzerare l'iniziativa? y/N\n") in {"y", "Y", "Yes", "yes"}:
                for s in session:
                    s.iniziativa = 0
    managePlayer(session)
    iniziativaTime(session)
    roundManager(session)

def roundManager(table):
    round = 0
    print("------------Pronti? Si parte!------------")
    playtime = True
    while playtime:
        round += 1
        print("Round: ", round)
        actualTable(table, False)
        for turnMan in table:
            print("\nE' il turno di ", end=" ")
            turnMan.printName(False)
            action(table, turnMan)
            makeBackup(table)
        enemyLeft = False
        for turnMan in table:
            if not enemyLeft:
                if (turnMan.type == "enemy") and (turnMan.alive == True):
                    enemyLeft = True
        if not enemyLeft:
            if input("Vuoi ancora mantenere la sessione attiva? Non ci sono più nemici y/N\n ") in {"No", "no", "n",
                                                                                                    "N", ""}:
                playtime = False


def action(table, character):
    if (character.type == "enemy") and (character.alive == False):
        return
    inputAction = input("Cosa succede? D-anni, C-ure, [N]-iente? \n")
    if inputAction in {"Danni", "danni", "D", "d"}:
        changeLife(table, "Damage")
    elif inputAction in {"Cura", "cura", "C", "c"}:
        changeLife(table, "Heal")


def changeLife(table, command):
    try:
        runningAction = True
        while runningAction:
            print("\n \n")
            actualTable(table, True)
            targetNumber = int(input("A chi? "))
            if command == "Damage":
                table[targetNumber].hp -= int(input("\nDi quanto? "))
                if table[targetNumber].hp <= 0:
                    table[targetNumber].alive = False
                    print("!!DIED!!")
            elif command == "Heal":
                table[int(input("Chi? "))].hp += int(input("\nDi quanto? "))
            if input("E basta? y/N \n") in {"Si", "si", "s", "Yes", "yes", "y"}:
                runningAction = False
    except:
        print("Hai sbagliato a selezionare a chi fare danni! Per sta volta chiudo un occhio...i nostri eroi "
              "non prendono danni! (almeno non qui)")


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
        req = input("A-ggiungi, R-imuovi, M-odifica, V-isualizza o [E]-sci dalla modalità modifica?\n")
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


def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])


if __name__ == "__main__":
    start()

    # print("~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~")
    # print("~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~")
