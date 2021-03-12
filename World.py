 
ROWS = 27
COLS = 9

def getDistance2(tileA, tileB):
    
    if tileA.x == tileB.x and tileA.y % 2 == tileB.y %2:
        return abs(tileA.y - tileB.y)/2

    if tileA.y == tileB.y:
        return 2*abs(tileA.x - tileB.y)
    
    distX = abs(tileA.x - tileB.x)
    distY = abs(tileA.y - tileB.y)
    return distX + distY

def getDistance(tileA, tileB):


    distX = abs(tileA.x - tileB.x)
    distY = abs(tileA.y - tileB.y)
    return distX + distY

def reTracePath(start_tile, end_tile):
    path = []
    current_tile = end_tile

    while current_tile != start_tile:
        path.append(current_tile)
        current_tile = current_tile.parent
    path.append(start_tile)  # I Pocetno polje
    return path[::-1]

def getMoveAction(tile1, tile2):
    difX = tile2.y - tile1.y
    difY = tile2.x - tile1.x


    if difY == 2:    #(x, y+2) -> dole
        return 's'
    if difY == -2:   #(x, y-2) -> gore  
        return 'w'
        
    if tile1.x % 2 == 0:
        if difX == 0 and difY == -1: #(x, y-1) -> gore desno
            return 'e'
        if difX == 0 and difY == 1: #(x, y+1) -> dole desno
            return 'd'
        if difX == -1 and difY == -1: #(x-1, y-1) -> gore levo
            return 'q'
        if difX == -1 and difY == 1: #(x-1, y+1) -> dole levo
            return 'a'
    else:
        if difX == 1 and difY == -1: #(x+1, y-1) -> gore desno
            return 'e'
        if difX == 0 and difY == -1: #(x, y-1) -> gore levo
            return 'q'
        if difX == 1 and difY == 1: #(x+1, y+1) -> dole desno
            return 'd'
        if difX == 0 and difY == 1: #(x, y+1) -> dole levo
            return 'a'


class FloodFillTileInfo():
    def __init__(self):
        self.dist = -1
        self.poss = None
        self.path = list()
 

class Tile:
    def __init__(self, tileData):
        self.row = tileData.get("row")
        self.column = tileData.get("column")
        self.ownedByTeam = tileData.get("ownedByTeam")
        self.itemType =  tileData.get("tileContent").get("itemType")
        self.numOfItems = tileData.get("tileContent").get("numOfItems")

        self.parent = None
        self.gCost = 0  # Distance to start node
        self.hCost = 0  # Distance to goal node
    def update(self, tileData):
        self.ownedByTeam = tileData.get("ownedByTeam")
        self.itemType =  tileData.get("tileContent").get("itemType")
        self.numOfItems = tileData.get("tileContent").get("numOfItems")
        
    @property
    def fCost(self):
        return self.gCost + self.hCost
    
    @property
    def position(self):
        return (self.column, self.row)
    @property
    def x(self):
        return self.row
    @property
    def y(self): 
        return self.column

    @property
    def walkable(self):
        return self.ownedByTeam == "" and self.itemType != "HOLE"

    def __repr__(self):
        return ('({0},{1}), {2}'.format(self.y, self.x, self.itemType))

