from flask import jsonify
from ..init_flask import app, conn

@app.route('/types', methods=['GET'])
def types():
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