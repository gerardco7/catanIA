import random
from GameConstants import *

class Hexagon:

  def __init__(self, resource, number, id):
    self.id = id
    self.resource = resource  
    self.number = number
    self.tiles = []

  def addTiles(self, tiles):
    for tile in tiles:
      self.tiles.append(tile)

  def __repr__(self):
    tiles = self.tiles
    val = "--------------HEXAGON INFO---------------\n"
    val += "Hexagon: " + str(self.id) +"\n"
    val += "Resource Type: " + str(self.resource) +"\n"
    val += "Tile number: " + str(self.number) +"\n"
    return val


class Tile:
  """
  Class: Tile
  ---------------------------
  A Tile represents a single square on our square gameboard.  A tile
  has a resource type, a roll number, and, optionally, can have a road
  or settlement be built on it by a single player.
  ---------------------------
  """


  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.player = None
    self.structure = Structure["NONE"] # Settlement, vertical road, or horizontal road
    self.hexagonids = []


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
    if self.isWater(): 
      raise Exception("This tile is water!")
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
    if self.isWater(): 
      raise Exception("This tile is water!")
    self.player = playerIndex
    self.structure = Structure["ROAD"]

  
  def addHexagon(self, hexagon):
    self.hexagonids.append(hexagon.id)


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
    return val
  

  def isWater(self):
    if (self.x == 0 and self.y == 0) or (self.x == 0 and self.y == 1) or (self.x == 1 and self.y == 0) or (self.x == 4 and self.y == 0) or (self.x == 5 and self.y == 1) or (self.x == 5 and self.y == 0) or (self.x == 0 and self.y == 9) or (self.x == 0 and self.y == 10) or (self.x == 1 and self.y == 10) or (self.x == 4 and self.y == 10) or (self.x == 5 and self.y == 9) or (self.x == 5 and self.y == 10): return True
    return False


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
    if self.isWater(): return "XX"
    if not self.isOccupied(): return "--"
    if self.structure == Structure["ROAD"]:
        return COLORS[self.player] + "R" + str(self.player) + END_COLOR
    if self.structure == Structure["SETTLEMENT"]:
        return COLORS[self.player]  + "S" + str(self.player) + END_COLOR
    if self.structure == Structure["CITY"]:
        return COLORS[self.player]  + "C" + str(self.player) + END_COLOR
    raise Exception("strRepresentation - invalid tile")
  

