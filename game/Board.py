import random
from GameConstants import *

class Tile:
  """
  Class: Tile
  ---------------------------
  A Tile represents a single square on our square gameboard.  A tile
  has a resource type, a roll number, and, optionally, can have a road
  or settlement be built on it by a single player.
  ---------------------------
  """


  def __init__(self, resource, number, x, y):
    self.resource = resource
    self.x = x
    self.y = y
    self.number = number
    self.player = None
    self.structure = Structure["NONE"] # Settlement, vertical road, or horizontal road


  """
  Method: isOccupied
  ---------------------------
  Parameters: None
  Returns: True/False depending on whether or not the tile has been used

  Returns whether or not this tile is occupied
  ---------------------------
  """
  def isOccupied(self):
    return self.structure != Structure["NONE"]


  """
  Method: settle
  ---------------------------
  Parameters:
    playerIndex: the index of the player that is settling on this tile
  Returns: NA

  Marks this tile as settled by the given player.  Throws an exception if
  this tile has already been used.
  ---------------------------
  """
  def settle(self, playerIndex):
    if self.isOccupied():
      raise Exception("This tile is already used!")
    self.player = playerIndex
    self.structure = Structure["SETTLEMENT"]
  
  """
  Method: upgrade
  ---------------------------
  Parameters:
    playerIndex: the index of the player that is settling on this tile
  Returns: NA

  Marks this tile as upgraded to a city by the given player.  Throws an exception if
  this tile is not settled by the proper player or doesn't have a settlement yet.
  Note that the tile is still within the settlements array so that all the adjacency
  methods work fine.
  ---------------------------
  """
  def upgrade(self, playerIndex):
    if self.structure != Structure["SETTLEMENT"]:
      raise Exception("This tile is not settled yet!")
    if self.player != playerIndex:
      raise Exception(str(self.player)+" has already settled here!")
    self.structure = Structure["CITY"]


  """
  Method: buildRoad
  ---------------------------
  Parameters:
    playerIndex: the index of the player that is building a road on this tile
  Returns: NA

  Builds a road owned by the given player on this tile.
  ---------------------------
  """
  def buildRoad(self, playerIndex):
    if self.isOccupied():
      raise Exception("Tile " + str(self) + " is already used!")
    self.player = playerIndex
    self.structure = Structure["ROAD"]


  """
  Method: __repr__ method
  ---------------------------
  Parameters: NA
  Returns: NA

  Prints out a description of this tile
  ---------------------------
  """
  def __repr__(self):
    val = "--------------TILE INFO AT (" + str(self.x) + ", " + str(self.y) + ")---------------\n"
    val += "Owned by player: " + str(self.player) +"\n"
    val += "Structure: " + str(self.structure) +"\n"
    val += "Resource Type: " + str(self.resource) +"\n"
    val += "Tile number: " + str(self.number) +"\n"
    return val


  """
  Method: strRepresentation
  ---------------------------
  Parameters: NA
  Returns: a "stringified" version of this tile

  Returns a string representing this tile.  If this tile is unused, this method
  returns "-".  If it is a settlement, it returns "S#", where # = the player who owns
  the settlement.  IF it is a road, it returns "R#", where # = the player who owns
  the road.  (Note: This method assumes the player index will never be more than 1 digit,
  since all tile string representations are length 2).
  ---------------------------
  """
  def strRepresentation(self):
    if not self.isOccupied(): return "--"
    elif self.structure == Structure["ROAD"]: return "R" + str(self.player)
    elif self.structure == Structure["SETTLEMENT"]: return "S" + str(self.player)
    raise Exception("strRepresentation - invalid tile")
  

