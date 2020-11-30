from flask import Flask, jsonify, request
from sqlalchemy import create_engine

from init_flask import app, conn

from models.user import *
from models.organization import *
from models.registration import *
from models.type import *
from models.room import *
from models.room_user import *
from models.message import *

from ml.data import *

@app.route('/')
def index():
    return 'Hello World'

# @app.route('/auth', methods=['POST'])
# def auth():
#     email = request.json['email']
#     password = request.json['password']


