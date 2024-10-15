# MONOPOLY
# IES ESTEVE TERRADAS I ILLAS
# DAM 2024-2025
# RUBÉN BELLIDO Y ALEJANDRO LÓPEZ

import sys
import os

MIN_DINERS_BANCA = 500000

tauler = {}
banca = 0
casella_mesures = {
    "alt": 2,
    "ampla": 8
}

tauler_mesures = {
    "ampla_total": 64,
    "ampla_partida": 10,
    "files": 7,
    "columnes": 7
}

jugadors = {
    "Vermell": {
        "nom": "Vermell",
        "icona": "V",
        "diners": 0,
        "posicio": [],
        "propietats": [],
        "es_preso": False,
        "cartes": []
    },
    "Groc": {
        "nom": "Groc",
        "icona": "G",
        "diners": 0,
        "posicio": [],
        "propietats": ["Gracia", "Pl Cat"],
        "es_preso": False,
        "cartes": []
    },
    "Taronja": {
        "nom": "Taronja",
        "icona": "T",
        "diners": 0,
        "posicio": [],
        "propietats": ["Aribau"],
        "es_preso": False,
        "cartes": []
    },
    "Blau": {
        "nom": "Blau",
        "icona": "B",
        "diners": 0,
        "posicio": [],
        "propietats": [],
        "es_preso": False,
        "cartes": ["Sortir preso"]
    }
}

caselles = {
    "Lauria": {
        "nom_acortat": "Lauria",
        "lloguer_casa": 10,
        "lloguer_hotel": 15,
        "preu_terreny": 50,
        "comprar_casa": 300,
        "comprar_hotel": 250
    },
}

posicions_caselles_files = [1, 5, 8, 11, 14, 17, 19]
posicions_caselles_columnes = [0, 10, 19, 28, 37, 45, 55]
posicions_separadors = [[0, 4], [0, 22]]
posicions_informacio = [[66, 1], [66, 4], [66, 9], [66, 14], [66, 19]]
posicio_estat = [5, 11]

#region FuncionesInteraccionConsola
def clearScreen():
    if os.name == 'nt':     # Si estàs a Windows
        os.system('cls')
    else:                   # Si estàs a Linux o macOS
        os.system('clear')

def mou_cursor(x, y):
    # Escapamos y nos movemos a la posición indicada
    sys.stdout.write(f"\033[{y};{x}H")
    # Forzamos un aplicado del buffer
    sys.stdout.flush()
#endregion FuncionesInteraccionConsola