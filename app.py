from flask import Flask, jsonify
from sqlalchemy import create_engine

from init_flask import app, conn

from user import *
from organization import *
from registration import *
from type import *

@app.route('/')
def index():
    return 'Hello World'
