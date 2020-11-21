from flask import jsonify
from init_flask import app, conn

@app.route('/users', methods=['GET'])
def users():
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