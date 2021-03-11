


class Tile:
    def __init__(self, _row, _column, _ownedByTeam, _itemType, _numOfItems):
        self.row = _row
        self.column = _column
        self.ownedByTeam = _ownedByTeam
        self.itemType = _itemType
        self.numOfItems = _numOfItems
    
    @property
    def position(self):
        return (self.column, self.row)
    @property
    def x(self):
        return self.row
    @property
    def y(self): 
        return self.column

ROWS = 27
COLS = 9

class World:
    def __init__(self, map):
        rows = map.get('tiles')
        self.tiles = [[
            Tile(
                tile.get("row"),
                tile.get("column"),
                tile.get("ownedByTeam"),
                tile.get("tileContent").get("itemType"),
                tile.get("tileContent").get("numOfItems")
            ) for tile in row 
        ] for row in rows]
        
    def getNeighbors(self, position: (int, int)): # POSITION (Y, X)
        neighbors = list()
        if position[1]%2 == 1:
            neighbors.append(self.tiles[position[1]-1][position[0]])      # Gore Levo -> q
            neighbors.append(self.tiles[position[1]-2][position[0]])      # Gore -> w
            neighbors.append(self.tiles[position[1]-1][position[0]+1])      # Gore Desno -> e 
            neighbors.append(self.tiles[position[1]+1][position[0]+1])      # Dole Desno -> d 
            neighbors.append(self.tiles[position[1]+2][position[0]])      # Dole -> s
            neighbors.append(self.tiles[position[1]+1][position[0]])      # Dole levo -> a
        else:
            neighbors.append(self.tiles[position[1]-1][position[0]-1])      # Gore Levo -> q
            neighbors.append(self.tiles[position[1]-2][position[0]])      # Gore -> w
            neighbors.append(self.tiles[position[1]-1][position[0]])      # Gore Desno -> e 
            neighbors.append(self.tiles[position[1]+1][position[0]])      # Dole Desno -> d 
            neighbors.append(self.tiles[position[1]+2][position[0]])      # Dole -> s
            neighbors.append(self.tiles[position[1]+1][position[0]-1])      # Dole levo -> a

        return neighbors
