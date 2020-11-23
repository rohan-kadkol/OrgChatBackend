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