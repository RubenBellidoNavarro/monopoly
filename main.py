# MONOPOLY
# IES ESTEVE TERRADAS I ILLAS
# DAM 2024-2025
# RUBÉN BELLIDO Y ALEJANDRO LÓPEZ

import sys
import os
import re # Usado para poder cambiar el nombre de las casillas de 'Sort' i 'Caixa', ya que necesitan un 1 o 2 al final para identificarlas correctamente
import time
import random
import json
from colorama import just_fix_windows_console # Paquete para que la terminal de Windows entienda los caràcteres ANSI y podamos mover el cursor a la posición que deseemos

just_fix_windows_console()

#region VARIABLESYCONSTANTES
MIN_DINERS_BANCA = 500000
MAX_LINIES_JUGADES = 13
MAX_CASELLES = 24

banca = 1000000

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

#Array que utilizaremos para generar un orden de tiradas, y el diccionario de jugadores:
noms_jugadors = ["Vermell","Groc","Taronja","Blau"]

#Tupla que utilizaremos para recorrerla con las tiradas de dados, de forma ordenada:
caselles_ordenades = ["Sortida",
                      "Lauria",
                      "Rosselló",
                      "Sort1",
                      "Marina",
                      "C. de cent",
                      "Presó",
                      "Muntaner",
                      "Aribau",
                      "Caixa1",
                      "Sant Joan",
                      "Aragó",
                      "Parking",
                      "Urquinaona",
                      "Fontana",
                      "Sort2",
                      "Les Rambles",
                      "Pl. Catalunya",
                      "Anr pró",
                      "P.Àngel",
                      "Via Augusta",
                      "Caixa2",
                      "Balmes",
                      "Pg. de Gràcia"
                      ]

caselles_posicions = [("Sortida",[19,55]),
                      ("Lauria",[19,46]),
                      ("Rosselló",[19,37]),
                      ("Sort1",[19,28]),
                      ("Marina",[19,19]),
                      ("C. de cent",[19,10]),
                      ("Presó",[19,0]),
                      ("Muntaner",[17,0]),
                      ("Aribau",[14,0]),
                      ("Caixa1",[11,0]),
                      ("Sant Joan",[8,0]),
                      ("Aragó",[5,0]),
                      ("Parking",[1,0]),
                      ("Urquinaona",[1,10]),
                      ("Fontana",[1,19]),
                      ("Sort2",[1,28]),
                      ("Les Rambles",[1,37]),
                      ("Pl. Catalunya",[1,46]),
                      ("Anr pró",[1,55]),
                      ("P.Àngel",[5,55]),
                      ("Via Augusta",[8,55]),
                      ("Caixa2",[11,55]),
                      ("Balmes",[14,55]),
                      ("Pg. de Gràcia",[17,55])
                      ]


caselles_ordenades_nom_acortat = ("Sortida",
                      "Lauria",
                      "Rossell",
                      "Sort",
                      "Marina",
                      "Consell",
                      "Presó",
                      "Muntan",
                      "Aribau",
                      "Caixa",
                      "S.Joan",
                      "Aragó",
                      "Parking",
                      "Urqinoa",
                      "Fontan",
                      "Sort",
                      "Rambles",
                      "Pl.Cat",
                      "Anr pró",
                      "Angel",
                      "Augusta",
                      "Caixa",
                      "Balmes",
                      "Gracia"
                      )

#Tupla de casillas que no tienen asociadas precios ni pertenencias a ningún jugador:
caselles_especials = ("Sort","Presó","Caixa","Anr pró","Sortida","Parking", "Sort1", "Sort2", "Caixa1", "Caixa2")
cartes_sort = [
    "Sortir presó",
    "Anar presó",
    "Anar sortida",
    "Anar 3 espais enrera",
    "Fer reparacions a les propietats",
    "Ets escollit alcalde"
]
cartes_caixa = [
    "Sortir presó",
    "Anar presó",
    "Error de la banca al teu favor",
    "Despeses mèdiques",
    "Despeses escolars",
    "Reparacions al carrer",
    "Concurs de bellesa"
]

#Tupla que contiene la utilización de los precios para cada casilla junto a su nombre acortado.
#Las posiciones de cada tupla corresponden a:
### [0] = Nombre acortado casilla
### [1] = Precio Llogar casa
### [2] = Precio Llogar hotel
### [3] = Precio Comprar Terreny
### [4] = Precio Comprar casa
### [5] = Precio Comprar hotel
preus_caselles = (("Lauria",10,15,50,200,250),
                  ("Rosell",10,15,50,225,255),
                  ("Marina",15,15,50,250,260),
                  ("Consell",15,20,50,275,265),
                  ("Muntan",20,20,60,300,270),
                  ("Aribau",20,20,60,300,270),
                  ("S.Joan",25,25,60,350,280),
                  ("Aragó",25,25,60,375,285),
                  ("Urqinoa",30,25,70,400,290),
                  ("Fontan",30,30,70,425,300),
                  ("Rambles",35,30,70,450,310),
                  ("Pl.Cat",35,30,70,475,320),
                  ("Angel",40,35,80,500,330),
                  ("Augusta",40,35,80,525,340),
                  ("Balmes",50,40,80,550,350),
                  ("Gracia",50,40,80,550,350))

etiquetes_preus_caselles = ("nom_acortat",
                            "lloguer_casa",
                            "lloguer_hotel",
                            "preu_terreny",
                            "comprar_casa",
                            "comprar_hotel")

posicions_caselles_files = [1, 5, 8, 11, 14, 17, 19]
posicions_caselles_columnes = [0, 10, 19, 28, 37, 45, 55]
posicions_separadors = [[0, 4], [0, 22]]
posicions_informacio = [[66, 1], [66, 4], [66, 9], [66, 14], [66, 19]]
posicio_jugades = [5, 11]
posicio_preso = [19, 0]
posicio_sortida = [19,55]

jugades = []
#endregion VARIABLESYCONSTANTES

#region FuncionesInteraccionConsola
def clearScreen() -> None:
    '''Limpiamos la pantalla de la terminal.

    Retorna: No retorna nada'''
    if os.name == 'nt':     # Si estàs a Windows
        os.system('cls')
    else:                   # Si estàs a Linux o macOS
        os.system('clear')

def mou_cursor(x: int, y: int) -> None:
    '''Movemos el cursor del terminal a la posición seleccionada.

    Input:
        -x(int): Posición en X de la posición a la que debemos mover el cursor.
        -y(int): Posición en Y de la posición a la que debemos mover el cursor.

    Retorna: No retorna nada'''
    # Escapamos y nos movemos a la posición indicada
    sys.stdout.write(f"\033[{y};{x}H")
    # Forzamos un aplicado del buffer
    sys.stdout.flush()

def imprimeix_per_pantalla(tauler: list, banca: int, jugadors: dict, jugades: list) -> None:
    '''Limipamos la pantalla e imprimimos el tablero, información y jugadas

    Input:
        -tauler(lisy): Lista con los diccionarios que contienen la información de las casillas.
        -banca(int): Cantidad de dinero que dispone la banca.
        -jugadors(dict): Diccionario que continene la información de todos los jugadores.
        -jugades(list): Lista con todas las jugadas realizadas.

    Retorna: No retorna nada'''
    clearScreen()
    imprimeix_taula(tauler)
    imprimeix_informacio(banca, jugadors)
    imprimeix_jugades(jugades)
#endregion FuncionesInteraccionConsola

#region GeneracionPartida             
def genera_jugadors(noms_jugadors:list) -> dict:
    '''Genera un diccionario de jugadores, donde cada clave será el nombre 
    del jugador (Ex. "Vermell") y su valor será un diccionario con información 
    sobre el jugador (icona, diners, posicio, propietats, es_preso, cartes).
    
    Inputs:
        -noms_jugadors(list): Lista con los nombres de los 
        jugadores ["Vermell","Groc","Taronja","Blau"]
        
    Retorna:
        -dict_jugadors(dict): Diccionario que contiene la información de cada jugador, asociando 
        a cada clave "Nombre jugador" un diccionario con la información necesaria.'''
    dict_jugadors = {}
    for clau_jugador in noms_jugadors:
        dict_jugadors[clau_jugador] = {
                                        "nom":clau_jugador,
                                        "icona":clau_jugador[0],
                                        "diners":0,
                                        "posicio":[],
                                        "propietats":[],
                                        "es_preso":False,
                                        "torns_preso":0,
                                        "cartes":[]
                                        }
    return dict_jugadors

def genera_noms_complets_sense_especials(caselles_ordenades:tuple) -> tuple:
    '''Genera, a partir de la variable 'caselles_ordenades', una tupla con el mismo contenido, pero omitiendo las casillas
    que realizan funciones especiales en el tablero.
    
    Input:
        -caselles_ordenades(tuple): Tupla que contiene todos los nombres completo de las casillas del tablero,
        en el orden de juego.
        
    Retorna:
        -noms_complets(tuple): Tupla que contiene los nombres de 'caselles_ordenades', omitiendo los valores que
        corresponden a casillas especiales.'''
    noms_complets = []
    for casella in caselles_ordenades:
        if casella not in caselles_especials:
            noms_complets.append(casella)
    noms_complets = tuple(noms_complets)
    return noms_complets

def genera_preus_caselles(caselles_ordenades, preus_caselles, etiquetes_preus_caselles):
    '''Genera un diccionario que contiene los precios de cada casilla.
    
    Input:
        -noms_complets(tuple): Una tupla con los nombres completos de las casillas.
        -preus_caselles(tuple): Una matriz de tuplas que contiene en cada tupla:
        s(NombreAcortado, PrecioAlquilarCasa, PrecioAlquilarHotel, PrecioComprarTerreno, PrecioComprarCasa, PrecioComprarHotel).
        -etiquetes_preus_caselles(tuple): Etiquetas correspondientes a cada valor de cada tupla de la matriz "preus_caselles".
        
    Retorna:
        -dict_preus_caselles(dict): Diccionario que tiene para cada casilla (clave) asociado un diccionario 
        con información sobre los precios de dicha casilla.'''

    dict_preus_caselles = {}

    noms_complets_sense_especials = genera_noms_complets_sense_especials(caselles_ordenades)

    for index, casella in enumerate(noms_complets_sense_especials):
        dict_preus_caselles[casella] = dict(zip(etiquetes_preus_caselles, preus_caselles[index]))

    return dict_preus_caselles

def crea_casella(nom_casella, caselles_ordenades, caselles_ordeandes_nom_acortat, caselles_especials, caselles_posicions):
    '''Genera y retorna un diccionario que contiene la información de la casilla (nombre, nombreAcortado, numCasas, numHoteles, jugadores, posicionCasilla).
    
    Input:
        -nom_casella(str): Nombre de la casilla a definir.
        -caselles_ordenades(tuple): Tupla que contiene los nombres completos de las casillas, en el orden del tablero.
        -caselles_ordeandes_nom_acortat(tuple): Tupla que contiene los nombres acortados de las casillas, en el orden del tablero.
        -caselles_especials(tuple): Tupla que contiene los nombres de las casillas que no pueden tener propietario y realizan funciones especiales dentro de la partida.
        -caselles_posicions(tuple): Matriz de tuplas que relaciona el nombre de una casilla y su posición en el tablero.
        
    Retorna:
        -casella(dict): Diccionario que contiene la información de la casilla.'''

    #Buscamos el índice a partir del nombre de la casilla (este indice coincidirá en todos los arrays que utilizamos):
    index = caselles_ordenades.index(nom_casella)
    nom_casella = re.sub(r'\d+', '', nom_casella)
    
    dict_casella = {    "nom_complet": nom_casella,
                        "nom_acortat": caselles_ordeandes_nom_acortat[index],
                        "cases": 0,
                        "hotels": 0,
                        "jugadors": [""],
                        "posicio": caselles_posicions[index][1],
                        "es_especial": False,
                        "propietari": "banca"
                    }
    
    if nom_casella in caselles_especials:
        dict_casella["es_especial"] = True
        dict_casella["propietari"] = None

    return dict_casella

