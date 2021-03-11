from world import World, getMoveAction
from BTree import select, FAILURE,  sequence, action, condition, not_, failer, actionWithProps, conditionWithProps

class PlayerStats:
    def __init__(self, playerData, key):
        self.key = key
        self.x = playerData.get('x')
        self.y = playerData.get('y')
        self.score = playerData.get('score')
        self.gatheredKoalas = playerData.get('gatheredKoalas')
        self.energy = playerData.get('energy')
        self.hasFreeASpot = playerData.get('hasFreeASpot')
        self.numberOfUsedFreeASpot = playerData.get('numberOfUsedFreeASpot')
        self.numOfSkipATurnUsed = playerData.get('numOfSkipATurnUsed')
        self.executedAction = playerData.get('executedAction')
        self.teamName = playerData.get('teamName')
    def update(self, playerData):
        self.x = playerData.get('x')
        self.y = playerData.get('y')
        self.score = playerData.get('score')
        self.gatheredKoalas = playerData.get('gatheredKoalas')
        self.energy = playerData.get('energy')
        self.hasFreeASpot = playerData.get('hasFreeASpot')
        self.numberOfUsedFreeASpot = playerData.get('numberOfUsedFreeASpot')
        self.numOfSkipATurnUsed = playerData.get('numOfSkipATurnUsed')
        self.executedAction = playerData.get('executedAction')
    @property
    def position(self):
        return (self.y, self.x)

class Agent:
    def __init__(self, gameJson):
        self.world = World(gameJson.get("map"))
        self.me = None
        self.enemy = None
        for key in gameJson.keys():
            if "player" in key and "Changed" not in key :
                # print(gameJson.get(key))
                if gameJson.get(key).get('teamName') != "INFTN":
                    self.enemy = PlayerStats(gameJson.get(key), key)
                else:
                    self.me = PlayerStats(gameJson.get(key), key)

        self.decisionTreeModel =self.createDTreeModel()
        self.ACTION = None
        
    def createDTreeModel(self):
        return select((
            action(self.getClosestFreeASpot),
        ))

    def getClosestFreeASpot(self):
        closestPath = None
        minDist = 100
        minTile = None
        for tile in self.world.freeASpot:
            path = self.world.AStar(self.me.position, tile.position)
            if path is not None:
                if minDist > len(path):
                    minDist = len(path)
                    closestPath = path
                    minTile = tile
        if closestPath is None or len(closestPath) < 2: 
            return FAILURE
        self.ACTION = "move"
        self.QUERY_DATA = {"direction": getMoveAction(closestPath[0], closestPath[1]), "distance":"1" }
        

    def update(self, gameJson):
        for key in gameJson.keys():
            if "Changed" in key:
                self.world.updateTiles(gameJson.get(key))
        self.me.update(gameJson.get(self.me.key))
        self.enemy.update(gameJson.get(self.enemy.key))
        


    def nextAction(self):
        self.decisionTreeModel.blackboard().tick()
        return (self.ACTION,self.QUERY_DATA)
    