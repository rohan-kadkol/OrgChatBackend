from flask import jsonify
from ..init_flask import app, conn

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