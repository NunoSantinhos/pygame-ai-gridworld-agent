from Neuralnetwork import *


# def n max_passsos
class Gene:
    def __init__(self):
        self._dna = NeuralNetwork((4, 6, 4))
        self.moves = 30
        self._fitness_score = 0  # ja esta feito
        self.left_garbage = None
        self.life_genaration = 1

    def get_dna(self):
        return self._dna

    def set_left_garbage(self, left_garbage):
        self.left_garbage = left_garbage

    def get_left_garbage(self):
        return self.left_garbage

    def get_fitness_score(self):
        return self._fitness_score

    def set_fitness_score(self, fitness_score):
        self._fitness_score = fitness_score

    def reset_fitness_score(self):
        self._fitness_score = 0

    def get_life_genaration(self):
        return self.life_genaration

    def increment_life_genaration(self):
        self.life_genaration += 1

    def set_dna_position(self, position, value):
        self._dna[position] = value

    def catch_garbage(self):
        self._fitness_score += 5

    def bad_move(self):
        if self._fitness_score > 0:
            self._fitness_score -= 1  ##numero bad moves

    def __str__(self):
        return f"{self._fitness_score}"


    # def pesos(self):
    #     print(self._dna.weights)
    #     return f"{self._dna.weights}"