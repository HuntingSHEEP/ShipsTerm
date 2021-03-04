# zmienianie kodowania w terminalu linux:
# $ locale
# $ locale -a
# $ sudo localectl set-locale LANG=en_US.UTF-8
# $ export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
import time
poczatek = time.time()

from sty import fg
from os import system
from time import sleep
from random import randint
import pickle
import numpy as np
from copy import deepcopy

modul = lambda a: a if a >= 0 else -a


### FUNKCJE DO AKTUALIZACJI MAPY - USUWANIA ZBĘDNYCH PÓL ###

def sito(do_przesiania, wzorzec):
    for i, e in enumerate(wzorzec):
        if e not in do_przesiania:
            wzorzec[i] = None
    return wzorzec

def wyznacz_ciagi(l):
    w = []
    q = 0
    poprzedni = None
    for i, e in enumerate(l):
        if e == 'Non':
            if poprzedni != None:
                w += [(i-q, (q, i-1))]
            poprzedni = None
        elif e != 'Non':
            if poprzedni == None:
                q = i
            poprzedni = e
    if poprzedni != None:
        w += [(10-q, (q, 9))]
    return w

def propozycje(B, rozmiar, FAZA2 = False):
    propozycjeA = []
    for i, e in enumerate(B):
        temp = []
        for d, k in enumerate(wyznacz_ciagi(e)):
            if FAZA2:
                if k[0] >= rozmiar:
                    temp += [k]
            else:
                if k[0] < rozmiar:
                    temp += [k]
        propozycjeA.append(temp)
    return propozycjeA

def wyznacz_koordynaty(L, transpozycja=False):
    wyznaczone = []
    for i, e in enumerate(L):
        if len(e) != 0:
            for a, b in enumerate(e):
                for x in range(b[1][0], b[1][1]+1):
                    if transpozycja:
                        wyznaczone.append((x, i))
                    else:
                        wyznaczone.append((i, x))
    return wyznaczone

def dane_aktualizacji(M, poszukiwane_statki):
    M = np.array(M)
    b = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    b = np.array(b)
    M = sito(M, b)
    M = M.reshape((10, 10))

    t = None
    for i, r in enumerate(poszukiwane_statki):
        x = wyznacz_koordynaty(propozycje(M, r))
        y = wyznacz_koordynaty(propozycje(M.transpose(), r), True)
        q = set(x).intersection(y)
        if i == 0:
            t = q
        else:
            t = t.intersection(q)
    t = list(t)

    for i, e in enumerate(t):
        t[i] = chr(e[0]+97) + str(e[1]+1)

    return t

#### FUNKCJE DO FAZY1 PRZESZUKIWANIA MAPY####

def okolica(k):
    k = k[1] + 96, k[0]
    dokola = []
    for x in range(3):
        for y in range(3):
            dokola.append(chr(k[0]+x)+str(k[1]+y))
    dokola.pop(6)
    dokola.pop(2)
    return dokola

def dane_FAZAI(s):
    t = []
    for i, s in enumerate(s):
        t += okolica(s)
    t = list(set(t))
    return t

def koordynaty_wycietych(a):
    b = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    b = np.array(b)
    a = sito(a, b)
    a = a.reshape((10, 10))
    c = np.where(a.transpose()=='Non')
    ret = list(np.array(c).transpose())
    for i, e in enumerate(ret):
        ret[i] = list(e)
    return ret

def FAZA1(wzorzec):
    a = deepcopy(wzorzec)
    dane_doFAZY1 = set(dane_FAZAI(koordynaty_wycietych(a)))
    a = set(a)
    dozwolone = a - dane_doFAZY1
    g = deepcopy(dozwolone)
    dozwolone = list(dozwolone)

    dozwolone = np.array(dozwolone)
    b = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    b = np.array(b)
    dozwolone = sito(dozwolone, b)
    dozwolone = dozwolone.reshape((10, 10))
    #input(dozwolone.transpose())
    return list(g)

def wybor_zFAZA1(dane):
    return dane[randint(0, len(dane)-1)]

