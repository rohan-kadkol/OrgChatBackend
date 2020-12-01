from flask import jsonify, request
from init_flask import app
from flask_cors import CORS, cross_origin

@app.route('/test/users', methods=['GET'])
def test_users():
    import os
    from sqlalchemy import create_engine

    username = os.environ['ORGCHAT_DB_USERNAME']
    password = os.environ['ORGCHAT_DB_PASSWORD']
    
    engine = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
    conn = engine.connect()

    results = conn.execute('select * from user;')
    users = []
    for row in results:
        users.append({
            'ID': row['ID'],
            'name': row['name'],
            'phone_number': row['phone_number'],
            'email': row['email']
        })

    conn.close()

    return jsonify({
        'success': True,
        'users': users
    })

@app.route('/users', methods=['GET'])
@cross_origin()
def users():
    import os
    from sqlalchemy import create_engine

    username = os.environ['ORGCHAT_DB_USERNAME']
    password = os.environ['ORGCHAT_DB_PASSWORD']
    
    engine = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
    conn = engine.connect()

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

    conn.close()

    return jsonify({
        'success': True,
        'users': users
    })

@app.route('/users/<string:user_id>', methods=['GET'])
@cross_origin()
def get_user(user_id):
    import os
    from sqlalchemy import create_engine

    username = os.environ['ORGCHAT_DB_USERNAME']
    password = os.environ['ORGCHAT_DB_PASSWORD']
    
    engine = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
    conn = engine.connect()

    results = conn.execute(""" select * from user
                                where   ID=%(ID)s;""", {'ID': user_id})
    users = []
    for row in results:
        users.append({
            'ID': row['ID'],
            'name': row['name'],
            'phone_number': row['phone_number'],
            'email': row['email']
        })

    conn.close()

    return jsonify({
        'success': True,
        'users': users
    })

@app.route('/users', methods=['POST'])
@cross_origin()
def add_user():
    import os
    from sqlalchemy import create_engine

    username = os.environ['ORGCHAT_DB_USERNAME']
    password = os.environ['ORGCHAT_DB_PASSWORD']
    
    engine = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
    conn = engine.connect()

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

        conn.close()

        return jsonify({
            'success': True,
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False,
            'error': str(ex)
        }), 400
        
@app.route('/users/<string:user_id>/organizations', methods=['GET'])
@cross_origin()
def user_organizations(user_id):
    import os
    from sqlalchemy import create_engine

    username = os.environ['ORGCHAT_DB_USERNAME']
    password = os.environ['ORGCHAT_DB_PASSWORD']
    
    engine = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
    conn = engine.connect()

    query = request.args.get('query')

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

    conn.close()
    
    return jsonify({
        'success': True,
        'organizations': organizations
    })