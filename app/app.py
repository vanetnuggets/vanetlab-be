from flask import Flask, jsonify
from flask_cors import CORS
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

CORS(app, resources=r'/api/*')
CORS(app, resources=r'/ws/*')

from app.api.routes import api

app.register_blueprint(api, url_prefix='/api')
