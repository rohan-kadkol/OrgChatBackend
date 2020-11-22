from flask import Flask, jsonify
from sqlalchemy import create_engine

from init_flask import app, conn

from models.user import *
from models.organization import *
from models.registration import *
from models.type import *

@app.route('/')
def index():
    return 'Hello World'