def genera_tauler(caselles_ordenades, caselles_ordeandes_nom_acortat, caselles_especials, caselles_posicions):
    '''Genera una lista de diccionarios, donde cada diccionario contiene la información de una casilla (nombre, nombreAcortado, numCasas, numHoteles, jugadores, posicionCasilla).
    
    Input:
        -caselles_ordenades(tuple): Tupla que contiene los nombres completos de las casillas, en el orden del tablero.
        -caselles_ordeandes_nom_acortat(tuple): Tupla que contiene los nombres acortados de las casillas, en el orden del tablero.
        -caselles_especials(tuple): Tupla que contiene los nombres de las casillas que no pueden tener propietario y realizan funciones especiales dentro de la partida.
        -caselles_posicions(tuple): Matriz de tuplas que relaciona el nombre de una casilla y su posición en el tablero.
        
    Retorna:
        -tauler(list): Lista de diccionarios, donde cada diccionario contiene la información de una casilla (nombre, nombreAcortado, numCasas, numHoteles, jugadores, posicionCasilla).'''

    tauler = []

    for casella in caselles_ordenades:
        dict_casella = crea_casella(casella, caselles_ordenades, caselles_ordeandes_nom_acortat, caselles_especials, caselles_posicions)
        tauler.append(dict_casella)

    return tauler

def primer_pagament(jugadors):
    '''Añadimos a todos los jugadores 2000€ en sus cuentas.

    Input:
        -jugadors(dict): Diccionario en el que cada clave es un jugador, y su valor asociado es un diccionario con información del jugador (icona, diners, posicio, propietats, es_preso, cartes)
        
    Retorna: No retorna nada'''
    for jugador in jugadors:
        jugadors[jugador]["diners"] = 2000

def ordre_tirada(jugadors):
    '''Mezaclamos el diccionario de jugadores para que tengan un orden aleatorio
    
    Input:
        -jugadors(dict): Diccionario en el que cada clave es un jugador, y su valor asociado es un diccionario con información del jugador (icona, diners, posicio, propietats, es_preso, cartes)
        
    Retorna:
        -ordre_jugadors(list): Lista que contiene los nombres de los jugadores mezclados aleatoriamente. Esta lista marcará el orden de tiradas durante la partida.'''
    ordre_jugadors = list(jugadors.keys())
    random.shuffle(ordre_jugadors)
    return ordre_jugadors
#endregion GeneracionPartida

#region ConsultarDatos

def propietari_casella(casella:str, tauler:list) -> str:
    '''Retorna un string con el propietario de la casilla.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -tauler(list): Lista de diccionarios que contienen la información de cada casilla del tablero.
        
    Retorna:
        -propietari_casella(str): String que contiene el nombre el jugador que posee la casilla.'''
    #Buscamos la casilla en el tablero:
    for dict_casella in tauler:
        if dict_casella["nom_complet"] == casella:
            propietari_casella = dict_casella["propietari"]
            return propietari_casella
        
def jugador_es_propietari(nom_jugador:str, casella:str, tauler:list) -> bool:
    '''Retorna un booleano True en caso de que el jugador sea el propietario de la casilla.
    
    Input:
        -nom_jugador(str): String que representa el nombre del jugador.
        -casella(str): String con el nombre completo de la casilla del tablero.
        -tauler(list): Lista de diccionarios que contienen la información de las casillas del tablero.
        
    Retorna:
        -jugador_es_propietari(bool): Booleano que informa sobre si el jugador es el propietario de la casilla.'''
    jugador_es_propietari = (propietari_casella(casella, tauler) == nom_jugador)
    return jugador_es_propietari
        
def num_cases(casella:str, tauler:list) -> int:
    '''Retorna el número de casas que hay en una determinada casilla del tablero.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -tauler(list): Lista de diccionarios que contienen la información de cada casilla del tablero.
        
    Retorna:
        -num_cases(int): Integer que representa el número de casas que hay en la casilla.'''
    #Buscamos la casilla en el tablero:
    for dict_casella in tauler:
        if dict_casella["nom_complet"] == casella:
            num_cases = dict_casella["cases"]
            return num_cases
    return 0
        
def num_hotels(casella:str, tauler:list) -> int:
    '''Retorna el número de hoteles que hay en una determinada casilla del tablero.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -tauler(list): Lista de diccionarios que contienen la información de cada casilla del tablero.
        
    Retorna:
        -num_hotels(int): Integer que representa el número de hoteles que hay en la casilla.'''
    #Buscamos la casilla en el tablero:
    for dict_casella in tauler:
        if dict_casella["nom_complet"] == casella:
            num_hotels = dict_casella["hotels"]
            return num_hotels
        
def preu_lloguer_casa(casella:str, preu_caselles:dict) -> int:
    '''Retorna el precio de alquiler de una casa en una determinada casilla.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -preus_caselles(dict): Diccionario que contiene toda la información referente a los precios.
        
    Retorna:
        -preu_lloguer_casa(int): Integer que representa el precio de alquilar una casa en una determinada casilla.'''
    preu_lloguer_casa = preu_caselles[casella]["lloguer_casa"]
    return preu_lloguer_casa

def preu_lloguer_hotel(casella:str, preu_caselles:dict) -> int:
    '''Retorna el precio de alquiler de un hotel en una determinada casilla.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -preus_caselles(dict): Diccionario que contiene toda la información referente a los precios.
        
    Retorna:
        -preu_lloguer_hotel(int): Integer que representa el precio de alquilar un hotel en una determinada casilla.'''
    preu_lloguer_hotel= preu_caselles[casella]["lloguer_hotel"]
    return preu_lloguer_hotel
        
def preu_terreny(nom_casella:str, preu_caselles:dict) -> int:
    '''Retorna el precio de compra de una determinada casilla.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -preus_caselles(dict): Diccionario que contiene toda la información referente a los precios.
        
    Retorna:
        -preu_terreny(int): Integer que representa el precio de una casilla/terreno.'''
    preu_terreny = preu_caselles[nom_casella]["preu_terreny"]
    return preu_terreny

def preu_comprar_casa(casella:str, preu_caselles:dict) -> int:
    '''Retorna el precio de compra de una casa en una determinada casilla.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -preus_caselles(dict): Diccionario que contiene toda la información referente a los precios.
        
    Retorna:
        -preu_casa(int): Integer que representa el precio de una casa en una determinada casilla.'''
    preu_casa = preu_caselles[casella]["comprar_casa"]
    return preu_casa

def preu_comprar_hotel(casella:str, preu_caselles:dict) -> int:
    '''Retorna el precio de compra de un hotel en una determinada casilla.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -preus_caselles(dict): Diccionario que contiene toda la información referente a los precios.
        
    Retorna:
        -preu_hotel(int): Integer que representa el precio de un hotel en una determinada casilla.'''
    preu_hotel = preu_caselles[casella]["comprar_hotel"]
    return preu_hotel

def import_lloguer_casella(casella:str, preu_caselles:dict, tauler:list) -> int:
    '''Retorna el precio total a pagar por estar en la casilla de un jugador, dependiendo de la cantidad de casas y hoteles.
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -preus_caselles(dict): Diccionario que contiene toda la información referente a los precios.
        -tauler(list): Lista de diccionarios que contienen la información de las casillas del tablero.
        
    Retorna:
        -import_casella(int): Integer que representa la cantidad a pagar al jugador propietario por estar en una casilla.'''
    #Buscamos la casilla en el tablero para saber cuántas casas y hoteles hay:
    n_cases = num_cases(casella, tauler)
    preu_lloguer_cases = preu_lloguer_casa(casella, preu_caselles)

    n_hotels = num_hotels(casella, tauler)
    preu_lloguer_hotels = preu_lloguer_hotel(casella, preu_caselles)

    import_casella = (n_cases * preu_lloguer_cases) + (n_hotels * preu_lloguer_hotels)
    return import_casella

def preu_total_casella(casella:str, preus_caselles:dict, tauler:list) -> int:
    '''Retorna el precio total que ha pagado el propietario por una casilla (terreno, casas y hoteles).
    
    Input:
        -casella(str): String con el nombre completo de la casilla del tablero.
        -preus_caselles(dict): Diccionario que contiene toda la información referente a los precios.
        -tauler(list): Lista de diccionarios que contienen la información de las casillas del tablero.
        
    Retorna:
        -preu_total_casella'''
    for dict_casella in tauler:
        if dict_casella["nom_complet"] == casella:
            preu_terreny = preu_terreny(casella, preus_caselles)
            n_cases = num_cases(casella, tauler)
            preu_comprar_cases = preu_comprar_casa(casella, preus_caselles)
            n_hotels = num_hotels(casella, preus_caselles)
            preu_comprar_hotels = preu_comprar_hotel(casella, preus_caselles)

            preu_total_casella = preu_terreny + (n_cases * preu_comprar_cases) + (n_hotels * preu_comprar_hotels)
            return preu_total_casella

def preu_total_propietats(nom_jugador:str, preus_caselles:dict, tauler:list) -> int:
    '''Retorna el precio total que ha pagado el jugador por cada terreno, casa y hotel que posea.
    
    Inputs:
        -nom_jugador(str): String que representa el nombre del jugador.
        -preus_caselles(dict): Diccionario que contiene toda la información referente a los precios.
        -tauler(list): Lista de diccionarios que contienen la información de las casillas del tablero.
        
    Retorna:
        -preu_total_propietats(int): Integer que representa el precio total que ha pagado el jugador
        por cada terreno, casa y hotel que posee.'''
    preu_total_propietats = 0

    for dict_casella in tauler:
        nom_casella = dict_casella["nom_complet"]
        if jugador_es_propietari(nom_jugador, nom_casella, tauler):
            preu_casella_propietats = preu_total_casella(nom_casella, preus_caselles, tauler)
            preu_total_propietats += preu_casella_propietats
    
    return preu_total_propietats

def hi_ha_guanyador(ordre_jugadors:list) -> bool:
    '''Retorna True si sólo queda un jugador en la partida.
    
    Input:
        -ordre_jugadors(list): Lista que contiene los nombres de los jugadores activos en la partida.
        
    Retorna:
        -hi_ha_guanyador(bool): Booleano que informa sobre si la partida tiene un ganador'''
    #Si sólo queda un jugador activo en la partida, debe ser el ganador:
    hi_ha_guanyador = (len(ordre_jugadors) == 1)
    return hi_ha_guanyador

#endregion ConsultarDatos

#region GestioBanca
def afegir_diners_banca(banca):
    '''Añadimos dinero a la banca cuando esta no disponga de suficiente dinero (< 500.000€).
    
    Inputs: No tiene
    
    Retorna: No retorna ningún valor. Modifica el valor de la varialbe "banca"'''
    banca += 500000
    return banca

def retirar_diners_banca(quantitat:int) -> None:
    global banca
    banca -= quantitat

def gestiona_diners_banca(banca:int):
    '''Miramos la cantidad de dinero de la banca, si es menor a 500.000€, llamaremos a afegir_diners_banca()
    
    Input:
        -banca (int): Cantidad de dinero que tiene la banca
        
    Retorna: No retorna nada'''
    if banca < MIN_DINERS_BANCA:
        afegir_diners_banca()
#endregion GestioBanca

#region ImpresionTablero
def imprimeix_separador() -> None:
    '''Imprimimos por pantalla las dos líneas divisorias del tablero (final de la primera y última fila)
        
    Retorna: No retorna nada'''
    amplada = casella_mesures["ampla"]
    print(f"+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+")

