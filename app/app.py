from flask import Flask, jsonify
from flask_cors import CORS
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

def get_sock():
  return sock

CORS(app, resources=r'/api/*')

from app.api.routes import api
app.register_blueprint(api, url_prefix='/api')
