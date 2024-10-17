# MONOPOLY
# IES ESTEVE TERRADAS I ILLAS
# DAM 2024-2025
# RUBÉN BELLIDO Y ALEJANDRO LÓPEZ

import random
import json

MIN_DINERS_BANCA = 500000

banca = 1000000

casella_mesures = {
    "alt": 2,
    "ampla": 8
}

tauler_mesures = {
    "ampla_total": 64,
    "ampla_partida": 10
}

#Array que utilizaremos para generar un orden de tiradas, y el diccionario de jugadores:
noms_jugadors = ["Vermell","Groc","Taronja","Blau"]

#Tupla que utilizaremos para recorrerla con las tiradas de dados, de forma ordenada:
caselles_ordenades = ("Sortida",
                      "Lauria",
                      "Rosselló",
                      "Sort",
                      "Marina",
                      "C. de cent",
                      "Presó",
                      "Muntaner",
                      "Aribau",
                      "Caixa",
                      "Sant Joan",
                      "Aragó",
                      "Parking",
                      "Urquinaona",
                      "Fontana",
                      "Sort",
                      "Les Rambles",
                      "Pl. Catalunya",
                      "Anr pró",
                      "P.Àngel",
                      "Via Augusta",
                      "Caixa",
                      "Balmes",
                      "Pg. de Gràcia"
                      )

caselles_posicions = (("Sortida",[19,55]),
                      ("Lauria",[19,45]),
                      ("Rosselló",[19,37]),
                      ("Sort",[19,28]),
                      ("Marina",[19,19]),
                      ("C. de cent",[19,10]),
                      ("Presó",[19,0]),
                      ("Muntaner",[17,0]),
                      ("Aribau",[14,0]),
                      ("Caixa",[11,0]),
                      ("Sant Joan",[8,0]),
                      ("Aragó",[5,0]),
                      ("Parking",[1,0]),
                      ("Urquinaona",[1,10]),
                      ("Fontana",[1,19]),
                      ("Sort",[1,28]),
                      ("Les Rambles",[1,37]),
                      ("Pl. Catalunya",[1,45]),
                      ("Anr pró",[1,55]),
                      ("P.Àngel",[5,55]),
                      ("Via Augusta",[8,55]),
                      ("Caixa",[11,55]),
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

#Tupla con los nombres completos de cada casilla, sin contar las casillas especiales:
noms_complets = []
for casella in caselles_ordenades:
    if casella not in caselles_especials:
        noms_complets.append(casella)
noms_complets = tuple(noms_complets)

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
                                        "cartes":[]
                                        }
    return dict_jugadors

def genera_preus_caselles(noms_complets, preus_caselles, etiquetes_preus_caselles):
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

    for index, casella in enumerate(noms_complets):
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

def afegir_diners_banca():
    '''Añadimos dinero a la banca cuando esta no disponga de suficiente dinero (< 500.000€).
    
    Inputs: No tiene
    
    Retorna: No retorna ningún valor. Modifica el valor de la varialbe "banca"'''
    global banca
    banca += 500000

def gestiona_diners_banca(banca:int):
    '''Miramos la cantidad de dinero de la banca, si es menor a 500.000€, llamaremos a afegir_diners_banca()
    
    Input:
        -banca (int): Cantidad de dinero que tiene la banca
        
    Retorna: No retorna nada'''
    if banca < MIN_DINERS_BANCA:
        afegir_diners_banca()

def ordre_tirada(jugadors):
    '''Mezaclamos el diccionario de jugadores para que tengan un orden aleatorio
    
    Input:
        -jugadors(dict): Diccionario en el que cada clave es un jugador, y su valor asociado es un diccionario con información del jugador (icona, diners, posicio, propietats, es_preso, cartes)
        
    Retorna:
        -ordre_jugadors(list): Lista que contiene los nombres de los jugadores mezclados aleatoriamente. Esta lista marcará el orden de tiradas durante la partida.'''
    ordre_jugadors = list(jugadors.keys())
    random.shuffle(ordre_jugadors)
    return ordre_jugadors

def primer_pagament(jugadors):
    '''Añadimos a todos los jugadores 2000€ en sus cuentas.
    
    Input:
        -jugadors(dict): Diccionario en el que cada clave es un jugador, y su valor asociado es un diccionario con información del jugador (icona, diners, posicio, propietats, es_preso, cartes)
        
    Retorna: No retorna nada'''
    for jugador in jugadors:
        jugadors[jugador]["diners"] = 2000

def imprimeix_casella(nom, cases, hotels, jugadors):
    # Imprimimos por pantalla la casilla 
    # Gestionamos:
    #   - Impresión del nombre
    #   - Impresión del número de casas y hoteles
    #   - Impresión de los jugadores en la casilla
    pass

def imprimeix_fila(fila_caselles):
    # Recibimos una fila del tablero.
    # Iteramos por la fila e imprimimos cada una de las casillas de la fila
    pass

def imprimeix_taula(tauler):
    # Imprimimos del tablero, llamando cada de las fila con los separadores
    pass

def imprimeix_informacio_banca(banca):
    # Imprimimos la información de la banca
    #   Banca:
    #   Diners: 1838734
    pass

def imprimeix_informacio_jugador(jugador):
    # Imprimimos la información de la banca
    #   Jugador Groc:
    #   Carrers: 2834
    #   Diners: 1838734
    #   Especial: (res) "Nombre de las cartas especiales"
    pass

def imprimeix_informacio(banca, jugadors):
    # Gestiona la impresión a la izquierda del tablero
    # ¡MIRAR COMO CAMBIAR LA POSICIÓN DEL PUNTERO DE CONSOLA!
    pass

def mira_propietari(casella_propietari, jugador):
    # Devuelva si el jugador es el propietario de la casilla o no
    pass

def cobra_casella(casella, jugador):
    # Miramos si la casilla tiene propietario:
    #   - En caso de no tener, no hacemos nada y continuamos
    #   - En caso de tener, deberemos reviasar su propietario:
    #       - Si es suya, no hacemos nada
    #       - Si es de otro jugador, deberemos hacerle pagar su valor en casas/hoteles
    pass

def imprimeix_jugades(accions):
    # Imprimimos en el espacio central del tablero 10 líneas de acciones realizadas por los jugadores
    amplada = tauler_mesures["ampla_total"] - (tauler_mesures["ampla_partida"] * 2)
    pass

def opcio_es_truc(opcio):
    # Miramos si tiene alguna opción de los trucos ('anar a')
    pass

def gestiona_truc(opcio):
    # Revismos que el truco se válido
    # Aplicamos el truco
    # Añadimos acción a la lista
    pass

def gestiona_accio_usuari():
    # Pedimos al usuario una acción
    # - Gestionamos trucos
    # Deberemos revisar en que posición se encuentra
    #   - En caso de que solo pueda 'passar', imprimiremos información y pasaremos de turno
    # Mostrar las acciones que puede realizar
    # Preguntar hasta optener opción válida
    # Gestionar opción y realizar acción correspondiente
    # Añadir dentro de acciones, que se deberán imprimir al acabar su turno
    pass

def main():
    pass