def imprimeix_casella_vertical(nom: str, cases: int, hotels: int, jugadors: dict, posicio: list) -> None:
    '''Imprimimos las casillas verticales. Se imprimirán las 2 filas con datos y el separador inferior. En caso de estar encima de la final vertical inferior, sólo se imprimirán las 2 filas con datos
    
    Input:
        -nom (str): Nombre a imprimir de la casilla
        -cases (int): Número de cases en la casilla
        -hotels (int): Número de hoteles en la casilla
        -jugadors (list): Lista con los iconos de los jugadores en la casilla
        -posicio (list): Lista con la posición en X,Y de la casilla
    
    Retorna: No retorna nada'''
    amplada = casella_mesures["ampla"]
    final_linia = "|"
    separador = f"+{"".ljust(amplada, "-")}+"

    string_final = f"{final_linia}"
    if cases > 0:
        amplada -= 1
        final_linia = f"{cases}C"

    string_final += f"{nom.ljust(amplada)}{final_linia}"
    mou_cursor(posicio[1], posicio[0])
    print(string_final)

    amplada = casella_mesures["ampla"]
    final_linia = "|"
    if hotels > 0:
        amplada -= 1
        final_linia = f"{hotels}H"
    string_final = "|"
    if len(jugadors) != 0:
        string_jugadors = ""
        for jugador in jugadors:
            string_jugadors += jugador
        string_final += f"{string_jugadors.ljust(amplada)}"
    else:
        string_final += f"{"".ljust(amplada)}"
    string_final += f"{final_linia}"
    mou_cursor(posicio[1], posicio[0] + 1)
    print(string_final)
    
    if posicio[0] != 17:
        string_final = f"{separador}"
        mou_cursor(posicio[1], posicio[0] + 2)
        print(string_final)

def imprimeix_casella_horizontal(nom: str, cases: int, hotels: int, jugadors: dict, posicio: list) -> None:
    '''Imprimimos las dos filas verticales. Gestionamos si nos encontramos en la fila superior o inferior para cambiar el orden de impresión de los datos.
    
    Input:
        -nom (str): Nombre a imprimir de la casilla
        -cases (int): Número de cases en la casilla
        -hotels (int): Número de hoteles en la casilla
        -jugadors (list): Lista con los iconos de los jugadores en la casilla
        -posicio (list): Lista con la posición en X,Y de la casilla

    Retorna: No retorna nada'''
    primera_linia = "+"
    if cases > 0:
        primera_linia += f"{"".ljust(4, "-")}{cases}C"
    else:
        primera_linia += f"".ljust(6, "-")

    if hotels > 0:
        primera_linia += f"{hotels}H+"
    else:
        primera_linia += f"".ljust(2, "-") + "+"
    
    amplada = casella_mesures["ampla"]
    final_linia = "|"
    if len(jugadors) != 0:
            string_jugadors = ""
            for jugador in jugadors:
                string_jugadors += jugador
            string_jugadors = string_jugadors.ljust(amplada)
    else:
        string_jugadors = "".ljust(amplada)

    if posicio[0] == 19:
        mou_cursor(posicio[1], posicio[0])
        print(primera_linia)

        mou_cursor(posicio[1], posicio[0] + 1)
        print(f"{final_linia}{string_jugadors}{final_linia}")

        mou_cursor(posicio[1], posicio[0] + 2)
        print(f"{final_linia}{nom.ljust(amplada)}{final_linia}")

    elif posicio[0] == 1:
        mou_cursor(posicio[1], posicio[0])
        print(primera_linia)

        mou_cursor(posicio[1], posicio[0] + 1)
        print(f"{final_linia}{nom.ljust(amplada)}{final_linia}")

        mou_cursor(posicio[1], posicio[0] + 2)
        print(f"{final_linia}{string_jugadors}{final_linia}")


def imprimeix_casella(nom, cases, hotels, jugadors, posicio):
    '''Gestionamos si la casilla a imprimir se encuentra en horizontal o vertical
    
    Input:
        -nom (str): Nombre a imprimir de la casilla
        -cases (int): Número de cases en la casilla
        -hotels (int): Número de hoteles en la casilla
        -jugadors (list): Lista con los iconos de los jugadores en la casilla
        -posicio (list): Lista con la posición en X,Y de la casilla
        
    Retorna: No retorna nada'''
    # Imprimimos por pantalla la casilla 
    # Gestionamos:
    #   - Impresión del nombre
    #   - Impresión del número de casas y hoteles
    #   - Impresión de los jugadores en la casilla
    # Miramos si la casilla debe tener la información en horizontal o en vertical
    if posicio[0] != 1 and posicio[0] != 19:
        imprimeix_casella_vertical(nom, cases, hotels, jugadors, posicio)
    else:
        imprimeix_casella_horizontal(nom, cases, hotels, jugadors, posicio)

def imprimeix_fila(fila_caselles: list) -> None:
    '''Recorremos la fila de casillas y vamos imprimiendo cada una de las casillas.
    
    Input:
        -fila_caselles(list): Lista con todas las casillas de una fila del tablero
        
    Retorna: No retorna nada'''
    # Recibimos una fila del tablero.
    # Iteramos por la fila e imprimimos cada una de las casillas de la fila
    for casella in fila_caselles:
            imprimeix_casella(casella["nom_acortat"], casella["cases"], casella["hotels"], casella["jugadors"], casella["posicio"])

def imprimeix_taula(tauler: list) -> None:
    '''Gestionamos la impresión completa del tablero.
        1. Vamos sacando las diferentes filas del tablero y las vamos imprimiendo.
        2. Imprimimos los separadores de las filas horizontales y verticales.
    
    Input:
        -tauler(list): Lista que contiene los diccionarios de las diferentes casillas.
        
    Retorna: No retorna nada'''
    # Imprimimos del tablero, llamando cada de las fila con los separadores
    for index in posicions_caselles_files:
        fila = list(filter(lambda casella: casella["posicio"][0] == index, tauler))
        imprimeix_fila(fila)
    
    mou_cursor(posicions_separadors[0][0], posicions_separadors[0][1])
    imprimeix_separador()
    mou_cursor(posicions_separadors[1][0], posicions_separadors[1][1])
    imprimeix_separador()
#endregion ImpresionTablero

#region ImprimirInformacion
def imprimeix_informacio_banca(banca: int) -> None:
    '''Gestionamos la impresión de la información de la banca
    
    Input:
        -banca(int): Cantidad de dinero que tiene actualmente la banca.
        
    Retorna: No retorna nada'''
    # Imprimimos la información de la banca
    #   Banca:
    #   Diners: 1838734
    mou_cursor(posicions_informacio[0][0], posicions_informacio[0][1])
    print("Banca: ")
    mou_cursor(posicions_informacio[0][0], posicions_informacio[0][1] + 1)
    print(f"Diners: {banca}")

def imprimeix_informacio_jugador(index: int, jugador: dict) -> None:
    '''Gestionamos la impresión de la información de un jugador
    
    Input:
        -index(int): Nos indica qué número de jugador nos está llegando. Utilizado para saber la posición en la que debemos posicionar el cursor e imprimir su información
        -jugador(dict): Diccionario con la información de un jugador.

    Retorna: No retorna nada'''
    # Imprimimos la información de la banca
    #   Jugador Groc:
    #   Carrers: 2834
    #   Diners: 1838734
    #   Especial: (res) "Nombre de las cartas especiales"
    mou_cursor(posicions_informacio[index][0], posicions_informacio[index][1])
    print(f"Jugador {jugador["nom"]}: ")

    mou_cursor(posicions_informacio[index][0], posicions_informacio[index][1] + 1)
    print(f"Carrers: ", end="")
    longitud = len(jugador["propietats"])
    if longitud != 0:
        for index_, propietat in enumerate(jugador["propietats"]):
            print(f"{propietat}", end="")
            if index_ != longitud - 1:
                print(", ", end="")
    else:
        print("(cap)")

    mou_cursor(posicions_informacio[index][0], posicions_informacio[index][1] + 2)
    print(f"Diners: {jugador["diners"]} ")

    mou_cursor(posicions_informacio[index][0], posicions_informacio[index][1] + 3)
    print(f"Especial: ", end="")
    longitud = len(jugador["cartes"])
    if longitud != 0:
        for index_, carta in enumerate(jugador["cartes"]):
            print(f"{carta}", end="")
            if index_ != longitud - 1:
                print(", ", end="")
    else:
        print("(res)")  

def imprimeix_informacio(banca: int, jugadors: dict) -> None:
    '''Gestionamos la impresión de la información a la derecha de tablero
    
    Input:
        -banca(int): Cantidad de dinero de la banca.
        -jugadors(dict): Diccionario con la información de todos los jugadores.

    Retorna: No retorna nada'''
    # Gestiona la impresión a la derecha del tablero
    imprimeix_informacio_banca(banca)

    for index, jugador in enumerate(jugadors.values()):
        imprimeix_informacio_jugador(index + 1, jugador)

def imprimeix_possibles_jugades(str_jugades:str) -> None:
    '''Imprime las posibles jugadas que puede hacer el jugador en su turno.
    
    Input:
        -str_jugades(str): String con el contenido a imprimir.
        
    Retorna: None'''
    mou_cursor(0, 23)
    print(str_jugades)

#endregion ImprimirInformacion

#region ImprimirJugadas
def imprimeix_jugades(accions: list) -> None:
    '''Gestionamos la impresión de las acciones transcurridas durante el juego. El máximo de líneas es 13.
    
    Input:
        -accions(list): Lista de strings con las jugadas a imprimir.

    Retorna: No retorna nada'''
    # Imprimimos en el espacio central del tablero 13 líneas de acciones realizadas por los jugadores
    amplada = tauler_mesures["ampla_total"] - (tauler_mesures["ampla_partida"] * 2)
    posicio_x = posicio_jugades[1]
    posicio_y = posicio_jugades[0]
    text_inici_accio = "Juga"
    simbol_inici_accio = ">"

    if len(accions) > MAX_LINIES_JUGADES:
        min = len(accions) - MAX_LINIES_JUGADES
        accions = accions[min:]
    
    for accio in accions:
        # Recortamos el string en caso que no nos vaya a caber en el espacio establecido
        if len(accio) > amplada:
            min = len(accio) - amplada
            accio = accio[min:]

        # Movemos el cursor a la posición deseada e imprimimos la línea
        # En caso que empecemos turno, deberemos añadir el carácter '>' al inicio
        mou_cursor(posicio_x, posicio_y)
        if text_inici_accio in accio:
            print(f"{simbol_inici_accio} ", end="")
            print(accio.ljust(amplada - 2))
        else:
            print(f"  {accio.ljust(amplada - 2)}")
        
        # Aumentamos en 1 la línea
        posicio_y += 1
#endregion ImprimirJugadas

#region Joc
def afegeix_jugadors_sortida(jugadors: dict, ordre: list, tauler: list) -> None:
    '''Añadimos la posición de la casilla 'Sortida' a los jugadores y añadimos los iconos de los jugadores a la casilla.
    
    Input:
        -jugadors(dict): Diccionarios con la información de todos los jugadores.
        -ordre(list): Lista con el ordre de jugadas de los jugadores. El valor de cada item de la lista es la clave del diccionario de jugadors.
        -tauler(list): Lista que contiene diccionarios con la información de las casillas.

    Retorna: No retorna nada'''
    casella_sortida = list(filter(lambda casella: casella["nom_complet"] == "Sortida", tauler))
    for jugador in ordre:
        jugadors[jugador]["posicio"] = casella_sortida[0]["posicio"]
        casella_sortida[0]["jugadors"].append(jugadors[jugador]["icona"])

def genera_partida() -> tuple:
    '''Gestionamos la generación de una nueva partida.
        1. Generamos el tablero (en caso de volver a jugar, se sobreescribirán los correspondientes datos).
        2. Generamos los jugadores (en caso de volver a jugar, se sobreescribirán los correspondientes datos).
        3. Ordenamos de manera aleatoria los jugadores.
        4. Añadimos dinero a la banca, en caso que sea necesario.
        5. Pagamos a todos los jugadores con 2000€.
        6. Añadimos los jugadores a la casilla de 'Sortida'.
        7. Imprimimos el tablero y la información de la banca y los jugadores.

    Retorna: tupla(tauler(list), jugadors(dict), ordre_jugadors(list))'''
    tauler = genera_tauler(caselles_ordenades, caselles_ordenades_nom_acortat, caselles_especials, caselles_posicions)
    jugadors = genera_jugadors(noms_jugadors)
    ordre_jugadors = ordre_tirada(jugadors)
    preus = genera_preus_caselles(caselles_ordenades, preus_caselles, etiquetes_preus_caselles)
    gestiona_diners_banca(banca)
    primer_pagament(jugadors)
    afegeix_jugadors_sortida(jugadors, ordre_jugadors, tauler)
    imprimeix_per_pantalla(tauler, banca, jugadors, jugades)
    return tauler, jugadors, ordre_jugadors, preus

