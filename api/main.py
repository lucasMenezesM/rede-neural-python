from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from NeuralNetwork import NeuralNetwork

app = Flask(__name__)
CORS(app)

# -----------------------------
# Criando rede neural
# 4x4 -> 16 entradas
# 3 saídas (dígitos 0 a 2)
# -----------------------------
nn = NeuralNetwork(input_size=16, hidden_size=2, output_size=3)

# -----------------------------
# Endpoint para treinar a rede
# -----------------------------


@app.route("/treinar", methods=["POST"])
def treinar():
    if request.json is None:
        return jsonify({"erro": "Envie um JSON válido"}), 400

    epocas = request.json.get("epocas")

    if not epocas:
        return jsonify({"erro": "Envie o número de épocas"}), 400

    X = np.array([
        [1, 1, 1, 1,
         1, 0, 0, 1,
         1, 0, 0, 1,
         1, 1, 1, 1],  # número "0",
        [0, 0, 1, 0,
         0, 0, 1, 0,
         0, 0, 1, 0,
         0, 0, 1, 0],  # número "1"
        [0, 0, 1, 0,
         0, 1, 1, 0,
         1, 1, 1, 1,
         0, 0, 1, 0],  # número "4",
    ])

    y = np.array([
        [1, 0, 0],  # "0" → posição 0
        [0, 1, 0],  # "1" → posição 1
        [0, 0, 1],  # "4" → posição 2
    ])

    nn.train(X, y)

    return jsonify({"status": "rede treinada com sucesso!"}), 200

# -----------------------------
# Endpoint para prever
# -----------------------------


@app.route("/prever", methods=["POST"])
def prever():
    if nn.trained is False:
        return jsonify({"erro": "Rede neural não treinada"}), 400

    if request.json is None:
        return jsonify({"erro": "Envie um JSON válido"}), 400

    data = request.json.get("matriz")

    if not data or len(data) != 4 or any(len(row) != 4 for row in data):
        return jsonify({"erro": "Envie uma matriz 4x4 válida"}), 400

    # Flatten (4x4 -> vetor de 16)
    X = np.array(data).reshape(1, 16)

    pred = nn.predict(X)
    return jsonify({"previsao": int(pred[0])}), 200


if __name__ == "__main__":
    app.run(debug=True)
