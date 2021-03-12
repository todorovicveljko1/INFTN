from world import World, getMoveAction
from BTree import select, FAILURE,  sequence, action, condition, not_, failer, actionWithProps, conditionWithProps

def movesCompression(moves):
    if moves is None: return None
    out = [[moves[0], 1]]
    for move in moves[1:]:
        if out[len(out)-1][0] == move:
            out[len(out)-1][1]+=1
        else:
            out.append([move,1])
    return out



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
        self.QUERY_DATA = None

    def createDTreeModel(self):
        return select((
            sequence((
                condition(self.canSteal),
                action(self.steal),
            )),
            sequence((
                condition(self.world.isThereFreeASpot),
                action(self.getClosestFreeASpot),
            )),
            action(self.moveToNextFreeTilePriority)
        ))

    def moveToNextFreeTilePriority(self):
        direction = self.world.checkNextFreeTilePriority(self.me.position)
        self.ACTION = "move"
        self.QUERY_DATA = {"direction": direction, "distance":1 }

    def moveToNextFreeTile(self):
        direction = self.world.checkNextFreeTile(self.me.position)
        self.ACTION = "move"
        self.QUERY_DATA = {"direction": direction, "distance":1 }

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
        moves = []
        prev = closestPath[0]
        for tile in closestPath[1:]:
            moves.append(getMoveAction(prev, tile))    
            prev = tile
        
        moves = movesCompression(moves)
        direction =  moves[0][0]
        distance = moves[0][1] if self.me.energy >= moves[0][1] else self.me.energy
        self.ACTION = "move"
        self.QUERY_DATA = {"direction": direction, "distance":distance }
        
    def steal(self):
        self.ACTION = "stealKoalas"
        self.QUERY_DATA = None

    def update(self, gameJson):
        self.world.update(gameJson.get("map"))
        self.me.update(gameJson.get(self.me.key))
        self.enemy.update(gameJson.get(self.enemy.key))
        


    def nextAction(self):
        self.decisionTreeModel.blackboard().tick()
        return (self.ACTION, self.QUERY_DATA)
    
    def canSteal(self):
        return self.me.energy >= 5 and self.enemy.energy < 5 and self.isNeighbor(self.enemy.position)

    def isNeighbor(self, position):
        neigh = self.world.getNeighbors(self.me.position)
        enemyTile = self.world.getTile(position)
        flag = False

        if enemyTile in neigh:
            flag = True

        return flag