class World:
    def __init__(self, map):
        rows = map.get('tiles')
        self.tiles = [[
            Tile(
                tile
            ) for tile in row 
        ] for row in rows]
        self.freeASpot = []
        for row in self.tiles:
            for tile in row:
                if tile.itemType == "FREE_A_SPOT":
                    self.freeASpot.append(tile)
        # TILES (27, 9)
    def update(self, map):
        rows = map.get('tiles')
        self.tiles = [[
            Tile(
                tile
            ) for tile in row 
        ] for row in rows]
        self.freeASpot = []
        for row in self.tiles:
            for tile in row:
                if tile.itemType == "FREE_A_SPOT":
                    self.freeASpot.append(tile)

    def isThereFreeASpot(self):
        return len(self.freeASpot) > 0

    def getNeighbors(self, position: (int, int)): # POSITION (Y, X)
        neighbors = list()
        if position[1]%2 == 1:
            if position[1] > 0:
                neighbors.append(self.tiles[position[1]-1][position[0]])      # Gore Levo -> q
            if position[1] > 1:
                neighbors.append(self.tiles[position[1]-2][position[0]])      # Gore -> w
            if position[1] > 0 and position[0] < 9:
                neighbors.append(self.tiles[position[1]-1][position[0]+1])      # Gore Desno -> e 
            if position[1] < 26 and position[0] < 9:
                neighbors.append(self.tiles[position[1]+1][position[0]+1])      # Dole Desno -> d 
            if position[1] < 25:
                neighbors.append(self.tiles[position[1]+2][position[0]])      # Dole -> s
            if position[1] < 26:
                neighbors.append(self.tiles[position[1]+1][position[0]])      # Dole levo -> a
        else:
            if position[1] > 0 and position[0] >0:
                neighbors.append(self.tiles[position[1]-1][position[0]-1])
            if position[1] > 1:    # Gore Levo -> q
                neighbors.append(self.tiles[position[1]-2][position[0]])      # Gore -> w
            if position[1] > 0:
                neighbors.append(self.tiles[position[1]-1][position[0]])      # Gore Desno -> e 
            if position[1] < 26:
                neighbors.append(self.tiles[position[1]+1][position[0]])      # Dole Desno -> d 
            if position[1] < 25:
                neighbors.append(self.tiles[position[1]+2][position[0]])      # Dole -> s
            if position[1] < 26:
                neighbors.append(self.tiles[position[1]+1][position[0]-1])      # Dole levo -> a

        return neighbors

    def getTile(self, position: (int, int)):
        return self.tiles[position[1]][position[0]]

    def checkNextFreeTile(self, position: (int, int)):
        tile = self.getTile(position)
        neigh = self.getNeighbors(position)

        for t in neigh:
            if t.walkable:
                return getMoveAction(tile, t)
    
    def AStar(self, startPos, endPos):

        start_tile = self.getTile(startPos)
        goal_tile = self.getTile(endPos)
        open_list = set()
        open_list.add(start_tile)
        closed_list = set()
        while len(open_list) > 0:
            current_tile = min(open_list, key = lambda tile: tile.fCost )
            #for tile in open_list[1:]:
            #    if tile.fCost < current_tile.fCost or (tile.fCost == current_tile.fCost and tile.hCost < current_tile.hCost):
            #        current_tile = tile

            open_list.remove(current_tile)
            closed_list.add(current_tile)
            if current_tile == goal_tile:
                # print("neigbor checked {0}".format(numb))
                return reTracePath(start_tile, goal_tile)

            for neigbor in self.getNeighbors(current_tile.position):

                if not neigbor.walkable or neigbor in closed_list:
                    continue
                newMovementCostToNeigbor = current_tile.gCost + \
                    getDistance(current_tile, neigbor)
                if newMovementCostToNeigbor < neigbor.gCost or not neigbor in open_list:
                    # numb+=1
                    neigbor.gCost = newMovementCostToNeigbor
                    neigbor.hCost = getDistance(goal_tile, neigbor)
                    neigbor.parent = current_tile
                    if not neigbor in open_list:

                        open_list.add(neigbor)
        return None

    def floodFill(self, position, depth=-1, accessTileCount = False):
        if depth == -1:
            depth = 100
        queue = set()
        mat = [[-1 for i in range(10)] for j in range(28)]
        mat[position[1]][position[0]] = 0
        count = 0
        queue.add(self.getTile(position))
        while len(queue) > 0:
            current_tile = queue.pop()
            for neigbor in self.getNeighbors(current_tile.position):
                if (mat[neigbor.x][neigbor.y] == -1 or mat[neigbor.x][neigbor.y] > mat[current_tile.x][current_tile.y] + 1) and neigbor.walkable:
                    mat[neigbor.x][neigbor.y] = mat[current_tile.x][current_tile.y] + 1
                    count+=1
                    if mat[neigbor.x][neigbor.y] == depth:
                        continue
                    queue.add(neigbor)
        if accessTileCount:
            return count
        return mat

    def checkNextFreeTilePriority(self, position: (int, int)):
        center = self.getTile(position)
        neighbors = self.getNeighbors(position)
        bestTileForMove = None
        bestTileExposure = -1
        prevItemType = center.itemType
        center.itemType = "HOLE"
        for tile in neighbors:
            if tile.walkable:
                temp = self.floodFill(tile.position, accessTileCount = True)
                if temp > bestTileExposure:
                    bestTileExposure = temp
                    bestTileForMove = tile
        center.itemType = prevItemType
        if bestTileExposure == -1:
            return None
        return getMoveAction(center, bestTileForMove)

               
    """
    def floodFillFindTiles(self, position, tilesPos, findCount=-1, depth=-1):
        if len(tilesPos) == 0:
            return []
        if depth == -1:
            depth = 2*ROWS
        if findCount == -1:
            findCount = len(tilesPos)
        queue = set()
        mat = [[FloodFillTileInfo() for i in range(10)] for j in range(28)]
        mat[position[1]][position[0]].dist = 0
        mat[position[1]][position[0]].poss = position
        found = 0
        queue.add(self.getTile(position))
        while len(queue) > 0:
            current_tile = queue.pop()
            for neigbor in self.getNeighbors(current_tile.position):
                if (mat[neigbor.x][neigbor.y].dist == -1 or mat[neigbor.x][neigbor.y].dist > mat[current_tile.x][current_tile.y].dist + 1) and neigbor.walkable:
                    mat[neigbor.x][neigbor.y].dist = mat[current_tile.x][current_tile.y].dist + 1
                    mat[neigbor.x][neigbor.y].poss = neigbor.position
                    mat[neigbor.x][neigbor.y].path = mat[current_tile.x][current_tile.y].path.copy()
                    mat[neigbor.x][neigbor.y].path.append(current_tile.position)
                    if neigbor.position in tilesPos:
                        found += 1
                        if found == findCount + 1:
                            out = list()
                            for tile in tilesPos:
                                if mat[tile[1]][tile[0]].dist != -1:
                                    mat[tile[1]][tile[0]].path.append(tile) # Add last tile
                                    out.append(mat[tile[1]][tile[0]])
                            return out
                    if mat[neigbor.x][neigbor.y].dist == depth:
                        continue
                    queue.add(neigbor)
        out = list()
        for tile in tilesPos:
            print(tile)
            if mat[tile[0]][tile[1]].dist != -1:
                mat[tile[0]][tile[1]].path.append(tile) # Add last tile
                out.append(mat[tile[0]][tile[1]])
        return out
    """