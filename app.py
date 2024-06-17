import random
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap


class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.uiScale = 2

        self.gameWindow = None
        self.dodajHasloWindow = None

        self.hasla = []
        self.kategorie = []
        self.plikKategorie = "kategorie.csv"
        self.plikHasla = "hasla.csv"
        self.zaladujKategorie()
        self.zaladujHasla()

        self.poprzednieHaslo = None

        self.setWindowTitle("Menu")
        self.setFixedSize(200 * self.uiScale, 200 * self.uiScale)

        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        self.setWindowIcon(QIcon("images\\icon.png"))

        buttonGraj = QPushButton("GRAJ", self)
        buttonDodajHaslo = QPushButton("DODAJ HASŁO", self)
        buttonWyjdz = QPushButton("WYJDŹ", self)

        buttonGraj.clicked.connect(self.buttonGrajAction)
        buttonDodajHaslo.clicked.connect(self.buttonDodajHasloAction)
        buttonWyjdz.clicked.connect(QApplication.quit)
        
        
        buttonGraj.setFixedSize(150 * self.uiScale, 50 * self.uiScale)
        buttonDodajHaslo.setFixedSize(150 * self.uiScale, 50 * self.uiScale)
        buttonWyjdz.setFixedSize(150 * self.uiScale, 50 * self.uiScale)

        buttonGraj.setStyleSheet(f"background-color: #2BC459; color: white;font-weight: bold;border-radius: 8px; font-size: {11 * self.uiScale}px;")
        buttonDodajHaslo.setStyleSheet(f"background-color: #008CBA; color: white;font-weight: bold;border-radius: 8px; font-size: {11 * self.uiScale}px;")
        buttonWyjdz.setStyleSheet(f"background-color: #C42B5E; color: white;font-weight: bold;border-radius: 8px; font-size: {11 * self.uiScale}px;")

        layout = QVBoxLayout()

        layout.addWidget(buttonGraj)
        layout.addWidget(buttonDodajHaslo)
        layout.addWidget(buttonWyjdz)

        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
    

    def buttonGrajAction(self):
        self.rozpocznijGre()
        self.hide()
    

    def buttonDodajHasloAction(self):
        self.dodajHasloWindow = DodajHaslo(self)
        self.dodajHasloWindow.show()
        self.hide()


    def zaladujKategorie(self):
        try:
            with open(self.plikKategorie, "r", encoding='utf-8') as file:
                for line in file.readlines():
                    try:
                        kategoria = line.strip().upper()
                        if kategoria not in self.kategorie:
                            self.kategorie.append(kategoria)
                    except:
                        pass
        except FileNotFoundError:
            with open(self.plikKategorie, "w", encoding='utf-8') as file:
                pass
    

    def zaladujHasla(self):
        try:
            with open(self.plikHasla, "r", encoding='utf-8') as file:
                for line in file.readlines():
                    try:
                        hasloKat = line.strip().split(";")
                        hasloKatTuple = (hasloKat[0].upper(), hasloKat[1].upper())
                        if not (hasloKatTuple in self.hasla):
                            self.hasla.append(hasloKatTuple)
                        if not (hasloKatTuple[1] in self.kategorie):
                            self.kategorie.append(hasloKatTuple[1])
                    except:
                        pass
        except FileNotFoundError:
            with open(self.plikHasla, "w", encoding='utf-8') as file:
                pass


    def dodajHaslo(self, haslo, kategoria):
        haslo = haslo.strip()
        if len(haslo) == 0 or ";" in haslo or len(haslo) > 22:
            self.dialog = self.Potwierdzenie(czyHaslo=True, czyBlad=True)
            self.dialog.show()
            return
        if (haslo,kategoria) not in self.hasla:
            self.hasla.append((haslo,kategoria))
            with open(self.plikHasla, "a", encoding='utf-8') as file:
                file.write(haslo + ";" + kategoria + "\n")
            self.dialog = self.Potwierdzenie(czyHaslo=True, czyBlad=False)
            self.dialog.show()


    def dodajKategorie(self, kategoria):
        kategoria = kategoria.strip()
        if len(kategoria) == 0 or ";" in kategoria or len(kategoria) > 22:
            self.dialog = self.Potwierdzenie(czyHaslo=False, czyBlad=True)
            self.dialog.show()
            return
        if kategoria not in self.kategorie:
            self.kategorie.append(kategoria)
            with open(self.plikKategorie, "a", encoding='utf-8') as file:
                file.write(kategoria + "\n")
            self.dialog = self.Potwierdzenie(czyHaslo=False, czyBlad=False)
            self.dialog.show()


    def losujHaslo(self):
        return random.choice(self.hasla)


    def rozpocznijGre(self):
        losowanie = self.losujHaslo()
        while losowanie == self.poprzednieHaslo:
            losowanie = self.losujHaslo()
        
        self.poprzednieHaslo = losowanie
        
        haslo, kategoria = losowanie[0], losowanie[1]

        self.gameWindow = Gra(kategoria, haslo, self)
        self.gameWindow.show()
    

    def getKategorie(self):
        return self.kategorie


    def getHasla(self):
        return self.hasla


    class Potwierdzenie(QWidget):
        def __init__(self, czyHaslo, czyBlad):
            super().__init__()

            self.uiScale = 2

            self.setWindowTitle(" ")
            self.setFixedSize(110 * self.uiScale, 60 * self.uiScale)

            if czyBlad:
                self.setFixedSize(160 * self.uiScale, 60 * self.uiScale)

            self.setWindowIcon(QIcon("images\\icon.png"))
            self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)

            self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

            layout = QVBoxLayout()

            font = QFont()
            font.setPointSize(11)

            if czyHaslo:
                if czyBlad:
                    tresc = "Nieprawidłowe hasło."
                else:
                    tresc = "Dodano hasło."
            else:
                if czyBlad:
                    tresc = "Nieprawidłowa kategoria."
                else:
                    tresc = "Dodano kategorię."

            label = QLabel(tresc, self)
            label.setFont(font)
            layout.addWidget(label, alignment=Qt.AlignCenter)

            buttonOK = QPushButton('OK', self)
            buttonOK.clicked.connect(self.close)
            layout.addWidget(buttonOK, alignment=Qt.AlignCenter)

            self.setLayout(layout)
             