class Board:
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

  def __init__(self, size_x=6, size_y=11):

    self.size_x = size_x
    self.size_y = size_y

    possibleResources = [4,4,4,4,1,1,1,1,3,3,3,3,2,2,2,0,0,0] 
    random.shuffle(possibleResources)

    possiblenumbers = [2,3,3,4,4,5,5,5,6,6,8,8,9,9,10,10,11,11,12]
    random.shuffle(possiblenumbers)

    self.hexagons = []

    for i in range (19):
      if i == 9:
        hexagon = Hexagon(-1, 7, 9)
      elif i == 18:
        hexagon = Hexagon(possibleResources[9], possiblenumbers[9], 19)
      else:
        hexagon = Hexagon(possibleResources[i], possiblenumbers[i], i)
      self.hexagons.append(hexagon)

    
    self.hexagons[0].addTiles([Tile(0, 2), Tile(0, 3), Tile(0, 4), Tile(1, 2), Tile(1, 3), Tile(1, 4)])
    self.hexagons[1].addTiles([Tile(0, 4), Tile(0, 5), Tile(0, 6), Tile(1, 4), Tile(1, 5), Tile(1, 6)]) 
    self.hexagons[2].addTiles([Tile(0, 6), Tile(0, 7), Tile(0, 8), Tile(1, 6), Tile(1, 7), Tile(1, 8)])
    self.hexagons[3].addTiles([Tile(1, 1), Tile(1, 2), Tile(1, 3), Tile(2, 1), Tile(2, 2), Tile(2, 3)])
    self.hexagons[4].addTiles([Tile(1, 3), Tile(1, 4), Tile(1, 5), Tile(2, 3), Tile(2, 4), Tile(2, 5)])
    self.hexagons[5].addTiles([Tile(1, 5), Tile(1, 6), Tile(1, 7), Tile(2, 5), Tile(2, 6), Tile(2, 7)])
    self.hexagons[6].addTiles([Tile(1, 7), Tile(1, 8), Tile(1, 9), Tile(2, 7), Tile(2, 8), Tile(2, 9)])
    self.hexagons[7].addTiles([Tile(2, 0), Tile(2, 1), Tile(2, 2), Tile(3, 0), Tile(3, 1), Tile(3, 2)])
    self.hexagons[8].addTiles([Tile(2, 2), Tile(2, 3), Tile(2, 4), Tile(3, 2), Tile(3, 3), Tile(3, 4)])
    self.hexagons[9].addTiles([Tile(2, 4), Tile(2, 5), Tile(2, 6), Tile(3, 4), Tile(3, 5), Tile(3, 6)])
    self.hexagons[10].addTiles([Tile(2, 6), Tile(2, 7), Tile(2, 8), Tile(3, 6), Tile(3, 7), Tile(3, 8)])
    self.hexagons[11].addTiles([Tile(2, 8), Tile(2, 9), Tile(2, 10), Tile(3, 8), Tile(3, 9), Tile(3, 10)])
    self.hexagons[12].addTiles([Tile(3, 1), Tile(3, 2), Tile(3, 3), Tile(4, 1), Tile(4, 2), Tile(4, 3)])
    self.hexagons[13].addTiles([Tile(3, 3), Tile(3, 4), Tile(3, 5), Tile(4, 3), Tile(4, 4), Tile(4, 5)])
    self.hexagons[14].addTiles([Tile(3, 5), Tile(3, 6), Tile(3, 7), Tile(4, 5), Tile(4, 6), Tile(4, 7)])
    self.hexagons[15].addTiles([Tile(3, 7), Tile(3, 8), Tile(3, 9), Tile(4, 7), Tile(4, 8), Tile(4, 9)])
    self.hexagons[16].addTiles([Tile(4, 2), Tile(4, 3), Tile(4, 4), Tile(5, 2), Tile(5, 3), Tile(5, 4)])
    self.hexagons[17].addTiles([Tile(4, 4), Tile(4, 5), Tile(4, 6), Tile(5, 4), Tile(5, 5), Tile(5, 6)])
    self.hexagons[18].addTiles([Tile(4, 6), Tile(4, 7), Tile(4, 8), Tile(5, 6), Tile(5, 7), Tile(5, 8)])

    self.board = []
    for i in range(size_x):
      boardRow = []
      for j in range(size_y):
          boardRow.append(Tile(i, j))
      self.board.append(boardRow)

    for i in range(19):
      for tile in self.hexagons[i].tiles:
        self.getTile(tile.x, tile.y).addHexagon(self.hexagons[i])

    self.settlements = []
    self.roads = []


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
    if 0 <= x < self.size_x and 0 <= y < self.size_y:
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
    s = "                " + self.board[0][3].strRepresentation() + "        " + self.board[0][5].strRepresentation()  + "        " + self.board[0][7].strRepresentation() + "                   \n" 
    s += "           " + self.board[0][2].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[0].resource) + " " + self.board[0][4].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[1].resource) + " " + self.board[0][6].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[2].resource)  + " " + self.board[0][8].strRepresentation() + " \n"
    
    s += "           " + self.board[1][2].strRepresentation() + "   " + str(self.hexagons[0].number) + "   " 
    if self.hexagons[0].number < 10: s += " "
    s += self.board[1][4].strRepresentation() + "   " + str(self.hexagons[1].number) + "   " 
    if self.hexagons[1].number < 10: s += " "
    s += self.board[1][6].strRepresentation() + "   " + str(self.hexagons[2].number)  + "   " 
    if self.hexagons[2].number < 10: s += " "
    s += self.board[1][8].strRepresentation() + " \n"

    s += "      " + self.board[1][1].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[3].resource) + " " + self.board[1][3].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[4].resource) + " " + self.board[1][5].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[5].resource)  + " " + self.board[1][7].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[6].resource) + " " + self.board[1][9].strRepresentation() + " \n"

    s += "      " + self.board[2][1].strRepresentation() + "   " + str(self.hexagons[3].number) + "   " 
    if self.hexagons[3].number < 10: s += " "
    s += self.board[2][3].strRepresentation() + "   " + str(self.hexagons[4].number) + "   " 
    if self.hexagons[4].number < 10: s += " "
    s += self.board[2][5].strRepresentation() + "   " + str(self.hexagons[5].number)  + "   " 
    if self.hexagons[5].number < 10: s += " "
    s += self.board[2][7].strRepresentation() + "   " + str(self.hexagons[6].number)  + "   " 
    if self.hexagons[6].number < 10: s += " "
    s += self.board[2][9].strRepresentation() +  " \n"
  
    s += " " + self.board[2][0].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[7].resource) + " " + self.board[2][2].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[8].resource) + " " + self.board[2][4].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[9].resource) + " " + self.board[2][6].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[10].resource) + " " + self.board[2][8].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[11].resource)  + " " + self.board[2][10].strRepresentation() + " \n"

    s += " " + self.board[3][0].strRepresentation() + "   " + str(self.hexagons[7].number) + "   " 
    if self.hexagons[7].number < 10: s += " "
    s += self.board[3][2].strRepresentation() + "   " + str(self.hexagons[8].number) + "   " 
    if self.hexagons[8].number < 10: s += " "
    s += self.board[3][4].strRepresentation() + "   " + str(self.hexagons[9].number)  + "   " 
    if self.hexagons[9].number < 10: s += " "
    s += self.board[3][6].strRepresentation() + "   " + str(self.hexagons[10].number)  + "   " 
    if self.hexagons[10].number < 10: s += " "
    s += self.board[3][8].strRepresentation() + "   " + str(self.hexagons[11].number)  + "   " 
    if self.hexagons[11].number < 10: s += " "
    s += self.board[3][10].strRepresentation() + " \n"

    s += "      " + self.board[3][1].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[12].resource) + " " + self.board[3][3].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[13].resource) + " " + self.board[3][5].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[14].resource) + " " + self.board[3][7].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[15].resource) + " " + self.board[3][9].strRepresentation() + " \n"

    s += "      " + self.board[4][1].strRepresentation() + "   " + str(self.hexagons[12].number) + "   " 
    if self.hexagons[12].number < 10: s += " "
    s += self.board[4][3].strRepresentation() + "   " + str(self.hexagons[13].number) + "   " 
    if self.hexagons[13].number < 10: s += " "
    s += self.board[4][5].strRepresentation() + "   " + str(self.hexagons[14].number)  + "   " 
    if self.hexagons[14].number < 10: s += " "
    s += self.board[4][7].strRepresentation() + "   " + str(self.hexagons[15].number)  + "   " 
    if self.hexagons[15].number < 10: s += " "
    s += self.board[4][9].strRepresentation() + " \n"

    s += "           " + self.board[4][2].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[16].resource) + " " + self.board[4][4].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[17].resource) + " " + self.board[4][6].strRepresentation() + " " + value2key(ResourceTypes, self.hexagons[18].resource) + " " + self.board[4][8].strRepresentation() +  " \n"

    s += "           " + self.board[5][2].strRepresentation() + "   " + str(self.hexagons[16].number) + "   " 
    if self.hexagons[16].number < 10: s += " "
    s += self.board[5][4].strRepresentation() + "   " + str(self.hexagons[17].number) + "   " 
    if self.hexagons[17].number < 10: s += " "
    s += self.board[5][6].strRepresentation() + "   " + str(self.hexagons[18].number)  + "   " 
    if self.hexagons[18].number < 10: s += " "
    s += self.board[5][8].strRepresentation() +  " \n"
    

    s += "                " + self.board[5][3].strRepresentation() + "        " + self.board[5][5].strRepresentation()  + "        " + self.board[5][7].strRepresentation() + " \n" 
    return print(s)
  

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
      for hexagonid in settlement.hexagonids:
        hexagon = self.hexagons[hexagonid]
        if hexagon.number == dieRoll and settlement.player == playerIndex:
          for resource in hexagon.resource:
            if settlement.structure == Structure["CITY"]:
              resources[resource] += 2
            else:
              resources[resource] += 1
                
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
      occupiedNeighbors2 = self.getOccupiedNeighbors(neighbor, diagonals=False)
      for neighbor2 in occupiedNeighbors2:
        if neighbor2.structure == Structure["SETTLEMENT"]:
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
  