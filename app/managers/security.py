from collections import Iterable
from functools import wraps
from flask import request, jsonify
import re

reg_scenario = r'[a-zA-Z0-9_\.]*'
reg_uuid = r'[a-zA-Z0-9\-]*'

def flatten(x):
  result = []
  if isinstance(x, dict):
    x = x.values()
  for el in x:
    if isinstance(el, Iterable) and not isinstance(el, str):
      result.extend(flatten(el))
    else:
      result.append(el)
  return result

def validate_scenario(f):
  @wraps(f)
  def wrapped(*args, **kwargs):
    data = request.get_json()
    flat = flatten(data)

    for elem in flat:
      if re.fullmatch(reg_scenario, str(elem)) == None:
        return jsonify({
          "error": True, 
          "message": "Bad characters in input."
        }), 400
    return f(*args, **kwargs)
  return wrapped

# Return true if ok
def validate_uuid(code):
  if re.fullmatch(reg_uuid, code) == None:
    return False
  return True
