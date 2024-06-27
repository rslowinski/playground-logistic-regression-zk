import hashlib

import numpy as np
from flask import Flask, request, jsonify, render_template
from py_ecc.optimized_bls12_381 import G1, multiply, curve_order
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

data = load_iris()
X, y = data.data, data.target
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = LogisticRegression(max_iter=200)
model.fit(X_scaled, y)

class_labels = data.target_names


def hash_to_int(data):
    return int(hashlib.sha256(data).hexdigest(), 16) % curve_order


def generate_proof(input_data, model, prediction):
    input_hash = hash_to_int(input_data.tobytes())
    model_hash = hash_to_int(model.coef_.tobytes())
    prediction_hash = hash_to_int(prediction.encode())
    proof = multiply(G1, input_hash + model_hash + prediction_hash)
    return proof


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    input_data = np.array(request.json['input_data']).reshape(1, -1)
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    prediction_label = class_labels[prediction]
    proof = generate_proof(input_scaled[0], model, prediction_label)
    return jsonify({'prediction': prediction_label, 'proof': str(proof)})


@app.route('/verify', methods=['POST'])
def verify():
    input_data = np.array(request.json['input_data']).reshape(1, -1)
    proof = request.json['proof']
    prediction = request.json['prediction']
    input_scaled = scaler.transform(input_data)
    expected_hash = multiply(G1,
                             hash_to_int(input_scaled[0].tobytes()) + hash_to_int(model.coef_.tobytes()) + hash_to_int(
                                 prediction.encode()))
    is_valid = (str(expected_hash) == proof)
    return jsonify({'is_valid': is_valid})


if __name__ == '__main__':
    app.run(debug=True)
