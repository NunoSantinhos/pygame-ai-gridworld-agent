import random
import json
import numpy as np
from scipy.special import softmax

def relu(a):
    return np.maximum(0, a)


class NeuralNetwork:
    def __init__(self, layer_nodes):
        self.layer_nodes = layer_nodes
        self.weights = []
        self.bias = []

        for i in range(len(self.layer_nodes) - 1):
            w = np.random.uniform(low=-1, high=1, size=(layer_nodes[i + 1], layer_nodes[i]))
            b = np.random.uniform(low=-1, high=1, size=(layer_nodes[i + 1], 1))
            self.weights.append(w)
            self.bias.append(b)

        # Converter listas de arrays para listas de arrays de NumPy (mantém cada matriz como um elemento separado)
        self.weights = np.array(self.weights, dtype=object)
        self.bias = np.array(self.bias, dtype=object)

        print(self.weights)
        print(self.bias)


    def feed_forward(self, x):
        print("x:", x)
        print("w:",self.weights)
        a = x
        for i in range(len(self.layer_nodes) - 2):
            z = self.weights[i] @ a
            a = relu(z)

        o = self.weights[-1] @ a
        o = softmax(o)
        y_pred = np.argmax(o)

        p = {0: "up", 1: "down", 2: "left", 3: "right"}

        return p[y_pred]

    def to_dict(self):
        return {
            "weights": self.weights,
            "biases": self.bias,
        }



class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, NeuralNetwork):
            return {
                "weights": obj.weights.tolist(),
                "biases": obj.bias.tolist(),
            }
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


