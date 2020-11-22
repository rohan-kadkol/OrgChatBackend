from flask import Flask
from sqlalchemy import create_engine

import os

username = os.environ['ORGCHAT_DB_USERNAME']
password = os.environ['ORGCHAT_DB_PASSWORD']

app = Flask(__name__)
engine = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
conn = engine.connect()