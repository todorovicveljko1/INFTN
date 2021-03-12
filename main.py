# 540495


import requests
from agent import Agent
import time

_agent = None
_gameId = None
_testing = False
_playerId = 540495
url = 'https://aibg2021.herokuapp.com'

def get(url):
  r = requests.get(url)
  res = r.json()
  return res

def test_game(playerId):
    global _agent, _gameId
    res = get(url + '/train/makeGame?playerId=' + str(playerId))
    #print(res)
    _agent = Agent(res)
    _gameId = res.get('gameId')
    print("Game id: " + str(_gameId))

def join(_playerId):
    global _agent, _gameId
    res = get(url + '/train/makeGame?playerId=' + str(playerId))
    #print(res)
    _agent = Agent(res)
    _gameId = res.get('gameId')
    print("Game id: " + str(_gameId))

def run():
    global _agent, _playerId, _gameId

    action = _agent.nextAction()
    print(action)
    # After we send an action - we wait for response
    res = do_action(_playerId, _gameId, action[0], action[1])
    # Other player made their move - we send our move again
    _agent.update(res)
    if res.get('message') == "Game is finished" or res.get('finished'):
        return;
    run()
  

def do_action(playerId, gameId, action, queryDict):
    if _testing:
        queryStr = url+"/train/"+action+"?playerId=" + str(playerId) + "&gameId=" + str(gameId)
    else:
        queryStr = url+"/"+action+"?playerId=" + str(playerId) + "&gameId=" + str(gameId)
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
  _testing = True
  test_game(_playerId)
  run()
elif command == 'join':
  print("Enter game id:")
  _gameId = input()
  join(_playerId)
  run()
