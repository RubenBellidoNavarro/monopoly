# MONOPOLY
# IES ESTEVE TERRADAS I ILLAS
# DAM 2024-2025
# RUBÉN BELLIDO Y ALEJANDRO LÓPEZ

import sys
import os
import re # Usado para poder cambiar el nombre de las casillas de 'Sort' i 'Caixa', ya que necesitan un 1 o 2 al final para identificarlas correctamente
from colorama import just_fix_windows_console # Paquete para que la terminal de Windows entienda los caràcteres ANSI y podamos mover el cursor a la posición que deseemos

just_fix_windows_console()

#region VARIABLESYCONSTANTES
MIN_DINERS_BANCA = 500000
MAX_LINIES_JUGADES = 13


import random
import json
import time

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
caselles_ordenades = ("Sortida",
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
                      )

caselles_posicions = (("Sortida",[19,55]),
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
                      )


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
caselles_especials = ("Sort","Presó","Caixa","Anr pró","Sortida","Parking")

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
#endregion VARIABLESYCONSTANTES

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

#region GestioBanca
def afegir_diners_banca(banca):
    '''Añadimos dinero a la banca cuando esta no disponga de suficiente dinero (< 500.000€).
    
    Inputs: No tiene
    
    Retorna: No retorna ningún valor. Modifica el valor de la varialbe "banca"'''
    banca += 500000
    return banca

def gestiona_diners_banca(banca:int):
    '''Miramos la cantidad de dinero de la banca, si es menor a 500.000€, llamaremos a afegir_diners_banca()
    
    Input:
        -banca (int): Cantidad de dinero que tiene la banca
        
    Retorna: No retorna nada'''
    if banca < MIN_DINERS_BANCA:
        afegir_diners_banca()
#endregion GestioBanca

#region ImpresionTablero
def imprimeix_separador():
    amplada = casella_mesures["ampla"]
    print(f"+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+{"".ljust(amplada, "-")}+")

def imprimeix_casella_vertical(nom, cases, hotels, jugadors, posicio):
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

def imprimeix_casella_horizontal(nom, cases, hotels, jugadors, posicio):
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

def imprimeix_fila(fila_caselles):
    # Recibimos una fila del tablero.
    # Iteramos por la fila e imprimimos cada una de las casillas de la fila
    for casella in fila_caselles:
            imprimeix_casella(casella["nom_acortat"], casella["cases"], casella["hotels"], casella["jugadors"], casella["posicio"])

def imprimeix_taula(tauler):
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
def imprimeix_informacio_banca(banca):
    # Imprimimos la información de la banca
    #   Banca:
    #   Diners: 1838734
    mou_cursor(posicions_informacio[0][0], posicions_informacio[0][1])
    print("Banca: ")
    mou_cursor(posicions_informacio[0][0], posicions_informacio[0][1] + 1)
    print(f"Diners: {banca}")

def imprimeix_informacio_jugador(index, jugador):
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

def imprimeix_informacio(banca, jugadors):
    # Gestiona la impresión a la izquierda del tablero
    # ¡MIRAR COMO CAMBIAR LA POSICIÓN DEL PUNTERO DE CONSOLA!
    imprimeix_informacio_banca(banca)

    for index, jugador in enumerate(jugadors.values()):
        imprimeix_informacio_jugador(index + 1, jugador)
#endregion ImprimirInformacion

#region ImprimirJugadas
def imprimeix_jugades(accions):
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
            print(accio)
        else:
            print(f"  {accio}")
        
        # Aumentamos en 1 la línea
        posicio_y += 1
#endregion ImprimirJugadas

#region Joc
def afegeix_jugadors_sortida(jugadors: dict, ordre: list, tauler: list) -> None:
    casella_sortida = list(filter(lambda casella: casella["nom_complet"] == "Sortida", tauler))
    for jugador in ordre:
        jugadors[jugador]["posicio"] = casella_sortida[0]["posicio"]
        casella_sortida[0]["jugadors"].append(jugadors[jugador]["icona"])

def genera_partida():
    tauler = genera_tauler(caselles_ordenades, caselles_ordenades_nom_acortat, caselles_especials, caselles_posicions)
    jugadors = genera_jugadors(noms_jugadors)
    ordre_jugadors = ordre_tirada(jugadors)
    gestiona_diners_banca(banca)
    primer_pagament(jugadors)
    afegeix_jugadors_sortida(jugadors, ordre_jugadors, tauler)
    imprimeix_taula(tauler)
    imprimeix_informacio(banca, jugadors)
    return tauler, jugadors, ordre_jugadors

