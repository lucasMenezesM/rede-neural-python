import numpy as np


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
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
        # calcular saída da camada escondida
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)

        # calcular saída da camada de saída
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def backward(self, X, y, output, learning_rate=0.1):
        # calcula o erro na camada de saída
        error = y - output

        # calcula gradiente do erro na camada de saída
        d_output = error * self.sigmoid_derivative(output)

        # atualiza as sinapses da camada de saída
        self.W2 += self.a1.T.dot(d_output) * learning_rate
        self.b2 += np.sum(d_output, axis=0, keepdims=True) * learning_rate

        # retropropaga o gradiente do erro para até a camada escondida
        error_hidden = d_output.dot(self.W2.T)
        d_hidden = error_hidden * self.sigmoid_derivative(self.a1)

        # atualiza as sinapses da camada escondida
        self.W1 += X.T.dot(d_hidden) * learning_rate
        self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs=1000):
        for _ in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)
        self.trained = True

    def identify(self, X):
        output = self.forward(X)
        return np.argmax(output, axis=1)
