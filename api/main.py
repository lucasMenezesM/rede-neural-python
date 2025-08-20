from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from NeuralNetwork import NeuralNetwork
from conjuntos_treinamento import training_sets, wished_outputs

app = Flask(__name__)
CORS(app)


nn = NeuralNetwork(input_size=16, hidden_size=2, output_size=3)


@app.route("/treinar", methods=["POST"])
def treinar():
    if request.json is None:
        return jsonify({"erro": "Envie um JSON válido"}), 400

    epochs = request.json.get("epochs")

    if not epochs:
        return jsonify({"erro": "Envie o número de épocas"}), 400

    # conjuntos de treinamento dos dígitos 0, 1 e 4
    X = np.array(training_sets)

    # saídas desejadas para cada conjunto de treinamento
    y = np.array(wished_outputs)

    nn.train(X=X, y=y, epochs=epochs)

    return jsonify({"sucesso": "Rede treinada com sucesso!"}), 200


@app.route("/identificar", methods=["POST"])
def identificar():
    if nn.trained is False:
        return jsonify({"erro": "Rede neural não treinada"}), 400

    if request.json is None:
        return jsonify({"erro": "Envie um JSON válido"}), 400

    data = request.json.get("matriz")

    if not data or len(data) != 4 or any(len(row) != 4 for row in data):
        return jsonify({"erro": "Envie uma matriz 4x4 válida"}), 400

    # Flatten (4x4 -> vetor de 16)
    X = np.array(data).reshape(1, 16)

    result = nn.identify(X)
    return jsonify({"previsao": int(result[0])}), 200


if __name__ == "__main__":
    app.run(debug=True)
