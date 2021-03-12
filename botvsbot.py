# 540495


import requests
from agent import Agent
import time

_agent = None
_agent = None
_gameId = None
_testing = False
_playerId = 540495
_playerId1 = 540496
url = 'https://aibg2021.herokuapp.com'

def get(url):
  r = requests.get(url)
  res = r.json()
  return res

def test_game():
    global _agent, _agent1 , _gameId, _playerId, _playerId1
    res = get(url + '/botVSbot?player1Id=' + str(_playerId) + "&player2Id="+str(_playerId1))
    #print(res)
    _gameId = res.get('gameId')
    print("Game id: " + str(_gameId))

    _agent = Agent(res)
    
    #print(res)
    _agent1 = Agent(res)
    _agent1.me, _agent1.enemy = _agent1.enemy, _agent1.me
    


def run():
    global _agent, _agent1, _playerId1 , _playerId, _gameId

    action = _agent.nextAction()
    print(action)
    # After we send an action - we wait for response
    res = do_action(_playerId, _gameId, action[0], action[1])
    # Other player made their move - we send our move again
    if res.get('message') == "Game is finished" or res.get('finished'):
        return;
    _agent.update(res)

    time.sleep(1)
    
    action = _agent1.nextAction()
    print(action)
    # After we send an action - we wait for response
    res = do_action(_playerId1, _gameId, action[0], action[1])
    print(res)
    if res.get('message') == "Game is finished" or res.get('finished'):
        return;
    
    # Other player made their move - we send our move again
    _agent1.update(res)
    time.sleep(1)
    run()
  

def do_action(playerId, gameId, action, queryDict):
    queryStr = url+"/"+action+"?playerId=" + str(playerId) + "&gameId=" + str(gameId)
    if queryDict is not None:
        for key in queryDict:
            queryStr += ("&" + str(key) + "=" + str(queryDict[key]))
    return get(queryStr)
#print("Enter player ID:")
#_playerId = input()

test_game()
run()
