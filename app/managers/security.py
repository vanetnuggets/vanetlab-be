from collections import Iterable
from functools import wraps
from flask import request, jsonify
import re

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

    regex = r'[a-zA-Z0-9_\.]*'
    for elem in flat:
      if re.fullmatch(regex, str(elem)) == None:
        return jsonify({
          "error": True, 
          "message": "Bad characters in input."
        }), 400
    return f(*args, **kwargs)
  return wrapped


