from Gene import Gene
import random
from Neuralnetwork import *
from typing import Tuple, List, Union, Optional

# Constants used in the genetic algorithm.
NUM_OF_GENES = 1500  # -> Population
DNA_SIZE = 30  # -> Number of moves  #apagar
NUM_OF_GENERATIONS = 50  # -> Number of generations
TOP_GENES = 3  # -> Top genes to be selected for crossover apagar
MUTATION_RATE = 0.02  # apagar
MAX_LIFE_GENERATION = 100  # apagar
CROSSOVER_K_POINTS = 1   # apagar



def create_inital_genes():  ## inicia o tabuleiro.
    population = []
    for _ in range(NUM_OF_GENES):
        population.append(Gene())
    return population


def simulated_binary_crossover(parent1: np.ndarray, parent2: np.ndarray, eta: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    This crossover is specific to floating-point representation.
    Simulate behavior of one-point crossover for binary representations.

    For large values of eta there is a higher probability that offspring will be created near the parents.
    For small values of eta, offspring will be more distant from parents

    Equation 9.9, 9.10, 9.11
    @TODO: Link equations
    """
    # Calculate Gamma (Eq. 9.11)
    rand = np.random.random(parent1.shape)
    gamma = np.empty(parent1.shape)
    gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (eta + 1))  # First case of equation 9.11
    gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (eta + 1))  # Second case

    # Calculate Child 1 chromosome (Eq. 9.9)
    chromosome1 = 0.5 * ((1 + gamma) * parent1 + (1 - gamma) * parent2)
    # Calculate Child 2 chromosome (Eq. 9.10)
    chromosome2 = 0.5 * ((1 - gamma) * parent1 + (1 + gamma) * parent2)


    return chromosome1, chromosome2


def single_point_binary_crossover(parent1: np.ndarray, parent2: np.ndarray, major='r') -> Tuple[np.ndarray, np.ndarray]:
    offspring1 = parent1.copy()
    offspring2 = parent2.copy()  # meter "universal" para todos 1,2,3,4,5,w's
    ###onde fazer o corte??
    rows, cols = parent2.shape
    row = np.random.randint(0, rows)
    col = np.random.randint(0, cols)

    if major.lower() == 'r':  ###########o que é o major????
        offspring1[:row, :] = parent2[:row, :]
        offspring2[:row, :] = parent1[:row, :]

        offspring1[row, :col + 1] = parent2[row, :col + 1]
        offspring2[row, :col + 1] = parent1[row, :col + 1]
    elif major.lower() == 'c':
        offspring1[:, :col] = parent2[:, :col]
        offspring2[:, :col] = parent1[:, :col]

        offspring1[:row + 1, col] = parent2[:row + 1, col]
        offspring2[:row + 1, col] = parent1[:row + 1, col]

    return offspring1, offspring2


def crossover(parent1_weights: np.ndarray, parent2_weights: np.ndarray,
              parent1_bias: np.ndarray, parent2_bias: np.ndarray) -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    _crossover_bins = np.cumsum([0.5, 0.5])
    _SBX_eta = 100
    _SPBX_type = 'r'
    rand_crossover = random.random()
    # crossover_bucket = np.digitize(rand_crossover, _crossover_bins)
    crossover_bucket = 0

    # SBX
    if crossover_bucket == 0:
        child1_weights, child2_weights = simulated_binary_crossover(parent1_weights, parent2_weights, _SBX_eta)
        child1_bias, child2_bias = simulated_binary_crossover(parent1_bias, parent2_bias, _SBX_eta)
    # Single point binary crossover (SPBX)
    elif crossover_bucket == 1:
        child1_weights, child2_weights = single_point_binary_crossover(parent1_weights, parent2_weights,
                                                                       major=_SPBX_type)
        child1_bias, child2_bias = single_point_binary_crossover(parent1_bias, parent2_bias, major=_SPBX_type)

    else:
        raise Exception('Unable to determine valid crossover based off probabilities')

    return child1_weights, child2_weights, child1_bias, child2_bias


def gaussian_mutation(chromosome: np.ndarray, prob_mutation: float,
                      mu: List[float] = None, sigma: List[float] = None,
                      scale: Optional[float] = None) -> np.ndarray:
    """
    Perform a gaussian mutation for each gene in an individual with probability, prob_mutation.

    If mu and sigma are defined then the gaussian distribution will be drawn from that,
    otherwise it will be drawn from N(0, 1) for the shape of the individual.
    """
    # Determine which genes will be mutated
    mutation_array = np.random.random(chromosome.shape) < prob_mutation
    # If mu and sigma are defined, create gaussian distribution around each one
    if mu and sigma:
        gaussian_mutation = np.random.normal(mu, sigma)
    # Otherwise center around N(0,1)
    else:
        gaussian_mutation = np.random.normal(size=chromosome.shape)

    if scale:
        gaussian_mutation[mutation_array] *= scale

    # Update
    chromosome[mutation_array] += gaussian_mutation[mutation_array]

    return chromosome


def random_uniform_mutation(chromosome: np.ndarray, prob_mutation: float,
                            low: Union[List[float], float],
                            high: Union[List[float], float]
                            ) -> np.ndarray:
    """
    Randomly mutate each gene in an individual with probability, prob_mutation.
    If a gene is selected for mutation it will be assigned a value with uniform probability
    between [low, high).

    @Note [low, high) is defined for each gene to help get the full range of possible values
    @TODO: Eq 11.4
    """
    assert type(low) == type(high), 'low and high must have the same type'
    mutation_array = np.random.random(chromosome.shape) < prob_mutation
    if isinstance(low, list):
        uniform_mutation = np.random.uniform(low, high)
    else:
        uniform_mutation = np.random.uniform(low, high, size=chromosome.shape)
    chromosome[mutation_array] = uniform_mutation[mutation_array]

    return chromosome


def mutate(child1_weights: np.ndarray, child2_weights: np.ndarray,
           child1_bias: np.ndarray, child2_bias: np.ndarray) -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    scale = .2
    rand_mutation = random.random()
    _mutation_bins = np.cumsum([1.0, 0.0])
    mutation_bucket = np.digitize(rand_mutation, _mutation_bins)

    mutation_rate = 0.05
    # if 'static'.lower() == 'decaying':
    #   mutation_rate = mutation_rate / sqrt(current_generation + 1)

    # Gaussian
    if mutation_bucket == 0:
        # Mutate weights
        child1_weights = gaussian_mutation(child1_weights, mutation_rate, scale=scale)
        child2_weights = gaussian_mutation(child2_weights, mutation_rate, scale=scale)

        # Mutate bias
        child1_bias = gaussian_mutation(child1_bias, mutation_rate, scale=scale)
        child2_bias = gaussian_mutation(child2_bias, mutation_rate, scale=scale)

    # Uniform random
    elif mutation_bucket == 1:
        # Mutate weights
        child1_weights = random_uniform_mutation(child1_weights, mutation_rate, -1, 1)
        child2_weights = random_uniform_mutation(child2_weights, mutation_rate, -1, 1)

        # Mutate bias
        child1_bias = random_uniform_mutation(child1_bias, mutation_rate, -1, 1)
        child2_bias = random_uniform_mutation(child2_bias, mutation_rate, -1, 1)

    return child1_weights, child2_weights, child1_bias, child2_bias


def elitism_selection(population, num_individuals: int):
    individuals = sorted(population, key=lambda individual: individual.fitness, reverse=True)
    return individuals[:num_individuals]


def roulette_wheel_selection(population: List[Gene], num_individuals: int) -> list[Gene]:
    selection = []
    wheel = sum(individual.get_fitness_score() for individual in population)
    for _ in range(num_individuals):
        pick = random.uniform(0, wheel)
        current = 0
        for individual in population:
            # current += individual['fitness']
            current += individual.get_fitness_score()
            if current > pick:
                selection.append(individual)
                break

    return selection




###########################NOVA---NOVA---NOVA---NOVA----NOVA##################################
def generate_next_generation(population):  # NUM_OF_GENES  ##filtar 500 new_pop

    population.sort(key=lambda individual: individual.get_fitness_score(), reverse=True)
    next_generation = population[:500]

    # # nova list que retorna no final
    # next_generation = []
    # ordenar = []
    # # ordenar populaçao anterior
    # for individual in population:
    #     ordenar.append(individual.get_fitness_score())
    # lista_ordenada = sorted(ordenar, reverse=True)
    #
    # # ir buscar os genes com maior score
    # for score in lista_ordenada[:5]:
    #     for individual in population:
    #         if individual.get_fitness_score() == score:
    #             next_generation.append(individual)

    print("123456789", next_generation)

    # dos top fazer filhos ate chegar NUM_GENES
    print(len(next_generation), NUM_OF_GENES)
    gg = 1

    while len(next_generation) < NUM_OF_GENES:
        p1, p2 = roulette_wheel_selection(population, 2)
        c1_data= {
            'w':[], 'b':[]
        }
        c2_data = {
            'w': [], 'b': []
        }

        for p1_W, p2_W, p1_b, p2_b in zip(p1.get_dna().weights, p2.get_dna().weights, p1.get_dna().bias,
                                          p2.get_dna().bias):
            print(f"antes_cross: p1_W shape: {np.shape(p1_W)}, p2_W shape: {np.shape(p2_W)}, p1_b shape: {np.shape(p1_b)}, p2_b shape: {np.shape(p2_b)}")

            c1_W, c2_W, c1_b, c2_b = crossover(p1_W, p2_W, p1_b, p2_b)
            print(f"depois_cross: p1_W shape: {np.shape(c1_W)}, p2_W shape: {np.shape(c2_W)}, p1_b shape: {np.shape(c1_b)}, p2_b shape: {np.shape(c2_b)}")

            # gg = 1
            c1_W, c2_W, c1_b, c2_b = mutate(c1_W, c2_W, c1_b, c2_b)
            print(f"depois_muta: p1_W shape: {np.shape(c1_W)}, p2_W shape: {np.shape(c2_W)}, p1_b shape: {np.shape(c1_b)}, p2_b shape: {np.shape(c2_b)}")

            c1_data['w'].append(c1_W)
            c2_data['w'].append(c2_W)
            c1_data['b'].append(c1_b)
            c2_data['b'].append(c2_b)

            # print(f"c1_data['w']: {c1_data['w']}, shape: {np.shape(c1_data['w'])}")
            # print(f"c2_data['w']: {c2_data['w']}, shape: {np.shape(c2_data['w'])}")

        c1 = Gene()
        c2 = Gene()
        c1.get_dna().weights = np.array(c1_data['w'], dtype=object)
        c1.get_dna().bias = np.array(c1_data['b'], dtype=object)
        c2.get_dna().weights = np.array(c2_data['w'], dtype=object)
        c2.get_dna().bias = np.array(c2_data['b'], dtype=object)



        # print("ola123,", (c1.get_dna().weights))

        next_generation.append(c1)
        next_generation.append(c2)

    # a = next_generation[0]._dna.weights
    # b = next_generation[-1]._dna.weights
    gg = 1
    return next_generation

