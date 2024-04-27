import numpy as np
from collections import Counter

def value2key(diccionario, valor):
    for clave, val in diccionario.items():
        if val == valor:
            return clave
    return None  # Devolver None si el valor no se encuentra en el diccionario

Actions = {
  "SETTLE": 1,
  "CITY": 2,
  "ROAD": 3,
  "TRADE": 4
}

ResourceTypes = {
  "BRICK ": 0,
  " WOOL ": 1,
  " ORE  ": 2,
  "GRAIN ": 3,
  "LUMBER": 4,
  " NONE ": -1
}

Structure = {
  "ROAD": 0,
  "SETTLEMENT": 1,
  "CITY": 2,
  "NONE": 3
}


VERBOSE = True

VICTORY_POINTS_TO_WIN = 10
SETTLEMENT_VICTORY_POINTS = 1
CITY_VICTORY_POINTS = SETTLEMENT_VICTORY_POINTS + 1

NUM_INITIAL_SETTLEMENTS = 2
# TOTAL_NUM_AGENTS = 13
CUTOFF_TURNS = 600

DEFAULT_PLAYER_ARRAY = np.array([4, 0])

# Crear contadores para los costos de construcción
ROAD_COST = {
  0: 1,
  1: 0,
  2: 0,
  3: 0,
  4: 1
}

SETTLEMENT_COST = {
  0: 1,
  1: 1,
  2: 0,
  3: 1,
  4: 1
}

CITY_COST = {
  0: 0,
  1: 0,
  2: 3,
  3: 2,
  4: 0
}

NUM_PLAYERS = 2
NUM_ITERATIONS = 4
DEPTH = 3

# Types of Agents
AGENT = np.array(["PLAYER_AGENT", "DICE_AGENT"])

COLORS = [
  "\033[91m", # Rojo
  "\033[92m",  # Verde
  "\033[94m",  # Azul
  "\033[93m",  # Amarillo
]

END_COLOR = "\033[0m"