class BasicBoard:
  """
  Class: BasicBoard
  ---------------------------
  A BasicBoard is an n x n grid of Tiles representing a simplified
  version of the Settlers of Catan gameboard.  Every Tile can be built
  on, and every tile has a resource type and roll number, along with an x and y.
  A BasicBoard contains an n x n grid of Tiles, as well as a list of all
  built settlements and a list of all built roads.
  ---------------------------
  """

  def __init__(self, size=5):
    self.board = []

    possibleResources = [] 
    for resource in ResourceTypes.values():
      possibleResources += 5*[resource]
      random.shuffle(possibleResources)

    possiblenumbers = [2,2,3,3,4,4,5,5,5,6,6,6,8,8,8,9,9,9,10,10,10,11,11,12,12]
    random.shuffle(possiblenumbers)
    for i in range(size):
      boardRow = []
      for j in range(size):
        boardRow.append(Tile(possibleResources.pop(), possiblenumbers.pop(), i, j))
      self.board.append(boardRow)

    self.settlements = []
    self.roads = []
    self.size = size


  """
  Method: getTile
  ---------------------------
  Parameters:
    x: the x coordinate of the tile to get
    y: the y coordinate of the tile to get
  Returns: the Tile object at that (x,y), or None if the coordinates are out of bounds

  Returns the tile on the board at the given coordinates, or None if the
  coordinates are out of bounds.
  ---------------------------
  """
  def getTile(self, x, y):
    if 0 <= x < self.size and 0 <= y < self.size:
      return self.board[x][y]
    return None

  """
  Method: printBoard
  ---------------------------
  Parameters: NA
  Returns: NA

  Prints out an ASCII representation of the current board state.
  It does this by printing out each row inside square brackets.
  Each tile is either '--' if it's unused, 'RX' if it's a road,
  or 'SX' if it's a settlement.  The 'X' in the road or settlement
  representation is the player who owns that road/settlement.
  ---------------------------
  """
  def printBoard(self):
    # Print top numbers
    s = "     "
    for i in range(self.size):
      s += str(i) + "   "
    print(s)

    for i, row in enumerate(self.board):
      s = str(i) + " ["
      for tile in row:
        s += " " + tile.strRepresentation() + " "
      print(s + "]")


  """
  Method: applyAction
  ---------------------------
  Parameters:
    playerIndex: the index of the player that is taking an action
    action: a tuple (ACTION_TYPE, Tile) representing the action to be
            taken and where that action should be taken.
  Returns: NA

  Updates the board to take the given action for the given player.  The action
  can either be building a settlement or building a road.
  ---------------------------
  """
  def applyAction(self, playerIndex, action):
    if action == None: return
    
    # Mark the tile as a settlement
    if action[0] == Actions["SETTLE"]:
      tile = action[1]
      tile.settle(playerIndex)
      self.settlements.append(tile)

    # Or mark the tile as a road
    elif action[0] == Actions["ROAD"]:
      tile = action[1]
      tile.buildRoad(playerIndex)
      self.roads.append(tile)

    # Or mark the tile as a city
    elif action[0] == Actions["CITY"]:
      tile = action[1]
      tile.upgrade(playerIndex)

  """
  Method: getNeighborTiles
  ---------------------------
  Parameters:
    tile: the Tile object to find the neighbors of
  Returns: a list of all the adjacent tiles to this tile

  Returns a list of all of the tiles immediately surrounding
  the passed-in tile
  ---------------------------
  """
  def getNeighborTiles(self, tile, diagonals=False):
    neighbors = []
    for dx in range(-1, 2):
      for dy in range(-1, 2):

        # Ignore the original tile
        if dx == 0 and dy == 0: continue

        # Optionally ignore diagonals
        if not diagonals and (dx != 0 and dy != 0): continue

        # If this location is in bounds, add the tile to our list
        currTile = self.getTile(tile.x + dx, tile.y + dy)
        if currTile != None:
          neighbors.append(currTile)

    return neighbors


  """
  Method: getUnoccupiedNeighbors
  ---------------------------
  Parameters:
    tile: the tile to return the neighbors for
  Returns: a list of all the unoccupied neighbors for this tile

  Returns a list of all of the unoccupied tiles adjacent to this tile
  ---------------------------
  """
  def getUnoccupiedNeighbors(self, tile, diagonals=True):
    neighbors = self.getNeighborTiles(tile, diagonals=diagonals)

    unoccupied = []
    for neighbor in neighbors:
      if not neighbor.isOccupied():
        unoccupied.append(neighbor)
    return unoccupied

  """
  Method: getResourcesFromDieRoll
  ---------------------------
  Parameters:
    tile: the tile to return the neighbors for
  Returns: a list of all the unoccupied neighbors for this tile

  Returns a list of all of the unoccupied tiles adjacent to this tile
  ---------------------------
  """
  def getResourcesFromDieRoll(self, playerIndex, dieRoll):
    resources = Counter() 
    
    for settlement in self.settlements:
      if settlement.number == dieRoll and settlement.player == playerIndex:
        resources[settlement.resource] += 1

        if settlement.structure == Structure["CITY"]:
            resources[settlement.resource] += 1
                
    return resources

  """
  Method: getOccupiedNeighbors
  ---------------------------
  Parameters:
    tile: the tile to return the neighbors for
  Returns: a list of all the occupied neighbors for this tile

  Returns a list of all of the occupied tiles adjacent to this tile
  ---------------------------
  """
  def getOccupiedNeighbors(self, tile, diagonals=True):
    neighbors = self.getNeighborTiles(tile, diagonals=diagonals)

    occupied = []
    for neighbor in neighbors:
      if neighbor.isOccupied():
        occupied.append(neighbor)

    return occupied


  """
  Method: isValidSettlementLocation
  ---------------------------
  Parameters:
    tile: the tile to check
  Returns: True/False depending on whether or not that tile is a valid settlement location

  Returns whether or not a settlement can validly be built on the given tile
  ---------------------------
  """
  def isValidSettlementLocation(self, tile):
    # It's a valid settlement location if there are no other settlements
    # within 1 space of this one
    occupiedNeighbors = self.getOccupiedNeighbors(tile, diagonals=False)
    for neighbor in occupiedNeighbors:
      if neighbor.structure == Structure["SETTLEMENT"]:
        return False

    return True


  """
  Method: getUnoccupiedRoadEndpoints
  ---------------------------
  Parameters:
    tile: the road to get endpoints for
  Returns: a list of all the unoccupied endpoints of the given road 

  Returns all the unoccupied endpoints of the given road.  Note
  that this could be up to 3 endpoints (since roads have no direction)
  ---------------------------
  """
  def getUnoccupiedRoadEndpoints(self, tile):
    if not tile.isOccupied() or tile.structure != Structure["ROAD"]:
      raise Exception("getUnoccupiedRoadEndpoints - not a road!")

    return self.getUnoccupiedNeighbors(tile, diagonals=False)
  