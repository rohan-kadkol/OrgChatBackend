from flask import Flask, jsonify
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine('mysql://kali:kali@localhost:3306/orgchat')
conn = engine.connect()


@app.route('/')
def index():
    return 'Hello World'


@app.route('/users', methods=['GET'])
def users():
    results = conn.execute('select * from user;')
    users = []
    for row in results:
        users.append({
            'ID': row['ID'],
            'name': row['name'],
            'phone_number': row['phone_number'],
            'email': row['email']
        })
    return jsonify({
        'success': True,
        'users': users
    })


@app.route('/organizations', methods=['GET'])
def organizations():
    results = conn.execute(
        """ select  organization.ID, 
                    organization.name,
                    type.name as type,
                    organization.location 
            from organization join type
            where organization.type = type.ID;""")
    organizations = []
    for row in results:
        organizations.append({
            'ID': row['ID'],
            'name': row['name'],
            'type': row['type'],
            'location': row['location']
        })
    return jsonify({
        'success': True,
        'organizations': organizations
    })
