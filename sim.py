from world import World, Tile, getMoveAction
from agent import Agent
import json


f = open("./map.json","r")
bot = Agent(json.load(f))
f.close()

print(bot.me.teamName)

"""
path = w.AStar((0,0),(7,26))
prev = path[0]

for p in path[1:]:
    print(getMoveAction(prev,p), end="->")
    prev = p

print(getMoveAction(prev,w.getTile))


"""