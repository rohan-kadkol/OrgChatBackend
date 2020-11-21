from flask import jsonify
from init_flask import app, conn

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