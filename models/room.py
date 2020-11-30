from flask import jsonify, request
from init_flask import app, conn, db

# @app.route('/test/rooms', methods=['GET'])
# def test_rooms():
#     results = conn.execute(
#         """ select 	room.ID,
# 	                room.name,
# 	                room.public,
#                     organization.name as organization
#             from	room join organization
#             where   room.organization = organization.ID;""")
#     rooms = []
#     for row in results:
#         rooms.append({
#             'ID': row['ID'],
#             'name': row['name'],
#             'public': True if row['public'] == 1 else False,
#             'organization': row['organization']
#         })
#     return jsonify({
#         'success': True,
#         'rooms': rooms
#     })

@app.route('/rooms/<int:room_id>/messages', methods=['GET'])
def room_messages(room_id):
    str = f""" select  message.ID,
                message.message,
                message.sender,
                user.name,
                UNIX_TIMESTAMP(timestamp) as timestamp
        from message join user on message.sender=user.ID
        where room={room_id} order by message.ID desc;"""

    results = conn.execute(str)
    messages = []

    print('START')    
    print(results)
    print(type(results))

    length = 0
    for row in results:
        length = length + 1
        messages.append({
            'ID': row['ID'],
            'message': row['message'],
            'sender': row['sender'],
            'name': row['name'],
            'timestamp': row['timestamp']
        })

    print(len)
    print(len(messages))
    print(messages)
    print('END')

    return jsonify({
        'success': True,
        'messages': messages
    })


@app.route('/rooms/<int:room_id>/messages', methods=['POST'])
def send_message(room_id):
    try:
        message = request.json['message']
        sender = request.json['sender']

        conn.execute('insert into message (message, sender, timestamp, room) values (%(message)s, %(sender)s, now(), %(room)s);',
                     {'message': message, 'sender': sender, 'room': room_id})

        message_ref = db.collection(u'orgchat').document(u'main')
        message = message_ref.get().to_dict()
        print(message)
        message['orgchat'] = (message['orgchat'] + 1) % 1000
        message_ref.set(message)

        return jsonify({
            'success': True,
        })
    except Exception as ex:
        print(ex)
        return jsonify({
            'success': False,
            'error': str(ex)
        })
