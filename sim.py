from world import World
import json


f = open("./map.json","r")
w = World(json.load(f).get("map"))
f.close()
neighbors = w.getNeighbors((3,2))

for neighbor in neighbors:
    print(neighbor.x,neighbor.y,neighbor.itemType)

