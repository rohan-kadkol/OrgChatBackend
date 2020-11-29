from flask import jsonify, abort, request
from init_flask import app, conn_ml


@app.route('/prediction/data', methods=['POST'])
def add_data():
    data = request.json['data']
    class = request.json['class']

    split = data.split(',')
    if len(split) != 1600:
        return jsonify({'error': 'Must pass 1600 features where each feature can take the value of 0 or 1.'}), 400

    conn_ml.execute("""insert into data (data, timestamp, class) values (%(data)s, now(), %(class)d);""", {'data': data, 'class': class})

    return jsonify({'success': True})
