from flask import Flask
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine

import os

username = os.environ['ORGCHAT_DB_USERNAME']
password = os.environ['ORGCHAT_DB_PASSWORD']

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

engine = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
conn = engine.connect()

engine_ml = create_engine(f'mysql://{username}:{password}@localhost:3306/emojipredict')
conn_ml = engine_ml.connect()


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./protected/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()