def mateixa_posicio(posicio_1: list, posicio_2: list) -> bool:
    '''Validamos si una posición es igual a otra

    Input:
        -posicio_1(list): Lista con 2 posiciones con el valor de X,Y
        -posicio_2(list): Lista con 2 posiciones con el valor de X,Y

    Retorna: bool'''
    return posicio_1[0] == posicio_2[0] and posicio_1[1] == posicio_2[1]

def jugador_a_la_preso(tauler:list, jugador: dict) -> bool:
    '''Validamos si un jugador se encuentra en la prisión

    Input:
        -tauler(list): Lista de diccionarios con la información de las casillas.
        -jugador(dict): Diccionario con la información de un jugador.

    Retorna: bool'''
    posicio_jugador = jugador["posicio"]
    posicio_preso = list(map(lambda casella: casella["posicio"], filter(lambda casella: casella["nom_complet"] == "Presó", tauler)))
    
    return jugador["es_preso"] and mateixa_posicio(posicio_jugador, posicio_preso[0])

def actualitzar_jugador_preso(jugador:dict):
    '''Actualizamos el estado del jugador que se encuentra en prisión

    Input:
        -jugador(dict): Diccionario con la información de un jugador.

    Retorna: No retorna nada'''
    jugador["torns_preso"] += 1

    if jugador["torns_preso"] == 3:
        jugador["torns_preso"] = 0
        jugador["es_preso"] = False

def tirar_daus() -> tuple:
    '''Realizamos la tiradas de los datos y realizamos la suma de ellos.

    Retorna: tuple(dau_1(int), dau_2(int), total(int))'''
    dau_1 = random.randint(1, 6)
    dau_2 = random.randint(1, 6)
    total = dau_1 + dau_2

    return dau_1, dau_2, total

def surt_preso_daus(dau_1:int, dau_2:int) -> bool:
    '''Revismos si los dados son del mismo número para así salir de la prisión.

    Input:
        -dau_1(int): Valor del primer dado.
        -dau_2(int): Valor del segundo dado.

    Retorna: bool'''
    return dau_1 == dau_2

def gestiona_caixa_i_sort_afegir_numero(nom_casella: str, posicio_jugador: list) -> str:
    '''Revismos la casilla en la que se encuentra el jugador. Si es 'Sort' o 'Caixa' deberemos añadirle el número correspondiente para poderlo enviar a la posición que le corresponda.

    Input:
        -nom_casella(str): Nom que aparece en terminal de la casilla.
        -posicio_jugador(list): Lista de 2 items con los valores X,Y de la posición del jugador.

    Retorna: str'''
    caselles = list(filter(lambda casella: "Sort" in casella[0] or "Caixa" in casella[0], caselles_posicions))

    for casella in caselles:
        if mateixa_posicio(casella[1], posicio_jugador):
            return casella[0]
    
    return nom_casella

def gestiona_caixa_i_sort_retirar_numero(nom_casella:str) -> tuple:
    '''Revismos la casilla en la que se encuentra el jugador. Si es 'Sort' o 'Caixa' deberemos retirarle el número correspondiente para poderlo enviar a la posición que le corresponda.

    Input:
        -nom_casella(str): Nom que aparece en terminal de la casilla.

    Retorna: tuple(nom_casella(str), posicio(list))'''
    index = caselles_ordenades.index(nom_casella)
    posicio = caselles_posicions[index][1]
    if "Sort" in nom_casella or "Caixa" in nom_casella:
        return re.sub(r'\d+', '', nom_casella), posicio

    return nom_casella, posicio

def actualitza_posicio(tauler: list, jugador: dict, suma_daus: int) -> str:
    '''Actualizamos la posición del jugador en el tablero.

    Input:
        -tauler(list): Lista de diccionarios con la información de las casillas.
        -jugador(dict): Diccionario con la información de un jugador.
        -suma_daus(int): Número de casillas que deberemos avanzar en el tablero.

    Retorna: nom_casllea(srt)'''
    casella = list(map(lambda casella: casella, filter(lambda casella: mateixa_posicio(casella["posicio"], jugador["posicio"]), tauler)))
    nom_casella = gestiona_caixa_i_sort_afegir_numero(casella[0]["nom_complet"], jugador["posicio"])
    index = caselles_ordenades.index(nom_casella)
    casella[0]["jugadors"].remove(jugador["icona"])

    nou_index = (index + suma_daus) % MAX_CASELLES
    nom_casella = caselles_ordenades[nou_index]
    nom_casella, posicio = gestiona_caixa_i_sort_retirar_numero(nom_casella)
    casella = list(map(lambda casella: casella, filter(lambda casella: casella["nom_complet"] == nom_casella and mateixa_posicio(casella["posicio"], posicio), tauler)))
    casella[0]["jugadors"].append(jugador["icona"])
    jugador["posicio"] = posicio

    afegir_jugada(f"\"{jugador["icona"]}\" avança fins \"{nom_casella}\"")

    return nom_casella

def afegir_jugada(accio: str) -> None:
    '''Añadimos la jugada realizada e imprimimos la lista.

    Input:
        -accio(str): String de la jugada realizada que deberemos añadir a la lista.

    Retorna: No retorna nada'''
    jugades.append(accio)
    imprimeix_jugades(jugades)

def gestiona_sort(jugador:dict, tauler:list, ordre:list, jugadors:dict, banca: int) -> None:
    '''Gestionamos la caída de un jugador en una casilla de 'Sort'.
        1. Escogemos una carta al azar de suerte.
        2. Realizamos las acciones correspondientes.

    Input:
        -jugador(dict): Diccionario con toda la información de un jugador.
        -tauler(list): Lista de diccionarios la información de todas las casillas.
        -ordre(list): Lista con el orden de los jugadores en la partida.
        -jugadors(dict): Diccionario con la información de todos los jugadores.
        -banca(int): Candidad de dinero que tiene la banca

    Retorna: No retorna nada'''
    carta = random.choice(cartes_sort)
    afegir_jugada(f"+ Sort: \"{carta}\"")

    if carta == "Sortir presó":
        # Jugador és a la presó
            # SI: Surt de la presó
            # NO: Afegim carta al seu stack
        if jugador_a_la_preso(tauler, jugador):
            jugador["es_preso"] = False
            afegir_jugada(f"\"{jugador["icona"]}\" surt de la presó")
        else:
            jugador["cartes"].append(carta)
            afegir_jugada(f"\"{jugador["icona"]}\" es guarda la carta")
    elif carta == "Anar presó":
        # Si jugador no és a la presó, el portem a la presó
        if not jugador_a_la_preso(tauler, jugador):
            afegir_jugada(f"\"{jugador["icona"]}\" va a la Presó")
            casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
            index_actual = caselles_ordenades.index(casella_actual[0])
            index_preso = caselles_ordenades.index("Presó")
            if index_actual > index_preso:
                tirada = 24 - index_actual + index_preso
                actualitza_posicio(tauler, jugador, tirada)
            else:
                tirada = index_preso - index_actual
                actualitza_posicio(tauler, jugador, tirada)
            jugador["es_preso"] = True
        else:
            afegir_jugada(f"\"{jugador["icona"]}\" es troba a la presó. Carta no té efecte")
    elif carta == "Anar sortida":
        afegir_jugada(f"\"{jugador["icona"]}\" va a la Sortida")
        jugador["diners"] += 200
        afegir_jugada(f"+$ \"{jugador["icona"]}\" rep 200€")
        casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
        index_actual = caselles_ordenades.index(casella_actual[0])
        tirada = 24 - index_actual
        actualitza_posicio(tauler, jugador, tirada)
    elif carta == "Anar 3 espais enrera":
        afegir_jugada(f"\"{jugador["icona"]}\" retrocedeix 3 posicions")
        casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
        index_actual = caselles_ordenades.index(casella_actual[0])
        tirada = - 3
        if index_actual + tirada < 0:
            tirada = 24 - (index_actual + tirada)
        actualitza_posicio(tauler, jugador, tirada)
    elif carta == "Fer reparacions a les propietats":
        cases = sum(list(map(lambda casella: casella["cases"], filter(lambda casella: casella["nom_complet"] in jugador["propietats"], tauler)))) * 25
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cases}€ per les seves cases")
        hotels = sum(list(map(lambda casella: casella["hotels"], filter(lambda casella: casella["nom_complet"] in jugador["propietats"], tauler)))) * 100
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {hotels}€ per les seves cases")
        jugador["diners"] -= (cases + hotels)
    elif carta == "Ets escollit alcalde":
        afegir_jugada(f"+$ \"{jugador["icona"]}\" rep 50€ de cada jugador")
        total = 0
        for nom_jugador in ordre:
            if nom_jugador == jugador["nom"]:
                continue
            total += 50
            jugadors[nom_jugador]["diners"] -= 50
        jugador["diners"] += total
    
    imprimeix_per_pantalla(tauler, banca, jugadors, jugades)

def gestiona_caixa(jugador:dict, tauler:list, jugadors:dict, banca: int) -> None:
    '''Gestionamos la caída de un jugador en una casilla de 'Caixa'.
        1. Escogemos una carta al azar de caixa.
        2. Realizamos las acciones correspondientes.

    Input:
        -jugador(dict): Diccionario con toda la información de un jugador.
        -tauler(list): Lista de diccionarios la información de todas las casillas.
        -jugadors(dict): Diccionario con la información de todos los jugadores.
        -banca(int): Candidad de dinero que tiene la banca

    Retorna: No retorna nada'''
    carta = random.choice(cartes_caixa)
    afegir_jugada(f"+ Sort: \"{carta}\"")

    "Sortir presó",
    "Anar presó",
    "",
    "",
    "Despeses escolars",
    "",
    ""

    if carta == "Sortir presó":
        # Jugador és a la presó
            # SI: Surt de la presó
            # NO: Afegim carta al seu stack
        if jugador_a_la_preso(tauler, jugador):
            jugador["es_preso"] = False
            afegir_jugada(f"\"{jugador["icona"]}\" surt de la presó")
        else:
            jugador["cartes"].append(carta)
            afegir_jugada(f"\"{jugador["icona"]}\" es guarda la carta")
    elif carta == "Anar presó":
        # Si jugador no és a la presó, el portem a la presó
        if not jugador_a_la_preso(tauler, jugador):
            afegir_jugada(f"\"{jugador["icona"]}\" va a la Presó")
            casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
            index_actual = caselles_ordenades.index(casella_actual[0])
            index_preso = caselles_ordenades.index("Presó")
            if index_actual > index_preso:
                tirada = 24 - index_actual + index_preso
                actualitza_posicio(tauler, jugador, tirada)
            else:
                tirada = index_preso - index_actual
                actualitza_posicio(tauler, jugador, tirada)
            jugador["es_preso"] = True
        else:
            afegir_jugada(f"\"{jugador["icona"]}\" es troba a la presó. Carta no té efecte")
    elif carta == "Error de la banca al teu favor":
        cost = 150
        banca -= cost
        jugador["diners"] += cost
        afegir_jugada(f"+$ \"{jugador["icona"]}\" guanya {cost}€")
    elif carta == "Despeses mèdiques":
        cost = 50
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Despeses esacolars":
        cost = 50
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Reparacions al carrer":
        cost = 40
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Concurs de bellesa":
        cost = 10
        banca -= cost
        jugador["diners"] += cost
        afegir_jugada(f"+$ \"{jugador["icona"]}\" guanya {cost}€")
    
    imprimeix_per_pantalla(tauler, banca, jugadors, jugades)

