from world import World, Tile, getMoveAction
from agent import Agent, movesCompression
import json


f = open("./map.json","r")
bot = Agent(json.load(f))
f.close()
mat = bot.moveToNextFreeTilePriority()
print(mat)
#for i in range(len(mat)):
#    for j in range(len(mat[i])):
#        if i%2 == 1 and j == 0:
 #           print("   ",end="")
 #       print("{:4}".format(mat[i][j]), end="  ")
 #   print()





#path = bot.world.AStar((1,11),(6,15))
#prev = path[0]
#for p in path[1:]:
#    print(getMoveAction(prev,p), end="->")
 #   prev = p
"""

for i in range(len(mat)):
    for j in range(len(mat[i])):
        if i%2 == 1 and j == 0:
            print("   ",end="")
        print("{:4}".format(mat[i][j]), end="  ")
    print()




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