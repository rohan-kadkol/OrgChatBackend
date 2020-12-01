from flask import jsonify, request
from init_flask import app, db

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
    import os
    from sqlalchemy import create_engine

    username = os.environ['ORGCHAT_DB_USERNAME']
    password = os.environ['ORGCHAT_DB_PASSWORD']
    
    engine1 = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
    conn1 = engine1.connect()

    str = f""" select  message.ID,
                message.message,
                message.sender,
                user.name,
                UNIX_TIMESTAMP(timestamp) as timestamp
        from message join user on message.sender=user.ID
        where room={room_id} order by message.ID desc;"""

    results = conn1.execute(str)
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

    print(length)
    print(len(messages))
    print(messages)
    print('END')

    conn1.close()

    return jsonify({
        'success': True,
        'messages': messages
    })


@app.route('/rooms/<int:room_id>/messages', methods=['POST'])
def send_message(room_id):
    import os
    from sqlalchemy import create_engine

    username = os.environ['ORGCHAT_DB_USERNAME']
    password = os.environ['ORGCHAT_DB_PASSWORD']
    
    engine = create_engine(f'mysql://{username}:{password}@localhost:3306/orgchat')
    conn = engine.connect()

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
        })
