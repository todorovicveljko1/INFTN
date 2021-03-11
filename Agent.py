from world import World

class PlayerStats:
    def __init__(self, playerData):
        self.x = playerData.get('x'),
        self.y = playerData.get('y')
        self.score = playerData.get('score')
        self.gatheredKoalas = playerData.get('gatheredKoalas')
        self.energy = playerData.get('energy')
        self.hasFreeASpot = playerData.get('hasFreeASpot')
        self.numberOfUsedFreeASpot = playerData.get('numberOfUsedFreeASpot')
        self.numOfSkipATurnUsed = playerData.get('numOfSkipATurnUsed')
        self.executedAction = playerData.get('executedAction')
        self.teamName = playerData.get('teamName')


class Agent:
    def __init__(self, gameJson):
        self.world = World(gameJson.get("map"))
        self.me = None
        self.enemy = None
        for key in gameJson.keys():
            if "player" in key and "Changed" not in key :
                print(gameJson.get(key))
                if gameJson.get(key).get('teamName') != "INFTN":
                    self.enemy = PlayerStats(gameJson.get(key))
                else:
                    self.me = PlayerStats(gameJson.get(key))

    def update(self, res):
        pass

    def nextAction(self):
        return ("move",{"direction":"s","distance":"1"})
    