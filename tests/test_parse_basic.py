import sys, os

print(os.path.dirname(os.path.abspath(f'{__file__}/..')))
sys.path.append(os.path.dirname(os.path.abspath(f'{__file__}/..')))
from app.parser.parser import parser

code = parser.parse('./jsons/second-ns3.json')
for i, x in enumerate(code.split('\n')):
  print(f'{i}: {x}')

with open('parsed_scenario.py', 'w') as f:
  f.write(code)