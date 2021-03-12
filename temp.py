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