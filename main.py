# 540495


import requests

_game = None
_gameId = None
_playerIndex = None
_playerId = 540495
url = 'http://localhost:8080'

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