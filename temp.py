def createDTreeModel(self):
        return select((
            sequence((
                condition(self.world.isThereFreeASpot),
                action(self.getClosestFreeASpot),
            )),
            sequence((
                condition(self.world)
            ))
            action(self.moveToNextFreeTile)
        ))

def imRobbed(self):
    return self.enemy.executedAction == "stealKoalas" and self.me.energy >= 5 and self.me.energy > self.enemy.energy


def shouldSkip(self):
    neighbors = self.world.getNeighbors(self.me.position)
    flag = False

    if len(neighbors) == 1:
        neighofneigh = self.world.getNeighbors(neighbors[0].position)
        if len(neighofneigh) == 1:
            flag = True

    if self.me.numOfSkipATurnUsed < 2:
        if flag == True  and len(self.world.koalaCrew)== 0:
            if self.freeSpots <= 20:
                return True
    
    return False

def skipAction(self):
    self.ACTION = "skipATurn"
    self.QUERY_DATA = None
         
        