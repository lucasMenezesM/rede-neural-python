from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# -----------------------------
# Classe Rede Neural simples
# -----------------------------


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def backward(self, X, y, output, learning_rate=0.1):
        error = y - output
        d_output = error * self.sigmoid_derivative(output)

        error_hidden = d_output.dot(self.W2.T)
        d_hidden = error_hidden * self.sigmoid_derivative(self.a1)

        self.W2 += self.a1.T.dot(d_output) * learning_rate
        self.b2 += np.sum(d_output, axis=0, keepdims=True) * learning_rate
        self.W1 += X.T.dot(d_hidden) * learning_rate
        self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs=1000):
        for _ in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)

    def predict(self, X):
        output = self.forward(X)
        return np.argmax(output, axis=1)


# -----------------------------
# Criando rede neural
# 4x4 -> 16 entradas
# 10 saídas (dígitos 0 a 9)
# -----------------------------
nn = NeuralNetwork(input_size=16, hidden_size=16, output_size=10)

# -----------------------------
# Endpoint para treinar a rede
# -----------------------------


@app.route("/treinar", methods=["GET"])
def treinar():
    if request.json is None:
        return jsonify({"erro": "Envie um JSON válido"}), 400

    epocas = request.json.get("epocas")

    # Exemplo de dataset: números "0" e "1"
    # (na prática você teria mais dados para treinar melhor)
    X = np.array([
        [0, 0, 1, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         0, 0, 1, 0],  # número "1"
        [0, 1, 1, 0,
         1, 0, 0, 1,
         1, 1, 1, 1,
         1, 0, 0, 1],  # número "0"
    ])

    y = np.array([
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # representa "1"
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # representa "0"
    ])

    nn.train(X, y, epochs=epocas)

    return jsonify({"status": "rede treinada com sucesso!"})

# -----------------------------
# Endpoint para prever
# -----------------------------


@app.route("/prever", methods=["POST"])
def prever():
    if request.json is None:
        return jsonify({"erro": "Envie um JSON válido"}), 400

    data = request.json.get("matriz")

    if not data or len(data) != 4 or any(len(row) != 4 for row in data):
        return jsonify({"erro": "Envie uma matriz 4x4 válida"}), 400

    # Flatten (4x4 -> vetor de 16)
    X = np.array(data).reshape(1, 16)

    pred = nn.predict(X)
    return jsonify({"previsao": int(pred[0])})


if __name__ == "__main__":
    app.run(debug=True)
