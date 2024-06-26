# Zero-Knowledge Proof Machine Learning Project

This project demonstrates oversimplified integration of Zero-Knowledge Proofs (zk-SNARKs) with a logistic regression model
using `snarkjs` and `circom`.

## Prerequisites

- Node.js and npm
- Python 3.x
- Flask
- Required npm packages:
    - `snarkjs`
    - `circom`
- Required Python packages:
    - `scikit-learn`
    - `numpy`
    - `flask`

Set-up:

1. Compile the circuit and generate the necessary keys:

```shell
circom circuit.circom --r1cs --wasm --sym
snarkjs powersoftau new bn128 12 pot12_0000.ptau
snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau --name="First contribution" -v
snarkjs powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau
snarkjs groth16 setup circuit.r1cs pot12_final.ptau circuit_0000.zkey
snarkjs zkey contribute circuit_0000.zkey circuit_final.zkey --name="Second contribution" -v
snarkjs zkey export verificationkey circuit_final.zkey verification_key.json
```

2. Run the app:

```shell
python app.py
```

# Usage

### Getting Prediction and Proof

Enter the input data (sepal length, sepal width, petal length, petal width) in the form.
Click the "Get Prediction and Proof" button.
The prediction and proof will be displayed.

### Verifying the Proof

After getting the prediction and proof, click the "Verify Proof" button.
The verification result will be displayed.

### File Structure

- app.py: The Flask backend that handles model prediction and zk-SNARK proof generation/verification.
- templates/index.html: The frontend HTML file.
- circuit.circom: The circom circuit definition file.


