from flask import jsonify
from init_flask import app, engine


@app.route('/types', methods=['GET'])
def types():
    try:
        conn = engine.connect()

        results = conn.execute("""  select  ID,
                                            name 
                                    from type;""")
        types = []
        for row in results:
            types.append({
                'ID': row['ID'],
                'name': row['name']
            })
        return jsonify({
            'success': True,
            'types': types
        })
    except Exception as ex:
        print(ex)
        conn.close()
        return jsonify({
            'success': False
        }), 500
