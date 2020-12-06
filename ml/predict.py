from flask import jsonify, abort, request
from init_flask import app, engine_ml

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    raw_data = str(request.json['data'])

    to_predict = raw_data.split(',')

    if len(to_predict) != 1600:
        return jsonify({'error': 'Must pass 1600 features where each feature can take the value of 0 or 1.'}), 400

    prediction = predict(raw_data)

    return jsonify({'success': True, 'prediction': prediction})

def predict(raw_data):
    to_predict = raw_data.split(',')

    # if len(split) != 1600:
    #     return jsonify({'error': 'Must pass 1600 features where each feature can take the value of 0 or 1.'}), 400

    conn_ml = engine_ml.connect()
    classes_sql = conn_ml.execute('select ID, c, p from class;')
    conn_ml.close()

    classes = {}
    for row in classes_sql:
        _class = int(row['ID'])
        classes[_class] = {
            'c': row['c'],
            'p': row['p']
        }

    # prob_0 = classes[0]['p']
    # prob_1 = classes[1]['p']

    prob_0 = 1
    prob_1 = 1

    conn_ml = engine_ml.connect()
    features = conn_ml.execute('select ID, p00, p01, p10, p11 from feature;')
    conn_ml.close()

    for feature in features:
        # print(f"{feature['ID']}, {feature['p00']}, {feature['p01']}, {feature['p10']}, {feature['p11']}")
        value = to_predict[feature['ID']]
        prob_0 *= feature[f'p{value}0']
        prob_1 *= feature[f'p{value}1']

    # print(prob_0)
    # print(prob_1)
    # print('Happy' if prob_0 > prob_1 else 'Heart')

    return 0 if prob_0 > prob_1 else 1