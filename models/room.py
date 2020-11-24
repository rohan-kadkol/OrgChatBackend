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
