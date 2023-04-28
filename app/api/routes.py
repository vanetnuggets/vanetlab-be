from flask import Blueprint, send_file, request, make_response, redirect, jsonify, render_template
from app.managers.tcl_parser import tcl_parser
from app.managers.filemanager import filemanager
from app.managers.ns3manager import ns3manager
from app.managers.queuemanager import queue

from app.managers.security import authorized
from app.app import sock

import time, json

api = Blueprint('api', __name__)

@sock.route('/ws/status/<name>')
def get_status(socket, name):
  while True:
    status = queue.get_status_for(name)
    socket.send(json.dumps(status))

    if status['finished'] == True:
      socket.close()
      break

    time.sleep(1)

@api.route('/key/check')
@authorized
def checkkey():
  return "", 200

@api.route('/isalive')
def isalive():
  return jsonify({
    "volumetest": "all good",
    "error": False,
    "isalive": True
  })

@api.route('/from-sumo', methods=['POST'])
@authorized
def from_sumo():
  data = dict(request.form)

  name = data['name']
  trace_file = request.files['sumotrace']

  ok = filemanager.create_scenario(name)
  
  if ok == False:
    return jsonify({
      "error": True,
      "data": f"scenario with named {name} already exists."
    }), 400

  filemanager.save_sumo(name, trace_file)

  ns3manager.generate_ns2_mobility(name)

  conf = tcl_parser.tcl_to_conf(filemanager.get_ns2tcl(name))
  filemanager.save_conf(name, conf)

  return conf, 201

@api.route('/get/<name>/<file>', methods=['GET'])
def get_file(name, file):
  file_path = None
  if file == 'output':
    file_path = filemanager.get_file(name, 'output.txt')

  elif file == 'mobility':
    file_path= filemanager.get_file(name, 'mobility.tcl')
    
  elif file == 'trace':
    file_path = filemanager.get_file(name, 'trace.xml')

  elif file == 'config':
    file_path = filemanager.get_file(name, 'config.json')
    
  if file_path:
    return send_file(file_path)
  
  return jsonify({
    'error': True,
    'data': 'scenario or file does not exist. ensure you ran the simulation.' 
  }), 400

@api.route('/simulate/<name>', methods=['POST'])
@authorized
def simulate(name):
  filemanager.create_scenario(name)
  conf = request.get_json()
  
  try:
    queue.add({
      "name": name,
      "config": conf,
      "action": "simulate"
    })
    queue.next()
  except Exception as e:
    print(e)
    return {
      "error": True,
      "message": "scenario already in queue."
    }, 400
    
  return {
    "error": False,
    "message": "scenario queued up for simulation"
  }
 
@api.route('/summary/<name>', methods=['GET'])
def summary(name):
  try:
    summary = filemanager.summary(name)
    return jsonify({
      "error": False,
      "data": summary
    }), 200
  except:
    return jsonify({
      "error": True,
      "date": "no simulation output"
    }), 404



@api.route('/validate/<name>', methods=['POST'])
@authorized
def test_scenario(name, save_to='run'):
  filemanager.create_scenario(name)

  conf = request.get_json()
  filemanager.prepare_simulation(conf)
  err = ns3manager.validate(name)

  if err == None:
    return jsonify({
      "error": False,
      "data": None
    }), 200
  
  return jsonify({
    "error": True,
    "data": err
  }), 400

@api.route('/netanim-trace/<name>', methods=['GET'])
def get_trace(name):
  path = filemanager.get_netanim_trace(name)
  return send_file(path)

@api.route('/list', methods=['GET'])
def get_scenarios():
  return jsonify({
    "error": False,
    "data": filemanager.get_all_scenarios()
  })

@api.route('/scenario/<name>', methods=['GET'])
def get_scenario(name):
  if request.method == 'GET':
    return get_scenario(name)
  
@api.route('/scenario/<name>', methods=['POST'])
@authorized
def post_scenario(name):
  if request.method == 'POST':
    return post_scenario(name)


@api.route('/scenario/<name>', methods=['DELETE'])
@authorized
def remove_scenario(name):
  if filemanager.delete_scenario(name):
    return jsonify({
      "error": False,
      "message": f"scenario {name} successfully deleted"
    }), 204
  return jsonify({
    "error": True,
    "message": f"scenario {name} cannot be deleted"
  }), 404
      

@api.route('/exists/<name>', methods=['GET'])
def exists_scenario(name):
  res = filemanager.exists_scenario(name)
  return({
    "error": False,
    "data": res
  })

def post_scenario(name):
  data = request.get_json()
  if filemanager.save_conf(name, data):
    return jsonify({
      "error": False,
      "name": name
    }), 201
  
  return jsonify({
    "error": True,
    "message": f"scenario {name} could not be saved"
  }), 400

def get_scenario(name):
  config = {}
  try:
    config = filemanager.get_config(name)
  except Exception as e:
    return jsonify({
      "error": True,
      "message": "remote scenario does not exist."
    }), 404
  
  return jsonify({
    "error": False,
    "data": config
  }), 200
