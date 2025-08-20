import numpy as np


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # input_size = 16 | hidden_size = 2 | output_size = 3
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))
        self.trained = False

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, X):
        # 1º Passo: calcular saída da camada escondida
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)

        # 2º Passo: calcular saída da camada de saída
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def backward(self, X, y, output, learning_rate=0.1):
        # 3º Passo: calcula o erro na camada de saída
        error = y - output

        # 4º Passo: calcula gradiente do erro na camada de saída
        d_output = error * self.sigmoid_derivative(output)

        # 5º Passo: atualiza as sinapses da camada de saída
        self.W2 += self.a1.T.dot(d_output) * learning_rate
        self.b2 += np.sum(d_output, axis=0, keepdims=True) * learning_rate

        # 6º Passo: retropropaga o gradiente do erro para até a camada escondida
        error_hidden = d_output.dot(self.W2.T)
        d_hidden = error_hidden * self.sigmoid_derivative(self.a1)

        # 7º Passo: atualiza as sinapses da camada escondida
        self.W1 += X.T.dot(d_hidden) * learning_rate
        self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs=1000):
        for _ in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)
        self.trained = True

    def identify(self, X):
        output = self.forward(X)  # output = [0.8, 0.1, 0.05]
        return np.argmax(output, axis=1)