def mateixa_posicio(posicio_1: list, posicio_2: list) -> bool:
    '''Validamos si una posición es igual a otra

    Input:
        -posicio_1(list): Lista con 2 posiciones con el valor de X,Y
        -posicio_2(list): Lista con 2 posiciones con el valor de X,Y

    Retorna: bool'''
    return posicio_1[0] == posicio_2[0] and posicio_1[1] == posicio_2[1]

def jugador_a_la_preso(tauler:list, jugador: dict) -> bool:
    '''Validamos si un jugador se encuentra en la prisión

    Input:
        -tauler(list): Lista de diccionarios con la información de las casillas.
        -jugador(dict): Diccionario con la información de un jugador.

    Retorna: bool'''
    posicio_jugador = jugador["posicio"]
    posicio_preso = list(map(lambda casella: casella["posicio"], filter(lambda casella: casella["nom_complet"] == "Presó", tauler)))
    
    return jugador["es_preso"] and mateixa_posicio(posicio_jugador, posicio_preso[0])

def actualitzar_jugador_preso(jugador:dict):
    '''Actualizamos el estado del jugador que se encuentra en prisión

    Input:
        -jugador(dict): Diccionario con la información de un jugador.

    Retorna: No retorna nada'''
    jugador["torns_preso"] += 1

    if jugador["torns_preso"] == 3:
        jugador["torns_preso"] = 0
        jugador["es_preso"] = False

def tirar_daus() -> tuple:
    '''Realizamos la tiradas de los datos y realizamos la suma de ellos.

    Retorna: tuple(dau_1(int), dau_2(int), total(int))'''
    dau_1 = random.randint(1, 6)
    dau_2 = random.randint(1, 6)
    total = dau_1 + dau_2

    return dau_1, dau_2, total

def surt_preso_daus(dau_1:int, dau_2:int) -> bool:
    '''Revismos si los dados son del mismo número para así salir de la prisión.

    Input:
        -dau_1(int): Valor del primer dado.
        -dau_2(int): Valor del segundo dado.

    Retorna: bool'''
    return dau_1 == dau_2

def gestiona_caixa_i_sort_afegir_numero(nom_casella: str, posicio_jugador: list) -> str:
    '''Revismos la casilla en la que se encuentra el jugador. Si es 'Sort' o 'Caixa' deberemos añadirle el número correspondiente para poderlo enviar a la posición que le corresponda.

    Input:
        -nom_casella(str): Nom que aparece en terminal de la casilla.
        -posicio_jugador(list): Lista de 2 items con los valores X,Y de la posición del jugador.

    Retorna: str'''
    caselles = list(filter(lambda casella: "Sort" in casella[0] or "Caixa" in casella[0], caselles_posicions))

    for casella in caselles:
        if mateixa_posicio(casella[1], posicio_jugador):
            return casella[0]
    
    return nom_casella

def gestiona_caixa_i_sort_retirar_numero(nom_casella:str) -> tuple:
    '''Revismos la casilla en la que se encuentra el jugador. Si es 'Sort' o 'Caixa' deberemos retirarle el número correspondiente para poderlo enviar a la posición que le corresponda.

    Input:
        -nom_casella(str): Nom que aparece en terminal de la casilla.

    Retorna: tuple(nom_casella(str), posicio(list))'''
    index = caselles_ordenades.index(nom_casella)
    posicio = caselles_posicions[index][1]
    if "Sort" in nom_casella or "Caixa" in nom_casella:
        return re.sub(r'\d+', '', nom_casella), posicio

    return nom_casella, posicio

def actualitza_posicio(tauler: list, jugador: dict, suma_daus: int) -> str:
    '''Actualizamos la posición del jugador en el tablero.

    Input:
        -tauler(list): Lista de diccionarios con la información de las casillas.
        -jugador(dict): Diccionario con la información de un jugador.
        -suma_daus(int): Número de casillas que deberemos avanzar en el tablero.

    Retorna: nom_casllea(srt)'''
    casella = list(map(lambda casella: casella, filter(lambda casella: mateixa_posicio(casella["posicio"], jugador["posicio"]), tauler)))
    nom_casella = gestiona_caixa_i_sort_afegir_numero(casella[0]["nom_complet"], jugador["posicio"])
    index = caselles_ordenades.index(nom_casella)
    casella[0]["jugadors"].remove(jugador["icona"])

    nou_index = (index + suma_daus) % MAX_CASELLES
    nom_casella = caselles_ordenades[nou_index]
    nom_casella, posicio = gestiona_caixa_i_sort_retirar_numero(nom_casella)
    casella = list(map(lambda casella: casella, filter(lambda casella: casella["nom_complet"] == nom_casella and mateixa_posicio(casella["posicio"], posicio), tauler)))
    casella[0]["jugadors"].append(jugador["icona"])
    jugador["posicio"] = posicio

    afegir_jugada(f"\"{jugador["icona"]}\" avança fins \"{nom_casella}\"")

    return nom_casella

def gestiona_sort(jugador:dict, tauler:list, ordre:list, jugadors:dict, banca: int) -> None:
    '''Gestionamos la caída de un jugador en una casilla de 'Sort'.
        1. Escogemos una carta al azar de suerte.
        2. Realizamos las acciones correspondientes.

    Input:
        -jugador(dict): Diccionario con toda la información de un jugador.
        -tauler(list): Lista de diccionarios la información de todas las casillas.
        -ordre(list): Lista con el orden de los jugadores en la partida.
        -jugadors(dict): Diccionario con la información de todos los jugadores.
        -banca(int): Candidad de dinero que tiene la banca

    Retorna: No retorna nada'''
    carta = random.choice(cartes_sort)
    afegir_jugada(f"+ Sort: \"{carta}\"")

    if carta == "Sortir presó":
        # Jugador és a la presó
            # SI: Surt de la presó
            # NO: Afegim carta al seu stack
        if jugador_a_la_preso(tauler, jugador):
            jugador["es_preso"] = False
            afegir_jugada(f"\"{jugador["icona"]}\" surt de la presó")
        else:
            jugador["cartes"].append(carta)
            afegir_jugada(f"\"{jugador["icona"]}\" es guarda la carta")
    elif carta == "Anar presó":
        # Si jugador no és a la presó, el portem a la presó
        if not jugador_a_la_preso(tauler, jugador):
            afegir_jugada(f"\"{jugador["icona"]}\" va a la Presó")
            casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
            index_actual = caselles_ordenades.index(casella_actual[0])
            index_preso = caselles_ordenades.index("Presó")
            if index_actual > index_preso:
                tirada = 24 - index_actual + index_preso
                actualitza_posicio(tauler, jugador, tirada)
            else:
                tirada = index_preso - index_actual
                actualitza_posicio(tauler, jugador, tirada)
            jugador["es_preso"] = True
        else:
            afegir_jugada(f"\"{jugador["icona"]}\" es troba a la presó. Carta no té efecte")
    elif carta == "Anar sortida":
        afegir_jugada(f"\"{jugador["icona"]}\" va a la Sortida")
        jugador["diners"] += 200
        afegir_jugada(f"+$ \"{jugador["icona"]}\" rep 200€")
        casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
        index_actual = caselles_ordenades.index(casella_actual[0])
        tirada = 24 - index_actual
        actualitza_posicio(tauler, jugador, tirada)
    elif carta == "Anar 3 espais enrera":
        afegir_jugada(f"\"{jugador["icona"]}\" retrocedeix 3 posicions")
        casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
        index_actual = caselles_ordenades.index(casella_actual[0])
        tirada = - 3
        if index_actual + tirada < 0:
            tirada = 24 - (index_actual + tirada)
        actualitza_posicio(tauler, jugador, tirada)
    elif carta == "Fer reparacions a les propietats":
        cases = sum(list(map(lambda casella: casella["cases"], filter(lambda casella: casella["nom_complet"] in jugador["propietats"], tauler)))) * 25
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cases}€ per les seves cases")
        hotels = sum(list(map(lambda casella: casella["hotels"], filter(lambda casella: casella["nom_complet"] in jugador["propietats"], tauler)))) * 100
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {hotels}€ per les seves cases")
        jugador["diners"] -= (cases + hotels)
    elif carta == "Ets escollit alcalde":
        afegir_jugada(f"+$ \"{jugador["icona"]}\" rep 50€ de cada jugador")
        total = 0
        for nom_jugador in ordre:
            if nom_jugador == jugador["nom"]:
                continue
            total += 50
            jugadors[nom_jugador]["diners"] -= 50
        jugador["diners"] += total
    
    imprimeix_per_pantalla(tauler, banca, jugadors, jugades)

def gestiona_caixa(jugador:dict, tauler:list, jugadors:dict, banca: int) -> None:
    '''Gestionamos la caída de un jugador en una casilla de 'Caixa'.
        1. Escogemos una carta al azar de caixa.
        2. Realizamos las acciones correspondientes.

    Input:
        -jugador(dict): Diccionario con toda la información de un jugador.
        -tauler(list): Lista de diccionarios la información de todas las casillas.
        -jugadors(dict): Diccionario con la información de todos los jugadores.
        -banca(int): Candidad de dinero que tiene la banca

    Retorna: No retorna nada'''
    carta = random.choice(cartes_caixa)
    afegir_jugada(f"+ Sort: \"{carta}\"")

    if carta == "Sortir presó":
        # Jugador és a la presó
            # SI: Surt de la presó
            # NO: Afegim carta al seu stack
        if jugador_a_la_preso(tauler, jugador):
            jugador["es_preso"] = False
            afegir_jugada(f"\"{jugador["icona"]}\" surt de la presó")
        else:
            jugador["cartes"].append(carta)
            afegir_jugada(f"\"{jugador["icona"]}\" es guarda la carta")
    elif carta == "Anar presó":
        # Si jugador no és a la presó, el portem a la presó
        if not jugador_a_la_preso(tauler, jugador):
            afegir_jugada(f"\"{jugador["icona"]}\" va a la Presó")
            casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
            index_actual = caselles_ordenades.index(casella_actual[0])
            index_preso = caselles_ordenades.index("Presó")
            if index_actual > index_preso:
                tirada = 24 - index_actual + index_preso
                actualitza_posicio(tauler, jugador, tirada)
            else:
                tirada = index_preso - index_actual
                actualitza_posicio(tauler, jugador, tirada)
            jugador["es_preso"] = True
        else:
            afegir_jugada(f"\"{jugador["icona"]}\" es troba a la presó. Carta no té efecte")
    elif carta == "Error de la banca al teu favor":
        cost = 150
        banca -= cost
        jugador["diners"] += cost
        afegir_jugada(f"+$ \"{jugador["icona"]}\" guanya {cost}€")
    elif carta == "Despeses mèdiques":
        cost = 50
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Despeses esacolars":
        cost = 50
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Reparacions al carrer":
        cost = 40
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Concurs de bellesa":
        cost = 10
        banca -= cost
        jugador["diners"] += cost
        afegir_jugada(f"+$ \"{jugador["icona"]}\" guanya {cost}€")
    
    imprimeix_per_pantalla(tauler, banca, jugadors, jugades)

def mateixa_posicio(posicio_1: list, posicio_2: list) -> bool:
    '''Validamos si una posición es igual a otra

    Input:
        -posicio_1(list): Lista con 2 posiciones con el valor de X,Y
        -posicio_2(list): Lista con 2 posiciones con el valor de X,Y

    Retorna: bool'''
    return posicio_1[0] == posicio_2[0] and posicio_1[1] == posicio_2[1]

def jugador_a_la_preso(tauler:list, jugador: dict) -> bool:
    '''Validamos si un jugador se encuentra en la prisión

    Input:
        -tauler(list): Lista de diccionarios con la información de las casillas.
        -jugador(dict): Diccionario con la información de un jugador.

    Retorna: bool'''
    posicio_jugador = jugador["posicio"]
    
    return jugador["es_preso"] and mateixa_posicio(posicio_jugador, posicio_preso)

