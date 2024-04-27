from BoardCopy import *
from GameConstants import *
from Agents import *

class GameState:
  """
  Class: GameState
  -------------------------------
  A class representing all information about the current state of the game.
  Includes a Board object representing the current state of the game board,
  as well as a list of all agents (players) in the game.
  -------------------------------
  """

  def __init__(self):
    """
    Method: __init__
    -----------------------------
    Parameters:
      prevState - an optional GameState object to pass in.  If this is passed
        in, this new GameState object will instead be cloned from prevState
      layout - an optional board layout to pass in to define the layout
        of the game board

    Returns: NA

    Initializes the GameState object, either by creating a new one from
    scratch or by cloning an optionally passed-in other GameState object.
    Can also optionally define the board layout if you are creating a new
    GameState object from scratch.
    ------------------------------
    """
    
    self.board = Board()
    self.playerAgents = [PlayerAgent("yera", 0), PlayerAgent("krati", 1), PlayerAgent("juan", 2), PlayerAgent("isi", 3)]

    # Make the dice agent
    self.diceAgent = DiceAgent()

  def deepCopy(self):
    copy = GameState()
    copy.board = self.board.deepCopy()
    copy.playerAgents = [playerAgent.deepCopy(copy.board) for playerAgent in self.playerAgents]
    return copy


  def getLegalActions(self, agentIndex):
    """
    Method: getLegalActions
    ------------------------------
    Parameters:
      agentIndex - the index of the agent to return legal actions for

    Returns: a list of action tuples (ACTION, LOCATION) (e.g. (ACTIONS.SETTLE, *some Tile object*))
      representing all the valid actions that the given agent/player can take
    ------------------------------
    """
    legalActions = set()
    if self.gameOver() >= 0: return legalActions
    agent = self.playerAgents[agentIndex]

    # If they can build a road...
    if agent.canBuildRoad():
      # Look at all unoccupied edges coming from the player's existing settlements and cities
      agentSettlements = []; agentSettlements.extend(agent.settlements); agentSettlements.extend(agent.cities)
      for settlement in agentSettlements:
        tiles = self.board.getUnoccupiedNeighbors(settlement, diagonals=False)
        for tile in tiles:
            if not tile.isOccupied(): 
              if (Actions["ROAD"], tile) not in legalActions:
                legalActions.add((Actions["ROAD"], tile)) 

      # Look at all unoccupied edges coming from the player's existing roads
      for road in agent.roads:
        tiles = self.board.getUnoccupiedRoadEndpoints(road)
        for tile in tiles:
            if not tile.isOccupied(): 
              if (Actions["ROAD"], tile) not in legalActions:
                legalActions.add((Actions["ROAD"], tile)) 

    # If they can settle...
    if agent.canSettle():
      # Look at all unoccupied endpoints of the player's existing roads
      for road in agent.roads:
        tiles = self.board.getUnoccupiedRoadEndpoints(road)
        for tile in tiles:
          if not tile.isOccupied() and self.board.isValidSettlementLocation(tile): 
            if (Actions["SETTLE"], tile) not in legalActions:
              legalActions.add((Actions["SETTLE"], tile))

    # If they can build a city...
    if agent.canBuildCity():
      # All current settlements are valid city locations
      for settlement in agent.settlements:
        legalActions.add((Actions["CITY"], settlement))
    return list(legalActions)

  def generateSuccessor(self, playerIndex, action):
    """
    Method: generateSuccessor
    ----------------------------
    Parameters:
      playerIndex - the number of the player that is about to take an action
      action - the action that the player is about to take

    Returns: a new GameState object with playerIndex having taken 'action'

    Creates a clone of the current game state, and then performs the
    given action on behalf of the given player.  Returns the resulting
    GameState object.
    ----------------------------
    """
    if self.gameOver() >= 0:
      raise Exception("Can\'t generate a successor of a terminal state!")

    # Create a copy of the current state, and perform the given action
    # for the given player
    copy = self.deepCopy()
    copy.playerAgents[playerIndex].applyAction(action, copy.board)
    copy.board.applyAction(playerIndex, action)
    return copy

  def makeMove(self, playerIndex, action):
    """
    Method: makeMove
    ----------------------------
    Parameters:
      playerIndex - the number of the player that is about to take an action
      action - the action that the player is about to take

    Modifies the current game state to reflect the action that is passed in
    ----------------------------
    """
    self.playerAgents[playerIndex].applyAction(action, self.board)
    self.board.applyAction(playerIndex, action)

  def getNumPlayerAgents(self):
    """
    Method: getNumPlayerAgents
    ----------------------------
    Parameters: NA
    Returns: the number of PLAYER agents (players) in the game
    ----------------------------
    """
    return len(self.playerAgents)

  def gameOver(self):
    """
    Method: gameOver
    ----------------------------
    Parameters: NA
    Returns: the index of the player that has won, or -1 if the game has not ended
    ----------------------------
    """
    # See if any of the agents have won
    for agent in self.playerAgents:
      if agent.hasWon():
        return agent.agentIndex
    return -1

  def updatePlayerResourcesForDiceRoll(self, diceRoll):
    """
    Method: updatePlayerResourcesForDiceRoll
    -----------------------------------------
    Parameters:
      diceRoll - the dice total of the 2 rolled 6-sided dice
        to use to distribute more resources
    Returns: NA

    Updates the resource counts of all agents based on the
    given dice roll.
    -----------------------------------------
    """
    someone_received = False
    for agent in self.playerAgents:
      gainedResources = agent.updateResources(diceRoll, self.board)
      if VERBOSE:
        if gainedResources != Counter():
          print(str(agent.name) + " received: " + str(gainedResources))
          print(str(agent.name) + " now has: " + str(agent.resources))
          someone_received = True
    if VERBOSE:
      if not someone_received:
        print("No one received resources this turn")


