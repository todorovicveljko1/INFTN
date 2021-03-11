import requests

_game = None
_gameId = None
_playerIndex = None
_playerId = None
url = 'http://localhost:8080'

def get(url):
  r = requests.get(url)
  res = r.json()
  return res

def test_game(_playerId):
    


print("Enter player ID:")
_playerId = input()
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