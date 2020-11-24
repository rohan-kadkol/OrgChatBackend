from flask import jsonify, request
from init_flask import app, conn

@app.route('/test/organizations', methods=['GET'])
def test_organizations():
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

@app.route('/organizations', methods=['GET'])
def organizations():
    query = request.args.get('query')

    results = conn.execute(
        f""" select  organization.ID, 
                    organization.name,
                    type.name as type,
                    organization.location 
            from organization join type
            where   organization.type = type.ID and
                    organization.name like '%%{query}%%' or
                    organization.location like '%%{query}%%';""")
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

@app.route('/organizations/<int:organization_id>/users', methods=['GET'])
def organization_users(organization_id):
    results = conn.execute(
        f""" select 	user.ID as user_id,
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
	                organization.type = type.ID
                    
                    and
                    
                    organization.ID = {organization_id};"""
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

@app.route('/organizations/<int:organization_id>/rooms', methods=['GET'])
def organization_rooms(organization_id):
    results = conn.execute(
        f""" select 	room.ID,
	                room.name,
	                room.public,
                    organization.name as organization
            from	room join organization
            where   room.organization = organization.ID and
                    room.organization = {organization_id};""")
    rooms = []
    for row in results:
        rooms.append({
            'ID': row['ID'],
            'name': row['name'],
            'public': True if row['public'] == 1 else False,
            'organization': row['organization']
        })
    return jsonify({
        'success': True,
        'rooms': rooms
    })

@app.route('/organizations', methods=['POST'])
def add_organization():
    try:
        name = request.json['name']
        type = request.json['type']
        location = request.json['location']

        conn.execute(
            """ insert into organization (name, type, location) values 
                            (   %(name)s,
                                %(type)s,
                                %(location)s);""", 
                                {'name': name, 'type': type, 'location': location})

        return jsonify({
            'success': True,
        })
    except Exception as ex:
        print(ex)
        return jsonify({
            'success': False,
            'error': str(ex)
        }), 400

@app.route('/organizations/<int:organization_id>/rooms', methods=['POST'])
def add_organization_rooms(organization_id):
    try:
        name = request.json['name']
        public = request.json['public']

        conn.execute(
            """ insert into room (name, public, organization) values 
                            (   %(name)s,
                                %(public)s,
                                %(organization)s);""", 
                                {'name': name, 'public': public, 'organization': organization_id})

        return jsonify({
            'success': True
        })
    except Exception as ex:
        print(ex)
        return jsonify({
            'success': False,
            'error': str(ex)
        }), 400
