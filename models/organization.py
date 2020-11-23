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
def registrations(organization_id):
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