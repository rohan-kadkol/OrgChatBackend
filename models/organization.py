from flask import jsonify, request
from init_flask import app, engine

@app.route('/test/organizations', methods=['GET'])
def test_organizations():
    try:
        conn = engine.connect()

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

        conn.close()

        return jsonify({
            'success': True,
            'organizations': organizations
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False
        }), 500

@app.route('/organizations', methods=['GET'])
def organizations():
    try:
        conn = engine.connect()

        query = request.args.get('query')

        results = conn.execute(
            """ select  organization.ID, 
                        organization.name,
                        type.name as type,
                        organization.location 
                from organization join type
                where   organization.type = type.ID and (
                        organization.name like %(query)s or
                        organization.location like %(query)s);""", {'query': f'%{query}%'})
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
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False
        }), 500

@app.route('/organizations/<int:organization_id>/users', methods=['GET'])
def organization_users(organization_id):
    try:
        conn = engine.connect()

        results = conn.execute(
            f""" select 	user.ID as user_id,
                        user.name as user_name,
                        user.phone_number as user_phone_number,
                        user.email as user_email

                from 	user join registration

                where 	user.ID = registration.UID
                        
                        and
                        
                        registration.OID = {organization_id};"""
        )
        registrations = []
        for row in results:
            registrations.append({
                'ID': row['user_id'],
                'name': row['user_name'],
                'phone_number': row['user_phone_number'],
                'email': row['user_email'],
            })

        conn.close()

        return jsonify({
            'success': True,
            'registrations': registrations
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False
        }), 500

@app.route('/organizations/<int:organization_id>/users', methods=['POST'])
def add_user_to_organization(organization_id):
    try :
        conn = engine.connect()
        user_id = request.json['user_id']
        conn.execute('insert into registration values (%(uid)s, %(oid)s);', {'uid': user_id, 'oid': organization_id})

        conn.close()

        return jsonify({
            'success': True,
        })
    except Exception as ex:
        print(ex);
        conn.close()
        return jsonify({
            'success': False,
            'error': str(ex)
        }), 500
    
@app.route('/organizations/<int:organization_id>/users/<string:user_id>/rooms', methods=['GET'])
def organization_user_rooms(organization_id, user_id):
    try:
        conn = engine.connect()

        results = conn.execute(
            f"""    select  room.ID,
                            room.name,
                            room.public,
                            room.organization
                    from room_user join room
                    where room_user.UID='{user_id}' and room_user.RID=room.ID and room.organization={organization_id}

                    union

                    select  room.ID,
                            room.name,
                            room.public,
                            room.organization
                    from room
                    where room.organization={organization_id} and room.public=1;""")
        rooms = []
        for row in results:
            rooms.append({
                'ID': row['ID'],
                'name': row['name'],
                'public': True if row['public'] == 1 else False,
                'organization': row['organization']
            })

        conn.close()

        return jsonify({
            'success': True,
            'rooms': rooms
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False
        }), 500

@app.route('/organizations/<int:organization_id>/users/<string:user_id>/rooms', methods=['POST'])
def add_room_to_organization_and_enroll_user_in_rooms(organization_id, user_id):
    conn = engine.connect()

    name = request.json['name']
    public = request.json['public']

    trans = conn.begin()
    try:
        result = conn.execute('insert into room (name, public, organization) values (%(name)s, %(public)s, %(organization)s);', {'name': name, 'public': public, 'organization': organization_id})
        inserted_room_id = result.lastrowid
        conn.execute('insert into room_user values (%(RID)s, %(UID)s);', {'RID': inserted_room_id, 'UID': user_id})
        trans.commit()

        conn.close()

        return jsonify({
            'success': True
        })
    except Exception as e:
        print(e)
        trans.rollback()

        conn.close()

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/organizations/<int:organization_id>/rooms', methods=['GET'])
def organization_rooms(organization_id):
    try:
        conn = engine.connect()

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

        conn.close()

        return jsonify({
            'success': True,
            'rooms': rooms
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False
        }), 500


@app.route('/organizations', methods=['POST'])
def add_organization():
    try:
        conn = engine.connect()

        name = request.json['name']
        type = request.json['type']
        location = request.json['location']

        conn.execute(
            """ insert into organization (name, type, location) values 
                            (   %(name)s,
                                %(type)s,
                                %(location)s);""", 
                                {'name': name, 'type': type, 'location': location})

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
        }), 500

@app.route('/organizations/<int:organization_id>/rooms', methods=['POST'])
def add_organization_rooms(organization_id):
    try:
        conn = engine.connect()

        name = request.json['name']
        public = request.json['public']

        conn.execute(
            """ insert into room (name, public, organization) values 
                            (   %(name)s,
                                %(public)s,
                                %(organization)s);""", 
                                {'name': name, 'public': public, 'organization': organization_id})

        conn.close()

        return jsonify({
            'success': True
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False,
            'error': str(ex)
        }), 500