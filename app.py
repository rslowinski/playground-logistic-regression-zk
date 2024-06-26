from flask import Flask, request, jsonify, render_template
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import subprocess
import json

app = Flask(__name__)

data = load_iris()
X, y = data.data, data.target
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = LogisticRegression(max_iter=200)
model.fit(X_scaled, y)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    input_data = np.array(request.json['input_data']).reshape(1, -1)
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]

    # Prepare the input for the zk-SNARK
    coef = model.coef_[0].tolist()
    intercept = float(model.intercept_[0])
    zk_input = {
        "x": input_scaled[0].tolist(),
        "coef": coef,
        "intercept": intercept
    }

    with open("input.json", "w") as f:
        json.dump(zk_input, f)

    subprocess.run(["snarkjs", "groth16", "prove", "circuit_final.zkey", "input.json", "proof.json", "public.json"])

    with open("proof.json") as f:
        proof = json.load(f)

    return jsonify({'prediction': int(prediction), 'proof': proof})


@app.route('/verify', methods=['POST'])
def verify():
    proof = request.json['proof']

    with open("proof.json", "w") as f:
        json.dump(proof, f)

    result = subprocess.run(["snarkjs", "groth16", "verify", "verification_key.json", "public.json", "proof.json"],
                            capture_output=True, text=True)

    is_valid = "OK" in result.stdout
    return jsonify({'is_valid': is_valid})


if __name__ == '__main__':
    app.run(debug=True)
