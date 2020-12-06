from flask import jsonify
from init_flask import app, engine


@app.route('/room_user', methods=['GET'])
def room_user():
    try:
        conn = engine.connect()

        results = conn.execute(
            """ select  room_user.RID,
                        room_user.UID,
                        user.name as user_name,
                        organization.name as organization_name
                from room_user join user join organization join room
                where RID=room.ID and UID=user.ID;""")
        room_user = []
        for row in results:
            room_user.append({
                'room_id': row['RID'],
                'user_id': row['UID'],
                'user_name': row['user_name'],
                'organization_name': row['organization_name'],
            })

        conn.close()

        return jsonify({
            'success': True,
            'room_user': room_user
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False,
            'error': str(ex)
        }), 500
