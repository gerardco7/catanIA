from BoardCopy import *
from GameConstants import *
from collections import Counter
import copy
from random import randint

class DiceAgent:
  """
  Class: DiceAgent
  ---------------------
  DiceAgent represents the random agent responsible for the
  roll of the dice for resources each turn.  It generates a
  number from 1-12 with the correct probability distribution
  corresponding to rolling 2 6-sided dice.
  ---------------------
  """

  def __init__(self, numDiceSides = 6):
    self.agentType = AGENT[0]
    self.NUM_DICE_SIDES = numDiceSides

  def rollDice(self):
    """
    Method: rollDice
    ----------------------
    Parameters: NA
    Returns: an integer representing the result of a random
      roll of 2 6-sided dice
    ----------------------
    """
    return randint(1, self.NUM_DICE_SIDES) + randint(1, self.NUM_DICE_SIDES)

  def getRollDistribution(self):
    """
    Method: getRollDistribution
    -----------------------------
    Parameters: NA
    Returns: a list of (ROLL, PROBABILITY) tuples containing
      all the possible rolls and the probabilities that they will be rolled.
    -----------------------------
    """
    # Tally up all the possible roll combinations
    # and the number of dice roll combinations per dice total
    totalRolls = 0
    rollCounter = Counter()
    for dice1 in range(1, self.NUM_DICE_SIDES + 1):
      for dice2 in range(1, self.NUM_DICE_SIDES + 1):
        rollCounter[dice1 + dice2] += 1
        totalRolls += 1

    # Return the list of probability tuples
    return [(roll, rollCounter[roll] / float(totalRolls)) for roll in rollCounter]

  def deepCopy(self):
    """
    Method: deepCopy
    -------------------------
    Parameters: NA
    Returns: a new DiceAgent object

    Returns a copy of this agent (which is essentially just a new DiceAgent).
    -------------------------
    """
    return DiceAgent()