def actualitzar_jugador_preso(jugador:dict):
    '''Actualizamos el estado del jugador que se encuentra en prisión

    Input:
        -jugador(dict): Diccionario con la información de un jugador.

    Retorna: No retorna nada'''
    jugador["torns_preso"] += 1

    if jugador["torns_preso"] == 3:
        jugador["torns_preso"] = 0
        jugador["es_preso"] = False

def tirar_daus() -> tuple:
    '''Realizamos la tiradas de los datos y realizamos la suma de ellos.

    Retorna: tuple(dau_1(int), dau_2(int), total(int))'''
    dau_1 = random.randint(1, 6)
    dau_2 = random.randint(1, 6)
    total = dau_1 + dau_2

    return dau_1, dau_2, total

def surt_preso_daus(dau_1:int, dau_2:int) -> bool:
    '''Revismos si los dados son del mismo número para así salir de la prisión.

    Input:
        -dau_1(int): Valor del primer dado.
        -dau_2(int): Valor del segundo dado.

    Retorna: bool'''
    return dau_1 == dau_2

def gestiona_caixa_i_sort_afegir_numero(nom_casella: str, posicio_jugador: list) -> str:
    '''Revismos la casilla en la que se encuentra el jugador. Si es 'Sort' o 'Caixa' deberemos añadirle el número correspondiente para poderlo enviar a la posición que le corresponda.

    Input:
        -nom_casella(str): Nom que aparece en terminal de la casilla.
        -posicio_jugador(list): Lista de 2 items con los valores X,Y de la posición del jugador.

    Retorna: str'''
    caselles = list(filter(lambda casella: "Sort" in casella[0] or "Caixa" in casella[0], caselles_posicions))

    for casella in caselles:
        if mateixa_posicio(casella[1], posicio_jugador):
            return casella[0]
    
    return nom_casella

def gestiona_caixa_i_sort_retirar_numero(nom_casella:str) -> tuple:
    '''Revismos la casilla en la que se encuentra el jugador. Si es 'Sort' o 'Caixa' deberemos retirarle el número correspondiente para poderlo enviar a la posición que le corresponda.

    Input:
        -nom_casella(str): Nom que aparece en terminal de la casilla.

    Retorna: tuple(nom_casella(str), posicio(list))'''
    index = caselles_ordenades.index(nom_casella)
    posicio = caselles_posicions[index][1]
    if "Sort" in nom_casella or "Caixa" in nom_casella:
        return re.sub(r'\d+', '', nom_casella), posicio

    return nom_casella, posicio

def actualitza_posicio(tauler: list, jugador: dict, suma_daus: int) -> tuple:
    '''Actualizamos la posición del jugador en el tablero.

    Input:
        -tauler(list): Lista de diccionarios con la información de las casillas.
        -jugador(dict): Diccionario con la información de un jugador.
        -suma_daus(int): Número de casillas que deberemos avanzar en el tablero.

    Retorna: nom_casllea(srt)'''
    casella = list(map(lambda casella: casella, filter(lambda casella: mateixa_posicio(casella["posicio"], jugador["posicio"]), tauler)))
    nom_casella = gestiona_caixa_i_sort_afegir_numero(casella[0]["nom_complet"], jugador["posicio"])
    index = caselles_ordenades.index(nom_casella)
    casella[0]["jugadors"].remove(jugador["icona"])

    nou_index = (index + suma_daus) % MAX_CASELLES
    nom_casella = caselles_ordenades[nou_index]
    nom_casella, posicio = gestiona_caixa_i_sort_retirar_numero(nom_casella)
    casella = list(map(lambda casella: casella, filter(lambda casella: casella["nom_complet"] == nom_casella and mateixa_posicio(casella["posicio"], posicio), tauler)))
    casella[0]["jugadors"].append(jugador["icona"])
    jugador["posicio"] = posicio

    afegir_jugada(f"\"{jugador["icona"]}\" avança fins \"{nom_casella}\"")

    return (nou_index < index, nom_casella)

def gestiona_sort(jugador:dict, tauler:list, ordre:list, jugadors:dict, banca: int) -> None:
    '''Gestionamos la caída de un jugador en una casilla de 'Sort'.
        1. Escogemos una carta al azar de suerte.
        2. Realizamos las acciones correspondientes.

    Input:
        -jugador(dict): Diccionario con toda la información de un jugador.
        -tauler(list): Lista de diccionarios la información de todas las casillas.
        -ordre(list): Lista con el orden de los jugadores en la partida.
        -jugadors(dict): Diccionario con la información de todos los jugadores.
        -banca(int): Candidad de dinero que tiene la banca

    Retorna: No retorna nada'''
    carta = random.choice(cartes_sort)
    afegir_jugada(f"+ Sort: \"{carta}\"")

    if carta == "Sortir presó":
        jugador["cartes"].append(carta)
        afegir_jugada(f"\"{jugador["icona"]}\" es guarda la carta")
    elif carta == "Anar presó":
        # Si jugador no és a la presó, el portem a la presó
        enviar_jugador_preso(jugador, jugadors, tauler)
    elif carta == "Anar sortida":
        afegir_jugada(f"\"{jugador["icona"]}\" va a la Sortida")
        jugador["diners"] += 200
        afegir_jugada(f"+$ \"{jugador["icona"]}\" rep 200€")
        casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
        index_actual = caselles_ordenades.index(casella_actual[0])
        tirada = 24 - index_actual
        actualitza_posicio(tauler, jugador, tirada)
    elif carta == "Anar 3 espais enrera":
        afegir_jugada(f"\"{jugador["icona"]}\" retrocedeix 3 posicions")
        casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador["posicio"], caselles_posicions)))
        index_actual = caselles_ordenades.index(casella_actual[0])
        tirada = - 3
        if index_actual + tirada < 0:
            tirada = 24 - (index_actual + tirada)
        actualitza_posicio(tauler, jugador, tirada)
    elif carta == "Fer reparacions a les propietats":
        cases = sum(list(map(lambda casella: casella["cases"], filter(lambda casella: casella["nom_complet"] in jugador["propietats"], tauler)))) * 25
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cases}€ per les seves cases")
        hotels = sum(list(map(lambda casella: casella["hotels"], filter(lambda casella: casella["nom_complet"] in jugador["propietats"], tauler)))) * 100
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {hotels}€ per les seves cases")
        jugador["diners"] -= (cases + hotels)
    elif carta == "Ets escollit alcalde":
        afegir_jugada(f"+$ \"{jugador["icona"]}\" rep 50€ de cada jugador")
        total = 0
        for nom_jugador in ordre:
            if nom_jugador == jugador["nom"]:
                continue
            total += 50
            jugadors[nom_jugador]["diners"] -= 50
        jugador["diners"] += total
    
    imprimeix_per_pantalla(tauler, banca, jugadors, jugades)

def gestiona_caixa(jugador:dict, tauler:list, jugadors:dict, banca: int) -> None:
    '''Gestionamos la caída de un jugador en una casilla de 'Caixa'.
        1. Escogemos una carta al azar de caixa.
        2. Realizamos las acciones correspondientes.

    Input:
        -jugador(dict): Diccionario con toda la información de un jugador.
        -tauler(list): Lista de diccionarios la información de todas las casillas.
        -jugadors(dict): Diccionario con la información de todos los jugadores.
        -banca(int): Candidad de dinero que tiene la banca

    Retorna: No retorna nada'''
    carta = random.choice(cartes_caixa)
    afegir_jugada(f"+ Sort: \"{carta}\"")

    if carta == "Sortir presó":
        jugador["cartes"].append(carta)
        afegir_jugada(f"\"{jugador["icona"]}\" es guarda la carta")
    elif carta == "Anar presó":
        # Si jugador no és a la presó, el portem a la presó
        afegir_jugada(f"\"{jugador["icona"]}\" va a la Presó")
        enviar_jugador_preso(jugador, jugadors, tauler)
    elif carta == "Error de la banca al teu favor":
        cost = 150
        banca -= cost
        jugador["diners"] += cost
        afegir_jugada(f"+$ \"{jugador["icona"]}\" guanya {cost}€")
    elif carta == "Despeses mèdiques":
        cost = 50
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Despeses esacolars":
        cost = 50
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Reparacions al carrer":
        cost = 40
        banca += cost
        jugador["diners"] -= cost
        afegir_jugada(f"-$ \"{jugador["icona"]}\" paga {cost}€")
    elif carta == "Concurs de bellesa":
        cost = 10
        banca -= cost
        jugador["diners"] += cost
        afegir_jugada(f"+$ \"{jugador["icona"]}\" guanya {cost}€")
    
    imprimeix_per_pantalla(tauler, banca, jugadors, jugades)

def jugador_perd(jugador_actual:dict, jugadors:dict) -> bool:
    '''Comprueba si un jugador ha perdido la partida (tiene <= 0 en dinero), y devuelve
    un booleano en función de esta comprobación.
    
    Input:
        -jugador_actual(dict): Diccionario que contiene la información del jugador que está realizando el turno.
        -jugadors(dict): Diccionario de diccionarios que contiene la información de todos los jugadores de la partida.
        
    Retorna:
        -ha_perdut(bool): Variable que confirma o no si el jugador ha perdido la partida.'''
    nom_jugador = jugador_actual["nom"]
    diners_jugador = jugadors[nom_jugador]["diners"]
    ha_perdut = (diners_jugador <= 0)
    return ha_perdut

def borrar_jugador_partida(ordre_jugadors:list, jugador_actual:dict) -> list:
    '''Retorna la lista actualizada de jugadores que siguen en la partida, eliminando de la lista previa
    al jugador actual.
    
    Input:
        -ordre_jugadors(list): Lista de jugadores que participan en la partida.
        -jugador_actual(dict): Diccionario con información del jugador actual de la partida.
        
    Retorna: None'''
    nom_jugador = jugador_actual["nom"]
    ordre_jugadors.remove(nom_jugador)

def enviar_jugador_preso(jugador_actual:dict, jugadors:dict, tauler:list) -> None:
    '''Modifica los valores de posicion de 'tauler' y 'jugadors' poniendo el jugador en la prision,
    y cambia el valor de la clave 'es_preso' de 'jugadors' como 'True'.
    
    Input:
        -jugador_actual(dict): Diccionario que contiene la información del jugador que está realizando el turno.
        -jugadors(dict): Diccionario de diccionarios que contiene la información de todos los jugadores de la partida.
        -tauler(list): Lista de diccionarios, donde cada diccionario contiene la información 
        de una casilla (nombre, nombreAcortado, numCasas, numHoteles, jugadores, posicionCasilla).
        
    Retorna: None'''
    casella_actual = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador_actual["posicio"], caselles_posicions)))

    if casella_actual[0] != "Presó":
        index_actual = caselles_ordenades.index(casella_actual[0])
        index_preso = caselles_ordenades.index("Presó")
        if index_actual > index_preso:
            tirada = 24 - index_actual + index_preso
            actualitza_posicio(tauler, jugador_actual, tirada)
        else:
            tirada = index_preso - index_actual
            actualitza_posicio(tauler, jugador_actual, tirada)
    jugador_actual["es_preso"] = True
    jugador_actual["torns_preso"] = 0

    #Si el jugador tiene una carta para salir de la prisión, cambiamos su estado 'es_preso' a 'False' y retiramos la carta:
    if "Sortir de la presó" in jugador_actual["cartes"]:
        jugador_actual["es_preso"] = False
        jugador_actual["cartes"].remove("Sortir de la presó")
        afegir_jugada(f"\"{jugador_actual["icona"]}\" surt de la presó amb carta")

