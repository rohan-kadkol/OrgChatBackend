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