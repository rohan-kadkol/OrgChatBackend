from flask import jsonify, request
from init_flask import app, conn

@app.route('/test/users', methods=['GET'])
def test_users():
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

@app.route('/users', methods=['GET'])
def users():
    query = request.args.get('query')

    results = conn.execute(f""" select * from user
                                where   name like '%%{query}%%' or
                                        email like '%%{query}%%' or
                                        phone_number like '%%{query}%%';""")
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

@app.route('/users', methods=['POST'])
def add_user():
    try:
        ID = request.json['ID']
        name = request.json['name']
        phone_number = request.json['phone_number']
        email = request.json['email']

        conn.execute(
            """ insert into user (ID, name, phone_number, email) values 
                            (   %(ID)s,
                                %(name)s,
                                %(phone_number)s,
                                %(email)s);""", 
                                {'ID': ID, 'name': name, 'phone_number': phone_number, 'email': email})

        return jsonify({
            'success': True,
        })
    except Exception as ex:
        print(ex)
        return jsonify({
            'success': False,
            'error': str(ex)
        }), 400
        
@app.route('/users/<string:user_id>/organizations', methods=['GET'])
def user_organizations(user_id):
    query = request.args.get('query')

    print(f""" select  organization.ID, 
                    organization.name,
                    type.name as type,
                    organization.location 
            from registration join organization join type
            where   registration.OID = organization.ID and
                    organization.type = type.ID and (
                    organization.name like '%{query}%' or
                    organization.location like '%{query}%')
                    and
                    registration.UID = '{user_id}';""")

    results = conn.execute(
        f""" select  organization.ID, 
                    organization.name,
                    type.name as type,
                    organization.location 
            from registration join organization join type
            where   registration.OID = organization.ID and
                    organization.type = type.ID and (
                    organization.name like '%%{query}%%' or
                    organization.location like '%%{query}%%')
                    and
                    registration.UID = '{user_id}';""")
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