def calcula_possibles_jugades(jugador_actual, jugadors, tauler, preus_caselles, ordre_jugadors) -> list:
    '''Retorna una lista de strings que representan cada una de las posibles jugadas que puede
    realizar el jugador actual.
    
    Input:
        -jugador_actual(dict): Diccionario que contiene la información sobre el jugador actual
        -jugadors(dict): Diccionario de diccionarios que contiene la información de todos los jugadores (inluido el actual)
        -tauler(list): Lista de diccionarios que contienen la información de las casillas del tablero.
        -ordre_jugadors(list): Lista de los jugadores que están participando en la partida
        
    Retorna:
        -possibles_jugades(list): Lista de strings que representan cada una de las posibles jugadas
        que puede realizar el jugador durante su turno.'''
    nom_jugador = jugador_actual["nom"]
    casella_jugador = list(map(lambda casella: casella[0], filter(lambda casella: casella[1] == jugador_actual["posicio"], caselles_posicions)))
    diners_jugador = jugador_actual["diners"]

    #Iniciamos la variable resultante con la opción "passar" incluida, que siempre estará disponible:
    possibles_jugades = ["passar"]

    #Si el jugador puede comprar un terreno:
    if len(casella_jugador) != 0:
        terreny_lliure = (propietari_casella(casella_jugador[0], tauler) == "banca")
        pot_pagar_terreny = (diners_jugador > preu_terreny(casella_jugador[0], preus_caselles))
        casella_no_es_especial = casella_jugador[0] not in caselles_especials
        if terreny_lliure and pot_pagar_terreny and casella_no_es_especial:
            possibles_jugades.append("comprar terreny")

    #Si el jugador puede comprar una casa:
    jugador_es_propietari = (propietari_casella(casella_jugador[0], tauler) == nom_jugador)
    menys_de_4_cases = (num_cases(casella_jugador[0], tauler) < 4)
    pot_pagar_casa = (diners_jugador > preu_comprar_casa(casella_jugador[0], preus_caselles))
    
    if jugador_es_propietari and menys_de_4_cases and pot_pagar_casa:
        possibles_jugades.append("comprar casa")

    #Si el jugador puede comprar un hotel:
    jugador_es_propietari = (propietari_casella(casella_jugador[0], tauler) == nom_jugador)
    minim_2_cases = (num_cases(casella_jugador[0], tauler) >= 2)
    pot_pagar_hotel = (diners_jugador > preu_comprar_hotel(casella_jugador[0], preus_caselles))
    if jugador_es_propietari and minim_2_cases and pot_pagar_hotel:
        possibles_jugades.append("comprar hotel")

    #Si el jugador es propietario de la casilla (y quiere consultar precios):
    jugador_es_propietari = (propietari_casella(casella_jugador[0], tauler) == nom_jugador)

    if jugador_es_propietari:
        possibles_jugades.append("preus")

    #Si el jugador no puede pagar el importe de estar en la casilla:
    no_pot_pagar = (diners_jugador < import_lloguer_casella(casella_jugador[0], preus_caselles, tauler)) and (propietari_casella(casella_jugador[0], tauler) != nom_jugador)

    if no_pot_pagar:
        possibles_jugades.append("preu banc")
        possibles_jugades.append("preu jugador")
        possibles_jugades.append("vendre al banc")

        #Comprobamos si podemos vender a algún otro jugador:
        for potencial_comprador in ordre_jugadors:
            jugador_iterat_no_es_el_actual = (nom_jugador != potencial_comprador)
            if jugador_iterat_no_es_el_actual:
                diners_potencial_comprador = jugadors[potencial_comprador]["diners"]
                #El potencial comprador ha de poder pagar el 90% del precio de las propiedades del jugador:
                pot_pagar = (diners_potencial_comprador > (preu_total_propietats(nom_jugador, preus_caselles, tauler) * 0.9))
                if pot_pagar:
                    possibles_jugades.append(f"vendre a {potencial_comprador[0]}")
    return possibles_jugades

def str_possibles_jugades(jugador:dict, possibles_jugades:list) -> str:
    '''Retorna el string que se utilizará para imprimir las posibles opciones que
    puede realizar el jugador en su turno.
    
    Input:
        -jugador(dict): Diccionario que contiene la información del jugador actual.
        -possibles_jugades(list): Lista que contiene strings con todas las opciones que puede ejecutar el jugador.
        
    Retorna:
        -str_jugades(str): String que contiene información de quién juega y qué jugadas puede hacer.'''
    icona_jugador = jugador["icona"]
    qui_juga = f"Juga \"{icona_jugador}\", opcions: "

    jugades_possibles = ""
    for jugada in possibles_jugades:
        jugades_possibles += f"{jugada}, "
    
    #En 'jugades_possibles', indexamos [:-2] para omitir el final del string ", ":
    str_jugades = qui_juga + jugades_possibles[:-2]
    return str_jugades

def input_jugador(jugador_actual:dict, possibles_jugades:list, jugadors:dict, tauler:list) -> None:
    '''Recibe el input del usuario y lo procesa, dependiendo de las acciones que pueda realizar en su turno.
    
    Inputs:
        -jugador_actual(dict): Diccionario que contiene la información sobre el jugador actual
        -possibles_jugades(list): Lista de strings con cada una de las opciones que puede realizar el usuario.
        -jugadors(dict): Diccionario de diccionarios que contiene la información de todos los jugadores (inluido el actual)
        -tauler(list): Lista de diccionarios que contienen la información de las casillas del tablero.
        
    Retorna: None'''
    #Pedimus un input hasta que este sea válido:
    while True:
        jugada_escollida = input("Escull una opció del llistat: ")
        #Si el input se corresponde con alguna de las posibles jugadas, declaramos el input como válido:
        input_invalid = True
        for jugada in possibles_jugades:
            if jugada_escollida.lower() == jugada:
                input_invalid = False
                jugada_escollida = jugada
        #Si no hemos declarado el input como válido, este permanece inválido, y volvemos a pedir un input:
        if input_invalid:
            print("Opció invàlida, torneu a provar.")
            continue
        break
    return jugada_escollida

def cambiar_propietari(nom_casella:str, nou_propietari:str, tauler:list) -> None:
    '''Modifica la clave 'propietari' dentro de 'tauler' para asignarle el nuevo propietario.
    
    Input:
        -nom_casella(str): String que representa el nombre de la casilla que cambiará de propietario.
        -nou_propietari(str): String que representa el nombre del nuevo propietario de la casilla.
        -tauler(list): Lista de diccionarios que contiene la información de todas las casillas del tablero.
        
    Retorna: None'''
    for dict_casella in tauler:
        if dict_casella["nom_complet"] == nom_casella:
            dict_casella["propietari"] = nou_propietari
            break

def traspassar_totes_les_propietats(nom_anterior_propietari:str, nom_nou_propietari:str, tauler:list) -> None:
    '''Modifica la clave 'propietari' dentro de todas las casillas del tablero que fueran del anterior propietario, 
    para que ahora pertenezcan al nuevo propietario.
    
    Input:
        -nom_anterior_propietari(str): String que representa el nombre del jugador que posee las propiedades, y va a entregarlas a uno nuevo.
        -nom_nou_propietari(str): String que representa el nombre del jugador que va a adquirir las propiedades.
        -tauler(list): Lista de diccionarios que contiene la información de todas las casillas del tablero.
    
    Retorna: None'''
    for dict_casella in tauler:
        nom_casella = dict_casella["nom_complet"]
        if propietari_casella(nom_casella, tauler) == nom_anterior_propietari:
            cambiar_propietari(nom_casella, nom_nou_propietari, tauler)

def jugador_compra_terreny(nom_jugador:str, nom_casella:str, preus:dict, jugadors:dict, tauler:list) -> None:
    '''Modifica los valores necesarios en 'jugadors' y 'tauler' para reconocer la compra de un terreno
    por parte de un jugador.
    
    Input:
        -nom_jugador(str): String que representa el nombre del jugador que va a comprar el terreno.
        -nom_casella(str): String que representa el nombre de la casilla que se quiere adquirir.
        -preus(dict): Diccionario que contiene información sobre los precios de todas las casillas del tablero.
        -jugadors(dict): Diccionario que contiene la información de todos los jugadores.
        -tauler(list): Lista de diccionarios que contiene la información de todas las casillas del tablero.
        
    Retorna: None'''
    preu_comprar_terreny = preu_terreny(nom_casella, preus)

    #Retiramos dinero de la compra al jugador:
    jugadors[nom_jugador]["diners"] -= preu_comprar_terreny
    #Añadimos el terreno a la lista de propiedades del jugador:
    jugadors[nom_jugador]["propietats"].append(nom_casella)
    #Hacemos que el jugador sea propietario de la casilla en el tablero:
    cambiar_propietari(nom_casella, nom_jugador, tauler)

def afegir_cases(nom_casella:str, num_cases:int, tauler:list) -> None:
    '''Añade un número de casas a una casilla del tablero.
    
    Inputs:
        -nom_casella(str): String que representa el nombre de la casilla en la que se añadira el número de casas.
        -num_cases(int): Integer que representa el número de casas a añadir.
        -tauler(list): Lista de diccionarios que contiene toda la información necesaria de todas las casillas del tablero.
        
    Retorna: None'''
    for dict_casella in tauler:
        if dict_casella["nom_complet"] == nom_casella:
            dict_casella["cases"] += num_cases
            break

def retirar_cases(nom_casella:str, num_cases:int, tauler:list) -> None:
    '''Retira un número de casas a una casilla del tablero.
    
    Inputs:
        -nom_casella(str): String que representa el nombre de la casilla en la que se eliminará el número de casas.
        -num_cases(int): Integer que representa el número de casas a quitar.
        -tauler(list): Lista de diccionarios que contiene toda la información necesaria de todas las casillas del tablero.
        
    Retorna: None'''
    for dict_casella in tauler:
        if dict_casella["nom_complet"] == nom_casella:
            dict_casella["cases"] -= num_cases
            break

def jugador_compra_casa(nom_jugador:str, nom_casella:str, preus:dict, jugadors:dict, tauler:list) -> None:
    '''Modifica los valores necesarios en 'jugadors' y 'tauler' para reconocer la compra de una casa
    por parte de un jugador.
    
    Input:
        -nom_jugador(str): String que representa el nombre del jugador que va a comprar la casa.
        -nom_casella(str): String que representa el nombre de la casilla en la que se quiere adquirir una casa.
        -preus(dict): Diccionario que contiene información sobre los precios de todas las casillas del tablero.
        -jugadors(dict): Diccionario que contiene la información de todos los jugadores.
        -tauler(list): Lista de diccionarios que contiene la información de todas las casillas del tablero.
        
    Retorna: None'''
    preu_compra_casa = preu_comprar_casa(nom_casella, preus)

    #Retiramos dinero de la compra al jugador:
    jugadors[nom_jugador]["diners"] -= preu_compra_casa
    #HAñadimos una casa a la casilla en el tablero:
    afegir_cases(nom_casella, 1, tauler)

def afegir_hotels(nom_casella:str, num_hotels:int, tauler:list) -> None:
    '''Añade un número de choteles a una casilla del tablero.
    
    Inputs:
        -nom_casella(str): String que representa el nombre de la casilla en la que se añadira el número de hoteles.
        -num_cases(int): Integer que representa el número de hoteles a añadir.
        -tauler(list): Lista de diccionarios que contiene toda la información necesaria de todas las casillas del tablero.
        
    Retorna: None'''
    for dict_casella in tauler:
        if dict_casella["nom_complet"] == nom_casella:
            dict_casella["hotels"] += num_hotels
            break

def jugador_compra_hotel(nom_jugador:str, nom_casella:str, preus:dict, jugadors:dict, tauler:list) -> None:
    '''Modifica los valores necesarios en 'jugadors' y 'tauler' para reconocer la compra de un hotel
    por parte de un jugador.
    
    Input:
        -nom_jugador(str): String que representa el nombre del jugador que va a comprar el hotel.
        -nom_casella(str): String que representa el nombre de la casilla en la que se quiere adquirir un hotel.
        -preus(dict): Diccionario que contiene información sobre los precios de todas las casillas del tablero.
        -jugadors(dict): Diccionario que contiene la información de todos los jugadores.
        -tauler(list): Lista de diccionarios que contiene la información de todas las casillas del tablero.
        
    Retorna: None'''
    preu_compra_hotel = preu_comprar_hotel(nom_casella, preus)

    #Retiramos dinero de la compra al jugador:
    jugadors[nom_jugador]["diners"] -= preu_compra_hotel
    #Añadimos un hotel a la casilla del tablero:
    afegir_hotels(nom_casella, 1, tauler)
    #Retiramos 2 casas en la casilla de compra del hotel:
    retirar_cases(nom_casella, 2, tauler)

