from flask import jsonify
from init_flask import app, engine


@app.route('/messages', methods=['GET'])
def messages():
    try:
        conn = engine.connect()

        results = conn.execute(
            """ select  message.ID,
                        message.message,
                        message.timestamp,
                        user.name as user_name,
                        room.name as room_name,
                        organization.name as organization_name
                from message join user join room join organization
                where   message.sender = user.ID and
                        message.room = room.ID and
                        room.organization = organization.ID;""")
        messages = []
        for row in results:
            messages.append({
                'message_id': row['ID'],
                'message_message': row['message'],
                'timestamp': row['timestamp'],
                'user_name': row['user_name'],
                'room_name': row['room_name'],
                'organization_name': row['organization_name'],
            })
        return jsonify({
            'success': True,
            'messages': messages
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False
        }), 500