def FAZA2(wzorzec, szukane_statki):
    a = deepcopy(wzorzec)
    szukane_statki = [len(e) for e in szukane_statki] #odkomentować po przeflancowaniu do klasy
    a = np.array(a)
    b = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    b = np.array(b)
    a = sito(a, b)
    a = a.reshape((10, 10))
    a = a.transpose()

    d = propozycje(a, max(szukane_statki), True)
    h = propozycje(a.transpose(), max(szukane_statki), True)

    x = wyznacz_koordynaty(d, True)
    y = wyznacz_koordynaty(h)

    przeciecia = list(set(x).intersection(y)) #tutaj coś jest nie tak, nie wyznacza poprawnie przecięć chyba

    if len(przeciecia) != 0:
        #input('p  '+ str(przeciecia))
        losowy = przeciecia[randint(0, len(przeciecia)-1)]
        losowy = chr(losowy[0]+97)+str(losowy[1]+1)
        return losowy
    else:
        ds = [chr((e[0][1][1] - e[0][1][0] + 1) // 2 + e[0][1][0] + 96) + str(i + 1) for i, e in enumerate(d) if len(e) != 0]
        hs = [chr(i + 97) + str((e[0][1][1] - e[0][1][0] + 1) // 2 + e[0][1][0] + 1) for i, e in enumerate(h) if len(e) != 0]
        v = ds + hs
        input('srodki   '+ str(v))
        return v[randint(0, len(v)-1)]


############################################################

def CC(napis, kolor):
    """ red, green, yellow, blue, magenta, cyan, white"""
    red     = fg(200,0,0)
    green   = fg(0, 85, 150)
    yellow  = fg(235, 205, 50)
    blue    = fg(0, 60, 140)
    magenta = fg(250,0 , 100)
    cyan    = fg(00, 180, 255)
    white   = fg(250, 250, 250)
    zielony1= fg(0, 200, 30)
    zolty   = fg(255, 250, 0)
    czerwony = fg(255, 0 , 0)
    pomaranczowy = fg(250, 40, 0)
    niebieski = fg(0, 10, 255)
    pomaranczowy2 = fg(250, 160, 10)
    zielony2  = fg(5, 215, 255)
    return eval(kolor) + napis + fg.rs


class USTAWIENIA():
    def __init__(self, rozmiary_statkow = [5,4,4,3,3,2], podglad_statkow = True):
        self.rozmiary_statkow = rozmiary_statkow
        self.podglad_statkow = podglad_statkow
    def reset(self):
        domyslne_rozmiary_statkow = [5,4,4,3,3,2]
        domyslne_podglad_statkow = True

        self.rozmiary_statkow = domyslne_rozmiary_statkow
        self.podglad_statkow = domyslne_podglad_statkow



class Nieprawidlowe_dane(Exception):
    def __str__(self):
        return "Nieprawidłowe współrzędne!"

'\x1b[2;37m'+ chr(11034) +'\x1b[0m'
class Pole():
    def __init__(self):
        self.pole_puste = '\x1b[0;37m'+ chr(11034) +'\x1b[0m'
        self.pole_statek = (None, CC(chr(9638), 'czerwony'), CC(chr(9638), 'zolty'), CC(chr(9638), 'magenta'), CC(chr(9638), 'cyan'), CC(chr(9638), 'zielony1'),
     CC(chr(9638), 'niebieski'), CC(chr(9638), 'pomaranczowy2'), CC(chr(9638), 'zielony2'))
        self.pole_traf = CC(chr(8857), 'red')
        self.pole_traf_z = '\x1b[2;30m'+ chr(8864) +'\x1b[0m'
        self.pole_nie_traf = '\x1b[2;30m'+ chr(9678) +'\x1b[0m'


class Mapa(Pole):
    def __init__(self):
        super().__init__()
        self.plansza_MOJE = [[self.pole_puste for k in range(10)] for a in range(10)]
        self.plansza_PRZECIWNIKA = [[self.pole_puste for k in range(10)] for a in range(10)]

    def wyrysuj(self):
        print("\n\n" + ' ' * 20 + CC("[ ", "yellow") + CC("TWOJE POLE", 'cyan') + CC(" ]", "yellow") + ' ' * 45 + CC("[ ", "yellow")+ CC("POLE PRZECIWNIKA", 'cyan') + CC(" ]", "yellow")+' ' * 15 + '\n')
        print(CC('         A   B   C   D   E   F   G   H   I   J', "green") + '  ' * 12 + CC(' A   B   C   D   E   F   G   H   I   J', "green"),
              end='\n\n\n')

        for i in range(10):
            if i != 9:
                print(CC('  |', "green") + CC(str(i + 1), "cyan"), end=CC('|    ', "green"))
            else:
                print(CC('  |', "green") + CC(str(i + 1), "cyan"), end=CC('|   ', "green"))
            for M in self.plansza_MOJE[i]:
                print(M, end='   ')
            print(CC('      ~     ', "cyan"), end=' ')

            if i != 9:
                print(CC('  |', "green") + CC(str(i + 1), "cyan"), end=CC('|    ', "green"))
            else:
                print(CC('  |', "green") + CC(str(i + 1), "cyan"), end=CC('|   ', "green"))

            for P in self.plansza_PRZECIWNIKA[i]:
                print(P, end='   ')
            print('\n')

    def koordynaty(self, napis):
        a, *b = napis
        b = "".join(b)
        X = ord(a) - 96
        Y = int(b)
        return (X, Y)


class Gracz(Mapa):
    def __init__(self, nick):
        super().__init__()
        self.moje_okrety = []
        self.moje_okrety2 = []
        self.moje_okrety_trafione = []
        self.nick = nick
        self.usuniete2 = []

    def ustaw_statek(self, poczatek, koniec):
        x1, y1 = self.koordynaty(poczatek)
        x2, y2 = self.koordynaty(koniec)

        if not (x1 == x2 or y1 == y2):
            raise Nieprawidlowe_dane

        dx, dy = modul(x2 - x1), modul(y2 - y1)
        rozmiar = max(dx, dy)
        statek = []

        if max(dx, dy) > 0:
            for u in range(max(dx, dy) + 1):
                o = int(min(x1, x2) + (dx / max(dx, dy)) * u)
                p = int(min(y1, y2) + (dy / max(dx, dy)) * u)

                self.plansza_MOJE[p - 1][o - 1] = self.pole_statek[rozmiar]
                statek.append((o, p))
        self.moje_okrety.append(statek)
        self.moje_okrety2.append(statek)
        for s in statek:
            self.usuniete2.append(chr(s[0]+96) + str(s[1]))
        return rozmiar + 1

    def __czy_zatopione(self, przeciwnik):
        for s in range(len(przeciwnik.moje_okrety)):
            z = True
            for e in przeciwnik.moje_okrety[s]:
                if e not in przeciwnik.moje_okrety_trafione:
                    z = False
                    break
            if z:
                return przeciwnik.moje_okrety[s]
        return False

    def strzel(self, KOMU, GDZIE):
        X, Y = self.koordynaty(GDZIE)
        pole = KOMU.plansza_MOJE[Y - 1][X - 1]
        rodzaj = self.pole_statek

        if pole in rodzaj:
            KOMU.plansza_MOJE[Y - 1][X - 1] = self.pole_traf
            self.plansza_PRZECIWNIKA[Y - 1][X - 1] = self.pole_traf
            KOMU.moje_okrety_trafione.append((X, Y))
            czyzatopione = self.__czy_zatopione(KOMU)

            if type(czyzatopione) == list:
                KOMU.moje_okrety.remove(czyzatopione)
                for a in czyzatopione:
                    KOMU.plansza_MOJE[a[1] - 1][a[0] - 1] = self.pole_traf_z
                    self.plansza_PRZECIWNIKA[a[1] - 1][a[0] - 1] = self.pole_traf_z
                return True
            return True

        elif KOMU.plansza_MOJE[Y - 1][X - 1] == self.pole_puste:
            KOMU.plansza_MOJE[Y - 1][X - 1] = self.pole_nie_traf
            self.plansza_PRZECIWNIKA[Y - 1][X - 1] = self.pole_nie_traf
            return False

        else:
            return "Tu nie wolno strzelić!"


    def decyzja_ustawienie(self, wielkosc_statku):

        self.statek1 = []
        self.statek2 = []
        flaga1, flaga2 = False, False

        while not (flaga1 or flaga2):
            self.statek1 = []
            self.statek2 = []
            punkt_startowy = (randint(1, 10), randint(1, 10))
            flaga1 = True
            for a in range(wielkosc_statku):
                nowy_y = punkt_startowy[1] + a
                nowy_p1 = chr(punkt_startowy[0] + 96) + str(nowy_y)

                if (1 <= nowy_y <= 10) and (nowy_p1 not in self.usuniete2):
                    self.statek1.append(nowy_p1)
                else:
                    flaga1 = False
                    self.statek1 = []
                    break

            flaga2 = True
            for w in range(wielkosc_statku):
                # self.statek2.append(chr(punkt_startowy[0]+96+w)+str(punkt_startowy[1]))
                nowy_x = punkt_startowy[0] + 96 + w
                nowy_p2 = chr(nowy_x) + str(punkt_startowy[1])

                if (97 <= nowy_x <= 106) and (nowy_p2 not in self.usuniete2):
                    self.statek2.append(nowy_p2)
                else:
                    flaga2 = False
                    self.statek2 = []
                    break

        wybor = randint(0, 1)

        if wybor == 0:
            if flaga1 == True:
                for qw in self.statek1:
                    self.usuniete2.append(qw)
                return self.statek1[0], self.statek1[wielkosc_statku - 1]

            elif flaga2 == True:
                for qww in self.statek2:
                    self.usuniete2.append(qww)
                return self.statek2[0], self.statek2[wielkosc_statku - 1]

        elif wybor == 1:
            if flaga2 == True:
                for qww in self.statek2:
                    self.usuniete2.append(qww)
                return self.statek2[0], self.statek2[wielkosc_statku - 1]

            elif flaga1 == True:
                for qw in self.statek1:
                    self.usuniete2.append(qw)
                return self.statek1[0], self.statek1[wielkosc_statku - 1]


class Robot(Gracz):
    def __init__(self, nick):
        super().__init__(nick)
        self.wzor1 = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
        self.wzor2 = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
        self.trafienia = []
        self.do_ostrzelania = []
        self.usuniete = []
        self.FAZA1 = True
        self.FAZA2 = False

    def petla_testowa(self, co):
        flaga = True
        for e in co:
            if not (e in self.wzor1):
                flaga = False
                break
        return flaga

    def decyzja_ustawienie(self, wielkosc_statku):
        self.statek1 = []
        self.statek2 = []
        flaga1, flaga2 = False, False

        while not (flaga1 or flaga2):
            self.statek1 = []
            self.statek2 = []
            punkt_startowy = (randint(1, 10), randint(1, 10))
            flaga1 = True
            for a in range(wielkosc_statku):
                nowy_y = punkt_startowy[1] + a
                nowy_p1 = chr(punkt_startowy[0] + 96) + str(nowy_y)

                if (1 <= nowy_y <= 10) and (nowy_p1 not in self.usuniete):
                    self.statek1.append(nowy_p1)
                else:
                    flaga1 = False
                    self.statek1 = []
                    break

            flaga2 = True
            for w in range(wielkosc_statku):
                # self.statek2.append(chr(punkt_startowy[0]+96+w)+str(punkt_startowy[1]))
                nowy_x = punkt_startowy[0] + 96 + w
                nowy_p2 = chr(nowy_x) + str(punkt_startowy[1])

                if (97 <= nowy_x <= 106) and (nowy_p2 not in self.usuniete):
                    self.statek2.append(nowy_p2)
                else:
                    flaga2 = False
                    self.statek2 = []
                    break

        wybor = randint(0, 1)

        if wybor == 0:
            if flaga1 == True:
                for qw in self.statek1:
                    self.usuniete.append(qw)
                return self.statek1[0], self.statek1[wielkosc_statku - 1]

            elif flaga2 == True:
                for qww in self.statek2:
                    self.usuniete.append(qww)
                return self.statek2[0], self.statek2[wielkosc_statku - 1]

        elif wybor == 1:
            if flaga2 == True:
                for qww in self.statek2:
                    self.usuniete.append(qww)
                return self.statek2[0], self.statek2[wielkosc_statku - 1]

            elif flaga1 == True:
                for qw in self.statek1:
                    self.usuniete.append(qw)
                return self.statek1[0], self.statek1[wielkosc_statku - 1]

    def decyzja_strzalExpert2(self, PRZECIWNIK, EXPERT2 = False):
        if len(self.do_ostrzelania) == 0:
            if len(self.trafienia) == 0:
                self.aktualizacja_EXPERT2([len(e) for i, e in enumerate(PRZECIWNIK.moje_okrety)])

                if EXPERT2:
                    if self.FAZA1:
                        ilosc_dostepnych_pol = len(FAZA1(self.wzor2))
                        wybrane_pole = wybor_zFAZA1(FAZA1(self.wzor2))
                        if ilosc_dostepnych_pol < 10:
                            self.FAZA1 = False
                            self.FAZA2 = True
                        self.wzor2.remove(wybrane_pole)
                        return wybrane_pole

                    if self.FAZA2:
                        wybor = FAZA2(self.wzor2, PRZECIWNIK.moje_okrety)
                        self.wzor2.remove(wybor)
                        return wybor
                else:
                    punkt = (chr(randint(1, 10) + 96) + str(randint(1, 10)))
                    while not (punkt in self.wzor2):
                        punkt = (chr(randint(1, 10) + 96) + str(randint(1, 10)))
                    self.wzor2.remove(punkt)
                    return punkt
            else:
                punkt = self.trafienia[0]
                pp = (ord(punkt[0]) - 96, int(punkt[1:]))
                staaatek = []
                print('pp :', pp)

                for stateczek in PRZECIWNIK.moje_okrety:
                    if pp in stateczek:
                        staaatek = stateczek
                        break

                p1 = chr(ord(punkt[0]) + 1) + punkt[1:]
                p2 = chr(ord(punkt[0]) - 1) + punkt[1:]
                p3 = punkt[0] + str(int(punkt[1:]) + 1)
                p4 = punkt[0] + str(int(punkt[1:]) - 1)
                propozycje = [p1, p2, p3, p4]

                for hipotetyczny in propozycje:
                    if hipotetyczny not in self.wzor2:
                        propozycje.remove(hipotetyczny)

                gotowy_statek = []
                for p in staaatek:
                    ppa = chr(p[0] + 96) + str(p[1])
                    if ppa in self.wzor2:
                        gotowy_statek.append(ppa)

                dokladam = [] # to je nowe
                if len(propozycje) > 0:
                    ilosc_dolozonych = randint(0, len(propozycje))
                    for r in range(ilosc_dolozonych):
                        dokladam.append(propozycje.pop(randint(0, len(propozycje) - 1)))
                        #gotowy_statek.append(propozycje.pop(randint(0, len(propozycje) - 1)))

                #gotowy_statek = dokladam + gotowy_statek # to tyż
                #gotowy_statek = list(set(gotowy_statek))
                for d in dokladam:
                    if d in gotowy_statek:
                        dokladam.remove(d)

                #input(str(dokladam) + "   " + str(gotowy_statek) + "\n" + str(self.do_ostrzelania))
                gotowy_statek = dokladam + gotowy_statek

                przejsciowy = []
                for g in gotowy_statek:
                    if g in self.wzor2:
                        przejsciowy.append(g)

                gotowy_statek = przejsciowy
                pkt = gotowy_statek.pop(0)


                self.wzor2.remove(pkt)
                self.do_ostrzelania = gotowy_statek
                return pkt
        else:
            input(self.do_ostrzelania)
            xddd = self.do_ostrzelania[0]
            self.do_ostrzelania.remove(xddd)
            self.wzor2.remove(xddd)
        return xddd

    def aktualizacja_EXPERT2(self, posz_statki):
        zlikwidowac = dane_aktualizacji(self.wzor2, posz_statki)
        #input(self.wzor2)
        k = set(self.wzor2)
        l = set(zlikwidowac)
        w = list(k - l)
        self.wzor2 = w

    def aktualizacja_trafionych(self, PRZECIWNIK):
        if len(self.trafienia) != 0:
            do_usuniecia = []
            for wrogi in PRZECIWNIK.moje_okrety2:
                flaga = True
                for w in wrogi:
                    if chr(w[0] + 96) + str(w[1]) not in self.trafienia:
                        flaga = False
                        break
                if flaga:
                    do_usuniecia = wrogi
                    break
            if flaga:
                for d in do_usuniecia:
                    self.trafienia.remove(chr(d[0]+96) + str(d[1]))
        else:
            pass

#######################
# DEKLARACJE OBIEKTÓW #

global USTAWIENIE

try:
    with open('ships.conf', 'rb') as config_file:
        USTAWIENIE = pickle.load(config_file)
except Exception:                                           #czyli cokolwiek się wykrzaczy, zostaną przywrócone ustawienia domyślne
    pickle.dump(USTAWIENIA(), open('ships.conf', 'wb'))
    USTAWIENIE = pickle.load(open('ships.conf', 'rb'))
else:
    pass

###############################################################
 ############### #   DZIAŁ PROCEDURALNY   # ##################
###############################################################
def qsort(A):
    if len(A) <= 1:
        return A
    else:
        return qsort([a for a in A[1:] if a <= A[0]]) + [A[0]] + qsort([a for a in A[1:] if a > A[0]])

def intro():
    system("clear")
    print('{}{}{}'.format('\n' * 10, '    ' * 9, CC('STATKI', 'cyan')))

    system('clear')


def menu_glowne():
    koniec = time.time()

    system('clear')
    print("czas_od_startu:  ", koniec-poczatek)
    st = '\n' * 4 + '    ' * 8 + '    ' + CC('STATKI', 'cyan') + '\n' + '   ' * 10 + ' ' + CC('   ~~~~~~~~~~', 'white')
    ot = '    ' * 7
    a1 = CC('GRA DWUOSOBOWA    ', 'cyan') + CC('[a]\n\n', 'yellow')
    a2 = CC('BITWA SI          ', 'cyan') + CC('[k]\n\n', 'yellow')
    a5 = CC('STEROWANIE        ', 'cyan') + CC('[s]\n\n', 'yellow') + ot
    a6 = CC('USTAWIENIA        ', 'cyan') + CC('[u]\n\n', 'yellow') + ot
    a3 = CC('WYJŚCIE Z GRY     ', 'cyan') + CC('[p]\n\n', 'yellow')
    a4 = (CC(10 * " " + "/: ", 'yellow'))
    tryb = input('{}{}{}{}{}{}{}{}{}{}{}'.format(st, '\n' * 6, ot, a1, ot, a2, ot, a6, a5, a3, a4))
    system("clear")
    while tryb not in ['a', 'k', 'p', 's', 'u']:
        system('clear')
        tryb = input('{}{}{}{}{}{}{}{}{}{}{}'.format(st, '\n' * 6, ot, a1, ot, a2, ot, a6, a5, a3, a4))
        system('clear')
    return tryb


def petla_poczatkowa(gracz, statek):
    """ dostring """
    system('clear')

    wzorzec = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    flaga2 = False
    while len(statek) > 0:
        punkty = []
        fl2 = False

        while not fl2:
            ws_pp = ['']
            flaga = True
            while not ((len(ws_pp) == 2) and flaga):
                system('clear')
                print('Ustaw swoje okręty, {}!'.format(CC(gracz.nick, 'cyan')))
                gracz.wyrysuj()
                print(" Dostępne rodzaje statków: {}".format(" ,".join([CC(' ▦', 'green') * i for i in statek])))
                ws_pp = (input(CC("\nWprowadź współrzędne statku (oddzielone spacją)", 'cyan')+ CC(' /: ', 'yellow')) ).split(" ")
                system('clear')
                if "".join(ws_pp) in ('SETSHIPS', 'setships'):
                    system('clear')
                    # dodac w petli nowe statki
                    for rozmiar in statek:
                        k = gracz.decyzja_ustawienie(rozmiar)
                        gracz.ustaw_statek(k[0],k[1])
                        #statek.remove(rozmiar)
                    system('clear')
                    print('\n')
                    gracz.wyrysuj()
                    input(CC("Gotów!", 'cyan') + CC(' /: ', 'yellow'))
                    system('clear')
                    flaga2 = True
                if flaga2:
                    break

                flaga = True
                for e in ws_pp:
                    if not (e in wzorzec):
                        flaga = False
                        break
            if flaga2:
                break
            punkty = []
            p, k = ws_pp
            x1, y1 = ord(p[0]) - 96, int(p[1:])
            x2, y2 = ord(k[0]) - 96, int(k[1:])
            dx, dy = modul(x2 - x1), modul(y2 - y1)
            rozmiar = max(dx, dy)

            if max(dx, dy) > 0:
                for u in range(max(dx, dy) + 1):
                    o = int(min(x1, x2) + (dx / max(dx, dy)) * u)
                    p = int(min(y1, y2) + (dy / max(dx, dy)) * u)
                    punkty.append(chr(o + 96) + str(p))
            fl2 = True
            for p in punkty:
                if not (p in wzorzec):
                    fl2 = False
                    break

            rozmiar += 1
            if rozmiar not in statek:
                fl2 = False

            if not (x1 == x2 or y1 == y2):
                fl2 = False

        if flaga2:
            break

        for x in punkty:
            wzorzec.remove(x)

        poczatek, koniec = ws_pp
        gracz.ustaw_statek(poczatek, koniec)
        statek.remove(gracz.ustaw_statek(poczatek, koniec))
        system("clear")


def glowna_petla(gracz_pierwszy, gracz_drugi):
    for s in gracz_pierwszy.moje_okrety:
        if gracz_pierwszy.moje_okrety.count(s) != 1:
            gracz_pierwszy.moje_okrety.remove(s)

    for s in gracz_drugi.moje_okrety:
        if gracz_drugi.moje_okrety.count(s) != 1:
            gracz_drugi.moje_okrety.remove(s)


    a1 = '\n\n' * 4
    a2 = CC(34 * " " + "ZAKOŃCZ GRĘ ", 'cyan')
    a3 = CC(" [0]\n\n" + " " * 10, "yellow")
    a4 = CC(34 * " " + "MENU GŁÓWNE ", "cyan")
    a5 = CC(" [1]\n\n", 'yellow')
    a6 = CC("/: ", 'yellow')
    a7 = CC(34 * " " + "KONTYNUUJ   ", "cyan")
    a8 = CC(" [c]\n\n", 'yellow')
    wzor1 = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    wzor2 = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    while True:
        pierwszy = True
        while pierwszy:
            gdzie = ''
            while not (gdzie in wzor1):
                system("clear")
                print('\n     {}'.format(CC(gracz_pierwszy.nick, 'cyan')))
                gracz_pierwszy.wyrysuj()
                if USTAWIENIE.podglad_statkow:
                    print("\n       {}\n".format(" ,".join([CC(' ▦', 'green') * i for i in [len(a) for a in gracz_drugi.moje_okrety]])))
                gdzie = input(CC(4*" " + "&: ", 'yellow'))
                system("clear")

                if gdzie.lower() == 'menu':
                    co_dalej = 22
                    while co_dalej not in ['c', 'C', '1', '0']:
                        system("clear")
                        co_dalej = input("{}{}{}{}{}{}{}{}".format(a1, a7, a8, a4, a5, a2, a3, a6))
                    if co_dalej == '1':
                        return True
                    elif co_dalej == '0':
                        return False
                    elif co_dalej in ('c', 'C'):
                        continue

            pierwszy = gracz_pierwszy.strzel(gracz_drugi, gdzie)
            wzor1.remove(gdzie)
            system("clear")
            print('\n')
            gracz_pierwszy.wyrysuj()
            if USTAWIENIE.podglad_statkow:
                print("\n       {}\n\n\n".format(" ,".join([CC(' ▦', 'green') * i for i in [len(a) for a in gracz_drugi.moje_okrety]])))

            if gracz_drugi.moje_okrety == []:
                ax = CC("\n{} Gratulacje! Wygrałeś!\n\n\n".format(" " * 30), 'cyan')
                print(ax)
                dalej = input(CC(10*" " + "/: ", 'yellow'))
                co_dalej = 22

                while co_dalej not in [1, 0]:
                    system('clear')
                    co_dalej = input("{}{}{}{}{}{}".format(a1, a4, a5, a2, a3, a6))

                    if co_dalej.isdigit():
                        co_dalej = int(co_dalej)
                if co_dalej == 1:
                    return True
                else:
                    return False
        dalej = input(CC("Gotów!", 'cyan') + CC(' /: ', 'yellow'))
        system("clear")
        dalej = input(CC("\n\n Dalej", 'cyan') + CC(' /: ', 'yellow'))
        drugi = True

        while drugi:
            gdzie = ''
            while not (gdzie in wzor2):
                system("clear")
                print('\n     {}'.format(CC(gracz_drugi.nick, 'yellow')))
                gracz_drugi.wyrysuj()
                if USTAWIENIE.podglad_statkow:
                    print("\n       {}\n".format(" ,".join([CC(' ▦', 'green') * i for i in [len(a) for a in gracz_pierwszy.moje_okrety]])))
                gdzie = input(CC(4*" " + "&: ", 'yellow'))
                system("clear")

                if gdzie.lower() == 'menu':
                    co_dalej = 22
                    while co_dalej not in ['c', 'C', '1', '0']:
                        system("clear")
                        co_dalej = input("{}{}{}{}{}{}{}{}".format(a1, a7, a8, a4, a5, a2, a3, a6))
                    if co_dalej == '1':
                        return True
                    elif co_dalej == '0':
                        return False
                    elif co_dalej in ('c', 'C'):
                        continue

            drugi = gracz_drugi.strzel(gracz_pierwszy, gdzie)
            wzor2.remove(gdzie)
            system("clear")
            print("\n")
            gracz_drugi.wyrysuj()
            if USTAWIENIE.podglad_statkow:
                print("\n       {}\n\n\n".format(" ,".join([CC(' ▦', 'green') * i for i in [len(a) for a in gracz_pierwszy.moje_okrety]])))

            if gracz_pierwszy.moje_okrety == []:
                ax = CC("\n{} Gratulacje! Wygrałeś!\n\n\n".format(" " * 30), 'cyan')
                print(ax)
                dalej = input(CC(10*" " + "/: ", 'yellow'))
                co_dalej = 22
                while co_dalej not in [1, 0]:
                    system("clear")
                    co_dalej = input("{}{}{}{}{}{}".format(a1, a4, a5, a2, a3, a6))
                    if co_dalej.isdigit():
                        co_dalej = int(co_dalej)
                if co_dalej == 1:
                    return True
                else:
                    return False

        dalej = input(CC("Gotów!", 'cyan') + CC(' /: ', 'yellow'))
        system("clear")
        dalej = input(CC("\n\n Dalej", 'cyan') + CC(' /: ', 'yellow'))


def gra_dwuosobowa(gr1, gr2):
    global USTAWIENIE
    zaczyna = randint(1,2)
    zaczyna = 1

    g1_statki, g2_statki = USTAWIENIE.rozmiary_statkow, USTAWIENIE.rozmiary_statkow
    temporary = [a for a in g1_statki]
    temporary2 = [a for a in g1_statki]
    system("clear")

    if zaczyna == 1:
        print('\n' * 5 + " Zaczyna {} !".format(CC(gr1.nick, 'cyan')))
        petla_poczatkowa(gr1, g1_statki)
        #dziwna dziura więc i łatka jest dziwna
        USTAWIENIE = USTAWIENIA(temporary, USTAWIENIE.podglad_statkow)
        g1_statki, g2_statki = USTAWIENIE.rozmiary_statkow, USTAWIENIE.rozmiary_statkow

        print("\n"*14)
        input(CC(10*" " + "/: ", 'yellow'))
        system("clear")
        print("\n" * 14)
        input(CC(10 * " " + "/: ", 'yellow'))
        petla_poczatkowa(gr2, g2_statki)
        USTAWIENIE = USTAWIENIA(temporary2, USTAWIENIE.podglad_statkow)

        print("\n" * 14)
        input(CC(10 * " " + "/: ", 'yellow'))
        system("clear")
        print("\n" * 14)
        input(CC(10 * " " + "/: ", 'yellow'))
        #input("ustawienie {}".format(USTAWIENIE.rozmiary_statkow))
        return glowna_petla(gr1, gr2)

    elif zaczyna == 2:
        print('\n' * 5 + " Zaczyna {} !".format(CC(gr2.nick, 'cyan')))
        petla_poczatkowa(gr2, g2_statki)
        USTAWIENIE = USTAWIENIA(temporary, USTAWIENIE.podglad_statkow)
        g1_statki, g2_statki = USTAWIENIE.rozmiary_statkow, USTAWIENIE.rozmiary_statkow

        print("\n" * 14)
        input(CC(10 * " " + "/: ", 'yellow'))
        system("clear")
        print("\n" * 14)
        input(CC(10 * " " + "/: ", 'yellow'))
        petla_poczatkowa(gr1, g1_statki)
        USTAWIENIE = USTAWIENIA(temporary2, USTAWIENIE.podglad_statkow)
        g1_statki, g2_statki = USTAWIENIE.rozmiary_statkow, USTAWIENIE.rozmiary_statkow

        print("\n" * 14)
        input(CC(10 * " " + "/: ", 'yellow'))
        system("clear")
        print("\n" * 14)
        input(CC(10 * " " + "/: ", 'yellow'))
        return glowna_petla(gr2, gr1)


def glowna_petla_KOMP(gracz_pierwszy, komputer1, EXPERT):
    for s in gracz_pierwszy.moje_okrety:
        if gracz_pierwszy.moje_okrety.count(s) != 1:
            gracz_pierwszy.moje_okrety.remove(s)

    for s in komputer1.moje_okrety:
        if komputer1.moje_okrety.count(s) != 1:
            komputer1.moje_okrety.remove(s)


    a1 = '\n\n' * 4
    a2 = CC(34 * " " + "ZAKOŃCZ GRĘ     ", 'cyan')
    a3 = CC(" [0]\n\n" + " " * 10, "yellow")
    a4 = CC(34 * " " + "MENU GŁÓWNE     ", "cyan")
    a5 = CC(" [1]\n\n", 'yellow')

    a41 = CC(34 * " " + "WYBÓR ROZGRYWKI ", "cyan")
    a51 = CC(" [b]\n\n", 'yellow')

    a6 = CC("/: ", 'yellow')
    a7 = CC(34 * " " +  "KONTYNUUJ GRĘ   ", "cyan")
    a8 = CC(" [c]\n\n", 'yellow')
    a5 = a5 + a41 + a51
    wzor1 = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    wzor2 = [chr(i) + str(x) for i in range(97, 107) for x in range(1, 11)]
    while True:
        pierwszy = True
        while pierwszy:
            system('clear')
            gdzie = ''
            while not (gdzie in wzor1):
                system("clear")
                print('\n     {}'.format(CC(gracz_pierwszy.nick, 'cyan')))
                gracz_pierwszy.wyrysuj()
                if USTAWIENIE.podglad_statkow:
                    print("\n       {}\n".format(" ,".join([CC(' ▦', 'green') * i for i in [len(a) for a in komputer1.moje_okrety]])))
                gdzie = input(CC(4*" " + "&: ", 'yellow'))

                if gdzie.lower() == 'menu':
                    co_dalej = 22
                    while co_dalej not in ['c', 'C', '1', '0', 'b', 'B']:
                        system("clear")
                        co_dalej = input("{}{}{}{}{}{}{}{}".format(a1, a7, a8, a4, a5, a2, a3, a6))
                    if co_dalej == '1':
                        return True
                    elif co_dalej == '0':
                        return False
                    elif co_dalej in ('c', 'C'):
                        continue
                    elif co_dalej in ['b', 'B']:
                        return 'xD'


            system('clear')
            pierwszy = gracz_pierwszy.strzel(komputer1, gdzie)
            wzor1.remove(gdzie)
            system("clear")
            print('\n')
            gracz_pierwszy.wyrysuj()
            if USTAWIENIE.podglad_statkow:
                print("\n       {}\n\n\n".format(" ,".join([CC(' ▦', 'green') * i for i in [len(a) for a in komputer1.moje_okrety]])))

            if komputer1.moje_okrety == []:
                ax = CC("\n{} Gratulacje! Wygrałeś!\n\n\n".format(" " * 30), 'cyan')
                print(ax)
                dalej = input(CC(10*" " + "/: ", 'yellow'))

                co_dalej = 22
                while co_dalej not in ['1', '0', 'b', 'B']:
                    system("clear")
                    co_dalej = input("{}{}{}{}{}{}".format(a1, a4, a5, a2, a3, a6))

                if co_dalej == '1':
                    return True
                elif co_dalej == '0':
                    return False
                elif co_dalej == 'b':
                    return 'xD'

        dalej = input(CC("Gotów!", 'cyan')+CC(' /: ', 'yellow'))
        system("clear")
        #dalej = input(CC("\n\n\n\n Dalej: ", 'cyan'))
        drugi = True

        while drugi:
            gdzie = komputer1.decyzja_strzalExpert2(gracz_pierwszy, EXPERT) #chwilowo wersja 2
            drugi = komputer1.strzel(gracz_pierwszy, gdzie)
            #komputer1.aktualizacja_EXPERT2([len(e) for i, e in enumerate(gracz_pierwszy.moje_okrety)])     # tu powinna następować aktualizacja mapy - usuwanie zbędnych pól
            # wzor2.remove(gdzie)
            system("clear")
            # komputer1.wyrysuj()

            if drugi == True:
                komputer1.trafienia.append(gdzie)
            #należy zaktualizować listę trafienia jeżeli statek juz zatopiony
            komputer1.aktualizacja_trafionych(gracz_pierwszy)
            if gracz_pierwszy.moje_okrety == []:
                print('     Wygrał komputer!')
                komputer1.wyrysuj()

                dalej = input(CC(10*" " + "/: ", 'yellow'))
                system('clear')
                co_dalej = 22

                while co_dalej not in ['1', '0', 'b', 'B']:
                    system("clear")
                    co_dalej = input("{}{}{}{}{}{}".format(a1, a4, a5, a2, a3, a6))

                if co_dalej == '1':
                    system("clear")
                    return True
                elif co_dalej == '0':
                    system("clear")
                    return False
                elif co_dalej == 'b':
                    system("clear")
                    return 'xD'

                    # dalej = input("Gotów!: ")
        system("clear")
        #dalej = input("Dalej: ")


def gra_zkomputerem(gr1, komputer, EXPERT2 = False):
    global USTAWIENIE
    zaczyna = 1

    g1_statki, komp_statki = USTAWIENIE.rozmiary_statkow , USTAWIENIE.rozmiary_statkow #pierwotnie 544332
    temporary = [a for a in g1_statki]
    temporary2 = [a for a in g1_statki]
    system("clear")
    USTAWIENIE = USTAWIENIA(temporary, USTAWIENIE.podglad_statkow)
    g1_statki, komp_statki = USTAWIENIE.rozmiary_statkow , USTAWIENIE.rozmiary_statkow

    if zaczyna == 1:

        for ui in komp_statki:
            k = komputer.decyzja_ustawienie(ui)
            komputer.ustaw_statek(k[0], k[1])
        USTAWIENIE = USTAWIENIA(temporary, USTAWIENIE.podglad_statkow)
        g1_statki, komp_statki = USTAWIENIE.rozmiary_statkow, USTAWIENIE.rozmiary_statkow

        print('\n' * 5 + " Zaczyna {} !".format(CC(gr1.nick, 'green')))
        petla_poczatkowa(gr1, g1_statki)
        USTAWIENIE = USTAWIENIA(temporary2, USTAWIENIE.podglad_statkow)

        return glowna_petla_KOMP(gr1, komputer, EXPERT2)

def mini_menu(gdzie, decyzja_powrot = False):
    a1 = '\n\n' * 8
    a7 = CC(34 * " " + "KONTYNUUJ   ", "cyan")
    a8 = CC(" [c]\n\n", 'yellow')
    a4 = CC(34 * " " + "MENU GŁÓWNE ", "cyan")
    a5 = CC(" [1]\n\n", 'yellow')
    a45 = CC(34 * " " +"POWRÓT      ", "cyan")
    a55 = CC(" [b]\n\n", 'yellow')

    a2 = CC(34 * " " + "ZAKOŃCZ GRĘ ", 'cyan')
    a3 = CC(" [0]\n\n" + " " * 10, "yellow")
    a6 = CC("/: ", 'yellow')
    do_petli = ['c', 'C', '1', '0']
    if decyzja_powrot:
        a5 = a5+a45+a55
        do_petli += ['b', 'B']

    if gdzie.lower() == 'menu':
        co_dalej = 22
        while co_dalej not in do_petli:
            system("clear")
            co_dalej = input("{}{}{}{}{}{}{}{}".format(a1, a7, a8, a4, a5, a2, a3, a6))
        if co_dalej == '1':
            return True
        elif co_dalej == '0':
            return False
        elif co_dalej in ('c', 'C'):
            return 'continue'
        elif decyzja_powrot and co_dalej in ('b', 'B'):
            return 'b'




def bede_grau():
    global USTAWIENIE

    intro()
    ciag_dalszy = True

    while ciag_dalszy:
        flaga = False
        tryb = menu_glowne()

        if tryb == 'a':
            nazwy = []
            while len(nazwy) < 2 or len(nazwy) > 2:
                system('clear')
                nazwy = (input("{}{}".format('\n' * 13, CC('Wprowadź nazwę pierwszego oraz (po spacji) drugiego gracza', 'cyan'))+CC(' &: ', 'yellow'))).split(" ")
                mini = mini_menu(nazwy[0].lower())
                system("clear")
                if mini == True:
                    ciag_dalszy = True
                    flaga = True
                    break
                elif mini == False:
                    ciag_dalszy = False
                    flaga = True
                    break
                elif mini == 'continue':
                    continue
            if flaga:
                continue

            nick1, nick2 = nazwy
            gracz1, gracz2 = Gracz(nick1), Gracz(nick2)
            ciag_dalszy = gra_dwuosobowa(gracz1, gracz2)

        while tryb == 'k':
            flaga2 = False
            tresc = ['\n' * 13, CC(9 * ' ' + 'RUTYNOWY ZWIAD        ', 'cyan'), CC('[r]', 'yellow'),
                     2 * '\n', CC(9 * ' ' + 'STARCIE NA RUBIEŻACH  ', 'cyan'), CC('[u]', 'yellow'),
                     5 * '\n', CC('  &: ', 'yellow')]
            system('clear')
            poziom = ''
            while len(poziom) == 0:
                system('clear')
                poziom = input("{}".format("".join(tresc)))
                mini = mini_menu(("".join(poziom.split(' '))).lower())
                system("clear")
                if mini == True: #wyjście do menu glownego
                    ciag_dalszy = True
                    flaga = True
                    break
                elif mini == False: # wyjscie z gry
                    ciag_dalszy = False
                    flaga = True
                    break
                elif mini == 'continue': #kontunuacja
                    poziom = ''
                    continue
                elif poziom not in ['r', 'u']:
                    poziom = ''
                    continue
            if flaga:
                break

            system('clear')
            nazwa = ''
            while len(nazwa) == 0:
                system('clear')
                nazwa = input("{}{}".format('\n' * 13, CC('Wprowadź nazwę gracza', 'cyan') + CC(' &: ', 'yellow')))
                mini = mini_menu(("".join(nazwa.split(' '))).lower(), True)
                system("clear")
                if mini == True: # powinno wyrzucic do menu glownego
                    ciag_dalszy = True
                    flaga = True
                    break
                elif mini == False: # wyjscie z gry
                    ciag_dalszy = False
                    flaga = True
                    break
                elif mini == 'continue': # krec dalej
                    nazwa = ''
                    continue
                elif mini == 'b': #powrot do początku petli
                    flaga2 = True
                    break

            if flaga:
                break
            if flaga2:
                continue

            if poziom == 'r':
                nick, robot = nazwa, 'SI'
                gracz1, gracz_robot = Gracz(nick), Robot(robot)
                ciag_dalszy = gra_zkomputerem(gracz1, gracz_robot)

            elif poziom == 'u': #POPRAWIĆ NA ROZGRYWKĘ Z TRUDNIEJSZYM ALGORYTMEM
                nick, robot = nazwa, 'SI'
                gracz1, gracz_robot = Gracz(nick), Robot(robot)
                ciag_dalszy = gra_zkomputerem(gracz1, gracz_robot, True)


            if ciag_dalszy in [True, False]:
                flaga = True
                break
            elif ciag_dalszy == 'xD':
                ciag_dalszy = True
                continue

        if flaga:
            continue

        elif tryb == 's':
            system("clear")
            dalej = ''
            while dalej not in ['1', '0']:
                system('clear')
                tresc = (CC('\n\n\n\n     W WIERSZU POLECENIA ZACZYNAJĄCYM SIĘ OD ZNAKU [', 'cyan') + CC("&:",
                                                                                                         'yellow') +
                         CC("] MOŻESZ \n     UŻYWAĆ KOMENDY '", 'cyan') +
                         CC("MENU", 'yellow') + CC("', ABY WYŚWIETLIĆ DODATKOWE OPCJE.\n ", 'cyan') + CC("", 'cyan'))

                tresc2 = (CC("\n     MOŻNA RÓWNIEŻ POSŁUŻYĆ SIĘ POLECENIEM '", 'cyan') + CC("SET SHIPS", 'yellow') +
                          CC(
                              "' ABY W TRAKCIE\n     REJESTROWANIA STATKÓW PROCES TEN DOKONAŁ SIĘ AUTOMATYCZNIE, \n     NAWET JEŻELI JAKIEŚ OKRĘTY ZOSTAŁY JUŻ PRZEZ CIEBIE USTAWIONE.\n\n     ABY NAWIGOWAĆ PO GRZE NALEŻY WPISAĆ LITERĘ ODPOWIADAJĄCĄ ŻĄÐANEMU \n     DZIAŁANIU, A NASTĘPNIE ZATWIERDZIĆ PRZYCISKIEM ENTER.\n\n     REJESTRACJA STATKÓW ODBYWA SIĘ POPRZEZ WPISANIE KOORDYNATÓW POCZĄTKU \n     I KOŃCA DANEGO STATKU, ODDZIELONE JEDNĄ SPACJĄ. PRZYKŁAD: a1 a3\n     USTAWIA STATEK DŁUGOŚCI 3. ABY STRZELIĆ W POLE A3 NALEŻY WPISAĆ a3\n     A NASTĘPNIE ZATWIERDZIĆ ENTEREM.",
                              'cyan'))
                print(tresc + tresc2)
                p = 3 * "\n" + '    ' * 3 + CC('POWRÓT DO MENU  ', 'cyan') + CC('[1]\n', 'yellow')
                d = '    ' * 3 + CC('WYJŚCIE Z GRY   ', 'cyan') + CC('[0]\n\n', 'yellow')
                b = CC(5 * " " + "/: ", 'yellow')
                dalej = input("{}{}{}".format(p, d, b))
                system("clear")

            if dalej == '1':
                ciag_dalszy = True
                system("clear")
                continue
            elif dalej == '0':
                ciag_dalszy = False
                system("clear")
                continue
            pass

        elif tryb == 'u':
            system("clear")
            dalej = ' '
            while dalej not in ['1', '0']:
                system('clear')
                tresc = ("\n    USTAWIENIA\n[q] Aktualne rodzaje statkow: {}\n[p] podglad E/D {}\nRESET USTAWIEN - komenda RESET SETTINGS\nZAPIS USTAWIEN DO PLIKU - komenda SAVE".format(USTAWIENIE.rozmiary_statkow, USTAWIENIE.podglad_statkow))
                print(tresc)
                p = 3 * "\n" + '    ' * 3 + CC('POWRÓT DO MENU  ', 'cyan') + CC('[1]\n', 'yellow')
                d = '    ' * 3 + CC('WYJŚCIE Z GRY   ', 'cyan') + CC('[0]\n\n', 'yellow')
                b = CC(5 * " " + "/: ", 'yellow')
                dalej = input("{}{}{}".format(p, d, b))
                if dalej == "":
                    dalej = " "
                system("clear")

                if dalej == '1':
                    ciag_dalszy = True
                    system("clear")
                    continue
                elif dalej == '0':
                    ciag_dalszy = False
                    system("clear")
                    continue
                elif dalej[0] == "q":
                    dalej = [d for d in dalej.split(" ") if d.isdigit()]
                    nowe_statki = [int(s) for s in dalej if int(s) in range(2,10)]
                    if nowe_statki != []:
                        USTAWIENIE = USTAWIENIA(qsort(nowe_statki)[::-1], USTAWIENIE.podglad_statkow)
                    system("clear")
                elif dalej[0] == "p":
                    dalej = [d for d in dalej if d in ('e', 'E', 'd', 'D')][0]
                    if dalej in ('e', 'E'):
                        USTAWIENIE = USTAWIENIA(USTAWIENIE.rozmiary_statkow, True)
                    elif dalej in ('d', 'D'):
                        USTAWIENIE = USTAWIENIA(USTAWIENIE.rozmiary_statkow, False)
                    system('clear')
                elif dalej.lower() == "reset settings":
                    USTAWIENIE.reset()
                    system('clear')
                elif dalej.lower() == "save":
                    pickle.dump(USTAWIENIE, open('ships.conf', 'wb'))
                    system('clear')



            pass

        elif tryb == 'p':
            system("clear")
            ciag_dalszy = False


bede_grau()
#zrobić losowość w  trybie dla dwóch graczy
