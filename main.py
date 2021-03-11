# 540495


import requests

_game = None
_gameId = None
_playerIndex = None
_playerId = 540495
url = 'https://aibg2021.herokuapp.com'

def get(url):
  r = requests.get(url)
  res = r.json()
  return res

def test_game(playerId):
    global _game, _gameId, _playerIndex
    res = get(url + '/train/makeGame?playerId=' + str(playerId))
    print(res)
    # _game = res['result']
    # _gameId = _game['id']
    # print("Game id: " + str(_gameId))
    # _playerIndex = res['playerIndex']
    return res

def join(_playerId, _gameId):
    pass

def do_action(playerId, gameId, test, action, queryDict):
    queryStr = "?playerId=" + str(playerId) + "&gameId=" + str(gameId)
    for key,value in queryDict:
        queryStr += ("&" + str(key) + "=" + str(value))
    


#print("Enter player ID:")
#_playerId = input()
print("Enter command:")
command = input()
if command == 'test':
  print(_playerId)
  test_game(_playerId)
  run()
elif command == 'join':
  print("Enter game id:")
  _gameId = input()
  join(_playerId, _gameId)
  run()