def main():
    tauler, jugadors, ordre_jugadors = genera_partida()

    contador_jugador = 0    

    '''
    Contador que sirve para marcar el índice a mirar dentro de la lista de jugadores dentro del bucle

    Utilizamos esta solución porque la otra opción para recorrer la lista de jugadores sería hacer un bucle 'for' (dentro del bucle 'while True')
    y esto nos causarñia problemas cuando queramos modificar la lista de jugadores (a la vez que se realiza el bucle 'for'), como por ejemplo
    cuando eliminemos un jugador de la lista que ha perdido la partida.
    '''

    while True:

        #Miramos al principio de cada jugada si el contador rebasa la lista de jugadores. Si es así, se reinicia a 0.
        if contador_jugador > len(lista_jugadores):
            contador_jugador = 0

        jugador_actual = jugadors[ordre_jugadors[contador_jugador]]

    #   - Tiramos dados del jugador
        if jugador_a_la_presio(dict_jugadores): #devuelve un booleano diciendo si el jugador está en la prisión
            actualizar_jugador_preso(dict_jugadors) #actualiza el contador de turnos que lleva el jugador en la prision. Si el contador == 3, pone el contador a 0 y cambia la variable 'es_preso' a False
            contador_jugador += 1
            continue #pasamos al siguiente jugador
        tirar_dados() #Se retornan una tupla con los valores de los 2 dados

    #   - Actualizamos posición en tablero (borramos actual y ponemos la nueva, tanto en jugador como en casilla)
        actualitza_posicion(tauler, dict_jugadores, tirada_dados)

    #   - Añadimos jugada a la lista de jugadas (para poder imprimirla)
        afegir_jugada(jugada, lista_jugadas)





    #   - Revisamos qué opciones tiene el usuario según la casilla en la que se encuentra
        casilla_jugador = jugador_actual["posicio"]
        if casilla_jugador in caselles_especials:
        
            if casilla_jugador == "Parking": #en esta casilla, el jugador sólo puede pasar
                imprimeix_taula()
                imprimeix_informacio()
                time.sleep(1)
                contador_jugador += 1
                continue

            elif casilla_jugador == "Anr pró":
                pass
                '''
                #Actualizar posicion tauler (mandar a casilla Presso)
                #Actualizar posicion jugadors (mandar a casila Presso)

                #Actualizar clave "es_preso" del jugador a 'True'
                #Si el jugador tiene la carta de 'salir prision', poner 'es_preso' del jugador con valor 'False'.
                '''

            elif casilla_jugador == "Sortida":
                #Añadimos 200€ al jugador
                nom_jugador = jugador_actual["nom"]
                jugadors["nom"]["diners"] += 200

                #Actualizamos la impresión por pantalla y damos 1 segundo para que el usuario vea que ha ocurrido
                imprimeix_taula()
                imprimeix_informacio()
                time.sleep(1)
                contador_jugador += 1
                continue

            elif casilla_jugador == "Presó":
                '''
                #Actualizar clave "es_preso" del jugador a 'True'
                #Si el jugador tiene la carta de 'salir prision', poner 'es_preso' del jugador con valor 'False'.
                '''
            
        calcula_jugadas() #Decide qué jugadas puede realizar el jugador (retorna lista de jugadas)
        mostra_jugadas() #imprime por pantalla las posibles jugadas
        input_jugador() #Pide y gestiona el input que ponga el jugador (pedir input hasta que la jugada sea correcta)
        
        funciones especificas en funcion de imput de jugador (jugada1(), jugada2(), etc.)
        if jugador_perd(): #comprueba si el jugador ha perdido (no tiene dinero)
            borrar_jugador_partida() #Se elimina del diccionario de jugadores y del tablero

        #   - Volvemos a imprimir tablero e información con la nueva jugada
        clearScreen()
        IMPRIMIR TABLERO
    
        if len(lista_jugadores) == 1: #Si solo queda un jugador en la partida === Si hay un ganador
            break

    mostrar_ganador()
    pass
#endregion Joc

#region MAIN
clearScreen()
main()
mou_cursor(0, 25)
#endregion MAIN

# MONTAR DENTRO DE UNA FUNCIÓN (SE LLAMA AL INICIAR EL PROGRAMA)
#Tupla con los nombres completos de cada casilla, sin contar las casillas especiales:
noms_complets = []
for casella in caselles_ordenades:
    if casella not in caselles_especials:
        noms_complets.append(casella)
noms_complets = tuple(noms_complets)
