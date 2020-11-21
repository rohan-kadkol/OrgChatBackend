from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine('mysql://kali:kali@localhost:3306/orgchat')
conn = engine.connect()