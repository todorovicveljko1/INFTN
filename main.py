# 540495


import requests
from agent import Agent
import time

_agent = None
_gameId = None
_playerIndex = None
_playerId = 540495
url = 'https://aibg2021.herokuapp.com'

def get(url):
  r = requests.get(url)
  res = r.json()
  return res

def test_game(playerId):
    global _agent, _gameId, _playerIndex
    res = get(url + '/train/makeGame?playerId=' + str(playerId))
    #print(res)
    _agent = Agent(res)
    _gameId = res.get('gameId')
    print("Game id: " + str(_gameId))
    # _playerIndex = res['playerIndex']

def join(_playerId, _gameId):
    pass

def run():
    global _agent, _playerIndex, _playerId, _gameId

    action = _agent.nextAction()
    print(action)
    # After we send an action - we wait for response
    res = do_action(_playerId, _gameId, True, action[0], action[1])
    # Other player made their move - we send our move again
    _agent.update(res)
    if res.get('message') == "Game is finished" or res.get('finished'):
        return;
    run()
  

def do_action(playerId, gameId, test, action, queryDict):
    queryStr = url+"/train/"+action+"?playerId=" + str(playerId) + "&gameId=" + str(gameId)
    if queryDict is not None:
        for key in queryDict:
            queryStr += ("&" + str(key) + "=" + str(queryDict[key]))
    return get(queryStr)
#print("Enter player ID:")
#_playerId = input()
print("Enter command:")
command = input()
if command == 'test':
  #print(_playerId)
  test_game(_playerId)
  run()
elif command == 'join':
  print("Enter game id:")
  _gameId = input()
  join(_playerId, _gameId)
  run()