class PlayerAgent(object):
  """
  Class: PlayerAgent
  ---------------------
  PlayerAgent defines a generic player agent in Settlers consisting of a name,
  player index, and player stats/game-specific information like number
  of victory points, lists of all roads, settlements, and cities owned by the
  player, and a counter of resources that the player has.

  Instance Variables:
  ---
  agentType = the type of game agent (PLAYER_AGENT)
  name = a string containing the name of the player
  agentIndex = the player index
  victoryPoints = the number of victory points the player has
  roads = a list of Tiles objects representing the roads a player has
  settlements = a list of Tiles objects representing the settlements a player has
  cities = a list of Tiles objects representing the cities a player has
  resources = a Counter containing the count of each resource type (in ResourceTypes) the player has
  ---------------------
  """

  def __init__(self, name, agentIndex):
    self.agentType = AGENT[1]
    self.name = name
    self.agentIndex = agentIndex
    self.victoryPoints = 0

    # List of roads
    self.roads = []

    # List of settlements 
    self.settlements = []

    # List of Cities owned
    self.cities = []

    # Counter of resources initialized to zero
    self.resources = Counter({i: 0 for i in range(5)})
    
  def __repr__(self):
    """
    Method: __repr__
    ---------------------
    Parameters: NA
    Returns: a string representation of the current PlayerAgent.
    ---------------------
    """
    s = "---------- " + self.name + " ----------\n"
    s += "Victory points: " + str(self.victoryPoints) + "\n"
    s += "Resources: " + str(self.resources) + "\n"
    s += "Settlements (" + str(len(self.settlements)) + "): " + str(self.settlements) + "\n"
    s += "Roads (" + str(len(self.roads)) + "): " + str(self.roads) + "\n"
    s += "Cities (" + str(len(self.cities)) + "): " + str(self.cities) + "\n"
    s += "--------------------------------------------\n"
    return s


  def canSettle(self):
    """
    Method: canSettle
    ---------------------
    Parameters: NA
    Returns: True/False whether or not this PlayerAgent has enough
      resources to build a new settlement (based on the SETTLEMENT_COST constant)
    ---------------------
    """
    modifiedResources = copy.deepcopy(self.resources)
    modifiedResources.subtract(SETTLEMENT_COST)

    # If any resource counts dip below 0, we don't have enough
    for resourceType in modifiedResources:
      if modifiedResources[resourceType] < 0:
        return False

    return True

  def canBuildCity(self):
    """
    Method: canBuildCity
    ----------------------
    Parameters: NA
    Returns: True/False whether or not this PlayerAgent has enough
      resources to build a new city (based on the CITY_COST constant)
    ----------------------
    """
    modifiedResources = copy.deepcopy(self.resources)
    modifiedResources.subtract(CITY_COST)

    # If any resource counts dip below 0, we don't have enough
    for resourceType in modifiedResources:
      if modifiedResources[resourceType] < 0:
        return False

    return True

  def canBuildRoad(self):
    """
    Method: canBuildRoad
    ----------------------
    Parameters: NA
    Returns: True/False whether or not this PlayerAgent has enough
      resources to build a new road (based on the ROAD_COST constant)
    ----------------------
    """
    modifiedResources = copy.deepcopy(self.resources)
    modifiedResources.subtract(ROAD_COST)

    # If any resource counts dip below 0, we don't have enough
    for resourceType in modifiedResources:
      if modifiedResources[resourceType] < 0:
        return False

    return True

  def deepCopy(self, board):
    """
    Method: deepCopy
    ----------------------
    Parameters:
      board - the current state of the board (an instance of Board)
    Returns: a deep copy of this instance of PlayerAgent, including full
      copies of all instance Variables
    ----------------------
    """
    newCopy = PlayerAgent(self.name, self.agentIndex)
    newCopy.victoryPoints = self.victoryPoints
    newCopy.roads = [board.getTile(road.X, road.Y) for road in self.roads]
    newCopy.settlements = [board.getTile(settlement.X, settlement.Y) for settlement in self.settlements]
    newCopy.resources = copy.deepcopy(self.resources)
    newCopy.cities = [board.getTile(city.X, city.Y) for city in self.cities]
    return newCopy

  def applyAction(self, action, board):
    """
    Method: applyAction
    -----------------------
    Parameters:
      action - the action tuple (ACTION, LOCATION) to applyAction
    Returns: NA

    Applies the given action tuple to the current player.  Does this
    by deducting resources appropriately and adding to/removing from the player's
    lists of roads, settlements, and cities.
    -----------------------
    """
    if action == None:
      return

    action[0] = int(action[0])
    # Settling
    if action[0] == Actions["SETTLE"]:
      if not self.canSettle():
        raise Exception("Player " + str(self.agentIndex) + " doesn't have enough resources to build a settlement!")
      
      # Add this settlement to our settlements list and update victory
      # points and resources
      tile = action[1]
      board.applyAction(self.agentIndex, action)
      self.settlements.append(tile)
      self.resources.subtract(SETTLEMENT_COST)
      self.victoryPoints += SETTLEMENT_VICTORY_POINTS

    # Building a road
    if action[0] == Actions["ROAD"]:
      if not self.canBuildRoad():
        raise Exception("Player " + str(self.agentIndex) + " doesn't have enough resources to build a road!")

      # Add this road to our roads list and update resources
      road = action[1]
      board.applyAction(self.agentIndex, action)
      self.roads.append(road)
      self.resources.subtract(ROAD_COST)

    # Building a city
    if action[0] == Actions["CITY"]:
      if not self.canBuildCity():
        raise Exception("Player " + str(self.agentIndex) + " doesn't have enough resources to build a city!")
      
      # Add this city to our list of cities and remove this city
      # from our list of settlements (since it was formerly a settlement)
      tile = action[1]
      board.applyAction(self.agentIndex, action)
      self.cities.append(tile)
      for settlement in self.settlements:
        if settlement.x == tile.x and settlement.y == tile.y:
          self.settlements.remove(settlement)
          break

      # and update victory points and resources
      self.resources.subtract(CITY_COST)
      self.victoryPoints += CITY_VICTORY_POINTS

  def updateResources(self, diceRoll, board):
    """
    Method: updateResources
    -----------------------------
    Parameters:
      diceRoll - the sum of the two dice Rolled
      board - a Board object representing the current board state
    Returns: a Counter containing the number of each resource gained

    Takes the current dice roll and board setup, and awards
    the current player resources depending on built settlements on the board.
    Returns the count of each resource that the player gained.
    -----------------------------
    """
    newResources = board.getResourcesFromDieRoll(self.agentIndex, diceRoll)
    self.resources += newResources
    return newResources


  def collectInitialResources(self, board):
    """
    Method: collectInitialResources
    --------------------------------
    Parameters:
      board - a Board object representing the current board state

    Returns: NA

    Takes the current board setup and awards the current player
    resources for each of his/her current settlements.  For example,
    if the player had a settlement bordering BRICK and ORE and another
    one bordering BRICK, this player would receive 2 BRICK and 1 ORE.
    --------------------------------
    """
    # Get resources for each settlement
    for settlement in self.settlements:
      # Find all tiles bordering this settlement and
      # take 1 resource of each of the surrounding tile types
      tile = board.getTile(settlement.x, settlement.y)
      for hexagons in tile.hexagonids:
        hexagon = board.hexagons[hexagons]
        self.resources[hexagon.resource] += 1


  def hasWon(self):
    """
    Method: hasWon
    -----------------------------
    Parameters: NA
    Returns: True/False whether or not the curernt player
      has won the game (AKA met or exceeded VICTORY_POINTS_TO_WIN)
    -----------------------------
    """
    return self.victoryPoints >= VICTORY_POINTS_TO_WIN


  def getAction(self, state):
    """
    Method: getAction
    -----------------------------
    Parameters:
      state - a GameState object containing information about the current state of the game
    Returns: an action tuple (ACTION, LOCATION) of the action this player should take
    
    Note: must be overridden by a subclass
    -----------------------------
    """
    raise Exception("Cannot get action for superclass - must implement getAction in PlayerAgent subclass!")
