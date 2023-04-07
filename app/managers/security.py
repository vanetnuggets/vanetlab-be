from collections import Iterable
from functools import wraps
from flask import request, jsonify
import re
import config

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

# Return true if ok
def validate_uuid(code):
  if re.fullmatch(reg_uuid, code) == None:
    return False
  return True

def authorized(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth == None:
            return jsonify({
                "error": True,
                "message": "no api key supplied"
            }), 401
        token = auth.split(" ")[1].strip()
        if token != config.API_KEY:
            return ({
                "error": True,
                "message": "invalid api key"
            }), 401
        return f(*args, **kwargs)
    return wrapped

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

def validate_code(f):
  @wraps(f)
  def wrapped(*args, **kwargs):
    if 'code' not in request.args:
      return jsonify({
      "error": True,
      "message": "scenario code not specified."
    }), 400
    code = request.args.get('code')
    if validate_uuid(code) == False:
      return jsonify({
        "error": True,
        "message": "wrong code format. dir traversal attempt?"
      }), 400
    return f(*args, **kwargs)
  return wrapped
