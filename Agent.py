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
        self.numOfMove = 0
        self.me = None
        self.enemy = None
        for key in gameJson.keys():
            if "player" in key and "Changed" not in key :
                # print(gameJson.get(key))
                if gameJson.get(key).get('teamName') != "INFTN" or self.me is not None:
                    self.enemy = PlayerStats(gameJson.get(key), key)
                else:
                    self.me = PlayerStats(gameJson.get(key), key)

        self.decisionTreeModel =self.createDTreeModel()
        self.ACTION = None
        self.QUERY_DATA = None

    def createDTreeModel(self):
        return select((
            sequence((
                condition(self.canStealMore), # canSteal
                action(self.steal),
            )),
            sequence((
                conditionWithProps(self.lastThanTurns, 30), 
                condition(self.shouldNotMove),
                action(self.noMoveAction),
            )),
            sequence((
                condition(self.isTurnGreaterThen40),
                condition(self.world.isTurnKoalaCrew),
                actionWithProps(self.getClosestTiles, self.world.koalaCrew, False),
            )),
            sequence((
                condition(self.world.isThereFreeASpot),
                actionWithProps(self.getClosestTiles, self.world.freeASpot, False),
            )),
            sequence((
                conditionWithProps(self.lastThanTurns, 12), 
                condition(self.shouldSkip), #shouldSkip
                action(self.skipAction),
            )),
            action(self.moveToNextFreeTilePriority2)
        ))
    def moveToNextFreeTilePriority2(self):
        direction = self.world.checkNextFreeTilePriority2(self.me.position)
        self.ACTION = "move"
        self.QUERY_DATA = {"direction": direction, "distance":1 }

    def moveToNextFreeTilePriority(self):
        direction = self.world.checkNextFreeTilePriority(self.me.position)
        self.ACTION = "move"
        self.QUERY_DATA = {"direction": direction, "distance":1 }

    def moveToNextFreeTile(self):
        direction = self.world.checkNextFreeTile(self.me.position)
        self.ACTION = "move"
        self.QUERY_DATA = {"direction": direction, "distance":1 }

    def getClosestTiles(self, tiles, useJumps = True):
        closestPath = None
        minDist = 100
        minTile = None
        for tile in tiles:
            path = self.world.AStar(self.me.position, tile.position)
            if path is not None:
                if minDist > len(path):
                    minDist = len(path)
                    closestPath = path
                    minTile = tile
        #print(closestPath)
        #print(self.me.position)
        if closestPath is None or len(closestPath) < 2: 
            return FAILURE
        moves = []
        prev = closestPath[0]
        for tile in closestPath[1:]:
            moves.append(getMoveAction(prev, tile))    
            prev = tile
        if useJumps:
            moves = movesCompression(moves)
            direction =  moves[0][0]
            distance = moves[0][1] if self.me.energy >= moves[0][1] else self.me.energy
            self.ACTION = "move"
            self.QUERY_DATA = {"direction": direction, "distance":distance }
        else:
            self.ACTION = "move"
            self.QUERY_DATA = {"direction": moves[0][0], "distance":1 }


    def getClosestFreeASpot(self):
        self.getClosestTiles(self.world.freeASpot)
    #koalaCrew
    def getClosestKoalaCrew(self):
        self.getClosestTiles(self.world.koalaCrew)

    def isTurnGreaterThen40(self):
        return self.numOfMove >= 40

    def steal(self):
        self.ACTION = "stealKoalas"
        self.QUERY_DATA = None

    def update(self, gameJson):
        if gameJson == None:
            return
        self.numOfMove = gameJson.get("numOfMove")
        self.world.update(gameJson.get("map"))
        self.me.update(gameJson.get(self.me.key))
        self.enemy.update(gameJson.get(self.enemy.key))
        


    def nextAction(self):
        self.decisionTreeModel.blackboard().tick()
        return (self.ACTION, self.QUERY_DATA)
    """ OLD
    def canSteal(self):
        return self.me.energy >= 5 and self.enemy.energy < 5 and self.isNeighbor(self.enemy.position) 
    """
    def canStealMore(self):
        return (self.me.energy - self.enemy.energy) >= 1 and self.isNeighbor(self.enemy.position) and self.enemy.gatheredKoalas > 1
    def isNeighbor(self, position):
        neigh = self.world.getNeighbors(self.me.position)
        enemyTile = self.world.getTile(position)
        flag = False

        if enemyTile in neigh:
            flag = True

        return flag
    
    def lastThanTurns(self, turns):
        return self.world.freeSpots <= turns

    def shouldSkip(self): 
        neighbors = self.world.getNeighbors(self.me.position)
        flag = False
        countWalkable = 0
        countWalkable1 = 0
        walkableNeighbors = []
        for n in neighbors:
            if n.walkable:
                walkableNeighbors.append(n)  
        if len(walkableNeighbors) == 1:
            neighofneigh = self.world.getNeighbors(walkableNeighbors[0].position)
            for n in neighofneigh:
                if n.walkable:
                    countWalkable += 1  
            if countWalkable == 0:
                flag = True

        elif len(walkableNeighbors) == 2:
            countWalkable = 0
            countWalkable1 = 0
            neighofneigh1 = self.world.getNeighbors(walkableNeighbors[0].position)
            for n in neighofneigh1:
                if n.walkable:
                    countWalkable += 1 
            neighofneigh2 = self.world.getNeighbors(walkableNeighbors[1].position)
            for n in neighofneigh2:
                if n.walkable:
                    countWalkable1 += 1 
            if countWalkable == 0 and countWalkable1 == 0:
                flag = True

        if self.me.numOfSkipATurnUsed < 5 and (self.me.energy < self.enemy.energy or self.me.score > self.enemy.score): 
            if flag == True  and len(self.world.koalaCrew) == 0:
                return True
        
        return False

    def skipAction(self):
        self.ACTION = "skipATurn"
        self.QUERY_DATA = None

    def shouldNotMove(self):
        neighbors = self.world.getNeighbors(self.me.position)
        flag = False
        countWalkable = 0
        countWalkable1 = 0
        walkableNeighbors = []
        for n in neighbors:
            if n.walkable:
                walkableNeighbors.append(n)  
        if len(walkableNeighbors) == 1:
            neighofneigh = self.world.getNeighbors(walkableNeighbors[0].position)
            for n in neighofneigh:
                if n.walkable:
                    countWalkable += 1  
            if countWalkable == 0:
                flag = True

        elif len(walkableNeighbors) == 2:
            countWalkable = 0
            countWalkable1 = 0
            neighofneigh1 = self.world.getNeighbors(walkableNeighbors[0].position)
            for n in neighofneigh1:
                if n.walkable:
                    countWalkable += 1 
            neighofneigh2 = self.world.getNeighbors(walkableNeighbors[1].position)
            for n in neighofneigh2:
                if n.walkable:
                    countWalkable1 += 1 
            if countWalkable == 0 and countWalkable1 == 0:
                flag = True
        
        if self.me.energy*100 + self.me.score > self.enemy.score + self.enemy.energy*100:
            return flag
        return False
    def noMoveAction(self):
        if self.me.numOfSkipATurnUsed < 5:
            self.ACTION = "skipATurn"
            self.QUERY_DATA = None
        else:
            self.ACTION = "move"
            self.QUERY_DATA = {"direction": None, "distance":1 }