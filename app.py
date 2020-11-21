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


@app.route('/types', methods=['GET'])
def types():
    results = conn.execute("""  select  ID,
                                        name 
                                from type;""")
    types = []
    for row in results:
        types.append({
            'ID': row['ID'],
            'name': row['name']
        })
    return jsonify({
        'success': True,
        'types': types
    })


@app.route('/registrations', methods=['GET'])
def registrations():
    results = conn.execute(
        """ select 	user.ID as user_id,
	                user.name as user_name,
	                user.phone_number as user_phone_number,
	                user.email as user_email,
	                organization.ID as organization_id,
	                organization.name as organization_name,
	                type.name as organization_type,
	                organization.location as organization_location

            from 	user join registration
	                join organization join type

            where 	user.ID = registration.UID and 
	                organization.id = registration.OID and
	                organization.type = type.ID;"""
    )
    registrations = []
    for row in results:
        registrations.append({
            'user_id': row['user_id'],
            'user_name': row['user_name'],
            'user_phone_number': row['user_phone_number'],
            'user_email': row['user_email'],
            'organization_id': row['organization_id'],
            'organization_name': row['organization_id'],
            'organization_type': row['organization_type'],
            'organization_location': row['organization_location'],
        })
    return jsonify({
        'success': True,
        'registrations': registrations
    })