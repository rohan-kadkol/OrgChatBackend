from flask import jsonify
from init_flask import app, conn


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

    print(str)

    results = conn.execute(str)
    messages = []
    for row in results:
        messages.append({
            'ID': row['ID'],
            'message': row['message'],
            'sender': row['sender'],
            'name': row['name'],
            'timestamp': row['timestamp']
        })
    return jsonify({
        'success': True,
        'messages': messages
    })
