import sys, os

print(os.path.dirname(os.path.abspath(f'{__file__}/..')))
sys.path.append(os.path.dirname(os.path.abspath(f'{__file__}/..')))
from app.parser.parser import parser

code = parser.parse('./jsons/second-ns3.json')
print(code)