def jugador_actual_ven_tot_al_banc(nom_jugador:str, preus:dict, jugadors:dict, tauler:list) -> None:
    '''Realiza un transpaso de todas las propiedades del jugador actual a la banca, otorgando al 
    jugador actual el 50% del dinero que pagó por dichas propiedades.
    
    Input:
        -nom_jugador_vendedor(str): String que representa el nombre del jugador que va a vender todas sus propiedades.
        -preus(dict): Diccionario que contiene información sobre los precios de todas las casillas del tablero.
        -jugadors(dict): Diccionario que contiene la información de todos los jugadores.
        -tauler(list): Lista de diccionarios que contiene la información de todas las casillas del tablero.
        
    Retorna: None'''
    #Calculamos el precio que se ingresará/retirará, será el 50% del que pagó el jugador:
    preu_per_total_propietats = (preu_total_propietats(nom_jugador, preus, tauler) * 0.5)
    #Ingresamos el dinero al jugador:
    jugadors[nom_jugador]["diners"] += preu_per_total_propietats
    #Retiramos el dinero a la banca:
    retirar_diners_banca(preu_per_total_propietats)
    #Realizamos el traspase de propiedades entre jugador y banca:
    traspassar_totes_les_propietats(nom_jugador, 'banca', tauler)

def jugador_actual_vend_tot_a_altre_jugador(nom_jugador_vendedor:str, nom_jugador_comprador:str, preus:dict, jugadors:dict, tauler:list) -> None:
    '''Realiza un transpaso de todas las propiedades del jugador actual al jugador 'B', otorgando al 
    jugador actual el 90% del dinero que pagó por dichas propiedades.
    
    Input:
        -nom_jugador_vendedor(str): String que representa el nombre del jugador que va a vender todas sus propiedades.
        -nom_jugador_comprador(str): String que representa el nombre del jugador que va a comprar las propiedades del vendedor.
        -preus(dict): Diccionario que contiene información sobre los precios de todas las casillas del tablero.
        -jugadors(dict): Diccionario que contiene la información de todos los jugadores.
        -tauler(list): Lista de diccionarios que contiene la información de todas las casillas del tablero.
        
    Retorna: None'''
    #Calculamos el precio que se ingresará/retirará, será el 90% del que pagó el vendedor:
    preu_per_total_propietats = (preu_total_propietats(nom_jugador_vendedor, preus, tauler) * 0.9)
    #Ingresamos el dinero al vendedor:
    jugadors[nom_jugador_vendedor]["diners"] += preu_per_total_propietats
    #Retiramos el dinero al comprador:
    jugadors[nom_jugador_comprador]["diners"] -= preu_per_total_propietats
    #Realizamos el traspase de propiedades entre vendedor y comprador:
    traspassar_totes_les_propietats(nom_jugador_vendedor, nom_jugador_comprador, tauler)

def main():
    # Generar la partida
    #   - Generamos el tablero
    #       · Generamos las casillas y las metemos en el tablero
    #   - Determinamos el orden de los jugadores
    #   - Generamos los jugadores con los datos iniciales
    #       · Les damos el primer ingreso
    #   - Añandimos a la casilla 'Salida' todos los jugadores

    # Iniciar bucle de juego:
    tauler, jugadors, ordre_jugadors, preus = genera_partida()

    contador_jugador = 0    

    '''
    Contador que sirve para marcar el índice a mirar dentro de la lista de jugadores dentro del bucle

    Utilizamos esta solución porque la otra opción para recorrer la lista de jugadores sería hacer un bucle 'for' (dentro del bucle 'while True')
    y esto nos causarñia problemas cuando queramos modificar la lista de jugadores (a la vez que se realiza el bucle 'for'), como por ejemplo
    cuando eliminemos un jugador de la lista que ha perdido la partida.
    '''

    while True:

        #Miramos al principio de cada jugada si el contador rebasa la lista de jugadores. Si es así, se reinicia a 0.
        if contador_jugador >= len(ordre_jugadors):
            contador_jugador = 0

        # Recogemos la información del jugador actual
        jugador_actual = jugadors[ordre_jugadors[contador_jugador]]
        nom_jugador = jugador_actual["nom"]

    #   - Tiramos dados del jugador
        if jugador_actual["es_preso"] and jugador_actual["torns_preso"] <= 2: #devuelve un booleano diciendo si el jugador está en la prisión
            # Lanzamos los dados del jugador. En caso que no se haya sacado un doble dígito (2, 2) o (4, 4), el jugador continuará en la cárcel
            dau_1, dau_2, total = tirar_daus()
            surt_preso = surt_preso_daus(dau_1, dau_2)

            if not surt_preso:
                #actualitzar_jugador_preso(jugador_actual) #actualiza el contador de turnos que lleva el jugador en la prision. Si el contador == 3, pone el contador a 0 y cambia la variable 'es_preso' a False
                afegir_jugada(f"Juga \"{jugador_actual["icona"]}\", {dau_1} i {dau_2}. Continua a presó")
                jugador_actual["torns_preso"] += 1
                clearScreen()
                imprimeix_per_pantalla(tauler, banca, jugadors, jugades)
                time.sleep(2)
                contador_jugador += 1
                continue #pasamos al siguiente jugador
            else:
                jugador_actual["torns_preso"] = 3
                jugador_actual["es_preso"] = False
                #actualitzar_jugador_preso(jugador_actual)
        else:   
            dau_1, dau_2, total = tirar_daus() #Se retornan una tupla con los valores de los 2 dados y el valor sumado de ellos

        
        #   - Añadimos jugada a la lista de jugadas (para poder imprimirla)
            afegir_jugada(f"Juga \"{jugador_actual["icona"]}\", ha sortit {dau_1} i {dau_2}")
            #   - Actualizamos posición en tablero (borramos actual y ponemos la nueva, tanto en jugador como en casilla)
            ha_passat_sortida, nom_casella = actualitza_posicio(tauler, jugador_actual, total)

            if ha_passat_sortida and nom_casella != "Sortida":
                jugador_actual["diners"] += 200
                afegir_jugada(f"+$ \"{jugador_actual["icona"]}\" guanya 200€ al passar per \"Sortida\"")
        
        imprimeix_per_pantalla(tauler, banca, jugadors, jugades)
        time.sleep(2)
            
#   - Revisamos qué opciones tiene el usuario según la casilla en la que se encuentra
        if nom_casella in caselles_especials:
        
            if nom_casella == "Parking": #en esta casilla, el jugador sólo puede pasar
                clearScreen()
                imprimeix_per_pantalla(tauler, banca, jugadors, jugades)
                time.sleep(1)
                contador_jugador += 1
                continue

            elif nom_casella == "Anr pró":
                enviar_jugador_preso(jugador_actual, jugadors, tauler)
                contador_jugador += 1
                continue

            elif nom_casella == "Sortida":
                #Añadimos 200€ al jugador:
                nom_jugador = jugador_actual["nom"]
                jugadors[nom_jugador]["diners"] += 200
                afegir_jugada(f"+$ \"{jugador_actual["icona"]}\" guanya 200€ al passar per \"Sortida\"")

                #Actualizamos la impresión por pantalla y damos 1 segundo para que el usuario vea que ha ocurrido:
                clearScreen()
                imprimeix_per_pantalla(tauler, banca, jugadors, jugades)
                time.sleep(1)
                contador_jugador += 1
                continue

            elif nom_casella == "Presó":
                enviar_jugador_preso(jugador_actual, jugadors, tauler)
                contador_jugador += 1
                continue

            elif nom_casella == "Sort":
                gestiona_sort(jugador_actual, tauler, ordre_jugadors, jugadors, banca)
                time.sleep(1)
                contador_jugador += 1
                continue

            elif nom_casella == "Caixa":
                gestiona_caixa(jugador_actual, tauler, jugadors, banca)
                time.sleep(1)
                contador_jugador += 1
                continue
            
        else:
            contador_jugador += 1

            #Determinamos qué jugadas puede realizar el jugador (retorna lista de 'str' de jugadas):
            possibles_jugades = calcula_possibles_jugades(jugador_actual, jugadors, tauler, preus, ordre_jugadors)
            str_jugades = str_possibles_jugades(jugador_actual, possibles_jugades)

            #Demandamos el input del usuario (pedirlo hasta que la jugada sea válida) y gestionamos la realización del mismo:
            while True:
                #Actualizamos la información del juego:
                imprimeix_per_pantalla(tauler, banca, jugadors, jugades)
                #Imprimimos las posibles jugadas que puede hacer el jugador:
                imprimeix_possibles_jugades(str_jugades)

                jugada_escollida = input_jugador(jugador_actual, possibles_jugades, jugadors, tauler)

                if jugada_escollida == "truc":
                #Gestionar Trucos
                    pass

                if jugada_escollida == 'passar':
                    pass
                elif jugada_escollida == 'comprar terreny':
                    jugador_compra_terreny(nom_jugador, nom_casella, preus, jugadors, tauler)
                elif jugada_escollida == 'comprar casa':
                    jugador_compra_casa(nom_jugador, nom_casella, jugadors, tauler)
                elif jugada_escollida == 'comprar hotel':
                    jugador_compra_hotel(nom_jugador, nom_casella, jugadors, tauler)

                
                #Si el usuario escoge una jugada que consista en consultar información, volvemos a pedirle un input
                elif jugada_escollida == 'preus':
                    imprimeix_preus_casella_actual(nom_casella, preus) #Mostramos en la parte central los precios de comprar casa y hotel.
                    continue
                elif jugada_escollida == 'preu banc':
                    imprimeix_ganancias_vendre_a_banc(nom_casella, preus, tauler) #Mostramos en la parte central cuánto ganaría el jugador si vende sus propiedades al banco (al 50% del precio que pagó originalmente)
                    continue
                elif jugada_escollida == 'preu jugador':
                    imprimeix_ganancias_vendre_a_jugador(nom_casella, preus, tauler) #Mostramos en la parte central cuánto ganaría el jugador si vende sus propiedades a otro jugador (al 90% del precio que pagó originalmente)
                    continue

                elif jugada_escollida == 'vendre al banc':
                    jugador_actual_ven_tot_al_banc(nom_jugador, preus, jugadors, tauler)
                elif jugada_escollida == 'vendre a B':
                    jugador_actual_vend_tot_a_altre_jugador(nom_jugador, 'Blau', preus, jugadors, tauler)
                elif jugada_escollida == 'vendre a T':
                    jugador_actual_vend_tot_a_altre_jugador(nom_jugador, 'Taronja', preus, jugadors, tauler)
                elif jugada_escollida == 'vendre a G':
                    jugador_actual_vend_tot_a_altre_jugador(nom_jugador, 'Groc', preus, jugadors, tauler)
                elif jugada_escollida == 'vendre a V':
                    jugador_actual_vend_tot_a_altre_jugador(nom_jugador, 'Vermell', preus, jugadors, tauler)
                
                break
            
        #Volvemos a imprimir tablero e información con la nueva jugada
        imprimeix_per_pantalla(tauler, banca, jugadors, jugades)
        
        #Comprobamos si el jugador ha perdido (no tiene dinero), retornando un 'bool':
        if jugador_perd(jugador_actual, jugadors): 
            #Eliminamos al jugador de la lista de jugadores:
            borrar_jugador_partida(ordre_jugadors, jugador_actual)
    
        #Si solo queda un jugador en la partida después del turno:
        if hi_ha_guanyador(ordre_jugadors):
            #Realizamos la impresión final por pantalla de la partida, y rompemos el bucle de juego:
            '''mostrar_ganador(ordre_jugadors)'''
            break

#endregion Joc

#region MAIN
clearScreen()
main()
mou_cursor(0, 26)
#endregion MAIN