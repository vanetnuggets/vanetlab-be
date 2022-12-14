from test import Test

tests = []
try:
  tests = [
    Test('./jsons/json_vojto.json', 'csma, udp'),
    Test('./jsons/json_wifi.json', 'wifi'),
    Test('./jsons/json_samo.json', 'helper')
  ]
except:
  print('[!] Please run this from ./tests directory.')

ok = 0
failed = 0

for test in tests:
  err = test.all(False)
  if err:
    failed += 1
  else:
    ok += 1
print('\nTest summary:')
print('  - Tests passed:', ok)
print('  - Tests failed:', failed)