class Game:
  """
  Class: Game
  ------------------------
  Represents all information about a game, and controls game flow.
  In addition to containing a GameState object to keep track of all game
  state, a Game object also contains the game's move history as a list
  of (AGENTNAME, ACTION) tuples.
  ------------------------
  """

  def __init__(self, playerAgentNums = None):
    """
    Method: __init__
    ----------------------
    Parameters:
      gameState - an optional pre-defined GameState object to use for the game.
        If one isn't passed in, the Game begins with a newly-created GameState object.

    Returns: NA

    Initializes the Game object by initializing the move history list
    and the internal GameState object.
    ----------------------
    """
    self.moveHistory = []
    self.gameState = GameState()
    self.playerAgentNums = playerAgentNums 

  def start(self):
    """
    Method: start
    ----------------------
    Parameters: NA
    Returns: NAz

    Begins the game by running the main game loop.
    ----------------------
    """
    # Welcome message
    if VERBOSE:
      print("WELCOME TO SETTLERS OF CATAN!")
      print("-----------------------------")

    # Turn tracking
    turnNumber = 1
    currentAgentIndex = 0

    # Each player has to place 1 settlements and 1 roads
    for i in range(NUM_INITIAL_SETTLEMENTS):
      for agentIndex in range(self.gameState.getNumPlayerAgents()):
        currentAgent = self.gameState.playerAgents[agentIndex]
        legalActions = self.gameState.getLegalActions(agentIndex)

        if VERBOSE:
          print("---------- TURN " + str(turnNumber) + " --------------")
          print("It's " + str(currentAgent.name) + "'s turn!. Where do you want to place your settlement? \n")
          self.gameState.board.printBoard()
        
        x = input("Enter x: ")
        y = input("Enter y: ")
        action = (Actions["SETTLE"], self.gameState.board.getTile(int(x), int(y)))

        self.gameState.board.applyAction(agentIndex, action)
        currentAgent.settlements.append(action[1])
        self.moveHistory.append((currentAgent.name, action))

        if VERBOSE:
          print("Where do you want to place your road?")
          self.gameState.board.printBoard()
        
        x = input("Enter x: ")
        y = input("Enter y: ")
        action = (Actions["ROAD"], self.gameState.board.getTile(int(x), int(y)))

        self.gameState.board.applyAction(agentIndex, action)
        currentAgent.roads.append(action[1])
        self.moveHistory.append((currentAgent.name, action))

        currentAgentIndex = (currentAgentIndex+1) % self.gameState.getNumPlayerAgents()
        turnNumber += 1

      for agentIndex in range(self.gameState.getNumPlayerAgents()):
        currentAgent.collectInitialResources(self.gameState.board)

        if VERBOSE:
          currentAgent.printresources()

    while (self.gameState.gameOver() < 0):
      # Initial information
      currentAgent = self.gameState.playerAgents[currentAgentIndex]
      if VERBOSE:
        print("---------- TURN " + str(turnNumber) + " --------------")
        print("It's " + str(currentAgent.name) + "'s turn!")

      # Print player info
      if not VERBOSE:
        self.gameState.board.printBoard()
        print("PLAYER INFO:")
        for a in self.gameState.playerAgents:
          print(a)

      # Dice roll + resource distribution
      diceRoll = self.gameState.diceAgent.rollDice()
      if VERBOSE: print("Rolled a " + str(diceRoll))
      self.gameState.updatePlayerResourcesForDiceRoll(diceRoll)

      # Print player info
      if VERBOSE:
        print("PLAYER INFO:")
        print(currentAgent)

      # The current player performs 1 action, input the action from the list of legal actions
      legalActions = self.gameState.getLegalActions(currentAgentIndex)

      if VERBOSE:
        print("LEGAL ACTIONS:")
        for action in legalActions:
          print(action)

      if len(legalActions) == 0:
        if VERBOSE:
          print("No legal actions for " + str(currentAgent.name) + ". Skipping turn.")
          
        currentAgentIndex = (currentAgentIndex+1) % self.gameState.getNumPlayerAgents()
        turnNumber += 1
        continue

      self.gameState.board.printBoard()

      a = input("Enter your action: \n 'SETTLE': 1 \n 'CITY': 2 \n 'ROAD': 3 \n 'TRADE': 4 \n")
      x = input("Enter x: ")
      y = input("Enter y: ")

      action = [a, self.gameState.board.getTile(int(x), int(y))]
      currentAgent.applyAction(action, self.gameState.board)
    
      if VERBOSE:# Print out the updated game state
          print(str(currentAgent.name) + " took action " + str(action[0]) + " at " + str(action[1]) + "\n")

      # Track the game's move history
      self.moveHistory.append((currentAgent.name, action))
      # Go to the next player/turn
      currentAgentIndex = (currentAgentIndex+1) % self.gameState.getNumPlayerAgents()
      turnNumber += 1

      # Caps the total number of iterations for a game
      if turnNumber > CUTOFF_TURNS: break

    winner = self.gameState.gameOver()
    if winner < 0: return (winner, turnNumber, -1)
    agentWinner = self.gameState.playerAgents[winner]
    agentLoser = self.gameState.playerAgents[1-winner]
    if VERBOSE: print(agentWinner.name + " won the game")
    return (winner, turnNumber, agentWinner.victoryPoints - agentLoser.victoryPoints)
  
Game().start()
    