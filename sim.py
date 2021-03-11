from world import World, Tile, getMoveAction
from agent import Agent
import json


f = open("./map.json","r")
bot = Agent(json.load(f))
f.close()

print(bot.world.AStar((1,11),(6,15)))

"""
path = w.AStar((0,0),(7,26))
prev = path[0]

for p in path[1:]:
    print(getMoveAction(prev,p), end="->")
    prev = p

print(getMoveAction(prev,w.getTile))

Move: 
localhost:8080[/train]/move?playerId=567348&gameId=30&direction=d&distance=1

Skip a turn:
localhost:8080[/train]/skipATurn?playerId=567348&gameId=30

Steal Koalas:
localhost:8080[/train]/stealKoalas?playerId=123456&gameId=30

Free a Spot:
localhost:8080[/train]/freeASpot?playerId=567348&gameId=30&&x=2&&y=3







"""