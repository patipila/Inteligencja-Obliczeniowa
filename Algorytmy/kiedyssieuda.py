import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


def read_distance_matrix(file_path):
    df = pd.read_excel(file_path, index_col=0)
    return df.values


def calculate_distance(individual, distance_matrix):
    total_distance = 0
    for i in range(len(individual) - 1):
        total_distance += distance_matrix[individual[i], individual[i + 1]]
    total_distance += distance_matrix[individual[-1], individual[0]]
    return float(total_distance)


def calculate_fitness(individual, distance_matrix):
    total_distance = calculate_distance(individual, distance_matrix)
    return 1 / total_distance


def tournament_selection(population, distance_matrix):
    parents = list()

    for _ in range(2):
        indices = random.sample(range(0, len(population)), 2)
        participants = [population[i] for i in indices]
        parents.append(min(participants, key=lambda ind: calculate_distance(ind, distance_matrix)))
    return parents


def rank_selection(population, distance_matrix):
    population_copy = population.copy()
    parents = list()

    ranks = list(range(len(population_copy)))
    ranks.sort(key=lambda x: calculate_distance(population_copy[x], distance_matrix))

    for _ in range(2):
        selected_index = random.choice(ranks)
        parents.append(population_copy[selected_index])
        ranks.remove(selected_index)

    return parents



def roulette_selection(population, distance_matrix):
    fitness_scores = [calculate_fitness(individual, distance_matrix) for individual in population]
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]

    parents_indices = np.random.choice(range(len(population)), size=2, replace=False, p=probabilities)
    parents = [population[i] for i in parents_indices]

    return parents


def crossover_PMX(parent1, parent2):
    size = len(parent1)
    crossover_point1 = random.randint(0, size - 1)
    crossover_point2 = random.randint(crossover_point1 + 1, size)

    child = [-1] * size
    mapping = {parent2[i]: parent1[i] for i in range(crossover_point1, crossover_point2)}
    child[crossover_point1:crossover_point2] = parent2[crossover_point1:crossover_point2]

    for i in range(size):
        if child[i] == -1:
            current_city = parent2[i]
            while current_city in mapping:
                current_city = mapping[current_city]
            child[i] = current_city

    return child


def crossover_OX(parent1, parent2):
    crossover_point1 = random.randint(0, len(parent1) - 1)
    crossover_point2 = random.randint(crossover_point1 + 1, len(parent1))
    child = [-1] * len(parent1)

    child[crossover_point1:crossover_point2] = parent1[crossover_point1:crossover_point2]

    idx = crossover_point2
    for city in parent2[crossover_point2:] + parent2[:crossover_point2]:
        if city not in child:
            child[idx % len(parent1)] = city
            idx += 1

    return child


def mutate_swap(individual, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual


def mutate_reversed(individual, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        start, end = random.sample(range(len(individual)), 2)
        if start > end:
            start, end = end, start
        individual[start:end + 1] = reversed(individual[start:end + 1])
    return individual


def initialize_population(population_size, num_cities):
    population = []
    for _ in range(population_size):
        route = list(np.random.permutation(num_cities))
        population.append(route)

    return population  


# Define a function to select parents based on the selection type
def select_parents(population, distance_matrix, selection_type):
    if selection_type == 'tournament':
        return tournament_selection(population, distance_matrix)
    elif selection_type == 'rank':
        return rank_selection(population, distance_matrix)
    elif selection_type == 'roulette':
        return roulette_selection(population, distance_matrix)
    else:
        raise ValueError("Invalid selection type. Supported types: 'tournament', 'rank', 'roulette'.")

# Define a function to perform crossover based on the crossover type
def crossover_type(parent1, parent2, crossover_type):
    if crossover_type == 'PMX':
        return crossover_PMX(parent1, parent2)
    elif crossover_type == 'OX':
        return crossover_OX(parent1, parent2)
    else:
        raise ValueError("Invalid crossover type. Supported types: 'PMX', 'OX'.")

# Define a function to perform mutation based on the mutation type
def mutate_type(individual, mutation_rate, mutation_type):
    if mutation_type == 'swap':
        return mutate_swap(individual, mutation_rate)
    elif mutation_type == 'reversed':
        return mutate_reversed(individual, mutation_rate)
    else:
        raise ValueError("Invalid mutation type. Supported types: 'swap', 'reversed'.")


def remove_worst_individuals(population, distance_matrix):
    distances = [calculate_distance(individual, distance_matrix) for individual in population]
    for _ in range(2):
        worst_index=distances.index(max(distances))
        del population[worst_index]
        del distances[worst_index]
    return population



def genetic_algorithm(distance_matrix, population_size, generations, crossover_rate, mutation_rate, selection_type, crossover_method, mutation_type,max_stagnation=500):
    num_cities = len(distance_matrix)
    population = initialize_population(population_size, num_cities)

    best_individual = None
    best_fitness = 0
    stagnation_counter = 0

    for g in range(generations):
        fitness_scores = [calculate_fitness(individual, distance_matrix) for individual in population]
        fitness_scores = np.array(fitness_scores) / sum(fitness_scores)
        
        new_population = population.copy()

        parents = select_parents(population, distance_matrix, selection_type)
        parent1, parent2 = parents
        if random.uniform(0, 1) < crossover_rate:
            child1, child2 = crossover_type(parent1, parent2,crossover_method), crossover_type(parent2, parent1,crossover_method)
        else:
            child1, child2 = parent1[:], parent2[:]

        child1 = mutate_type(child1, mutation_rate, mutation_type)
        child2 = mutate_type(child2, mutation_rate, mutation_type)
        
        new_population.extend([child1, child2])

        population = remove_worst_individuals(new_population, distance_matrix)

        current_best_individual = max(population, key=lambda x: calculate_fitness(x, distance_matrix))
        current_best_fitness = calculate_fitness(current_best_individual, distance_matrix)

        if current_best_fitness > best_fitness:
            best_individual = current_best_individual
            best_fitness = current_best_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if stagnation_counter >= max_stagnation:
           break
        print(g,"-",calculate_distance(best_individual, distance_matrix))
        
    return best_individual, best_fitness


def print_route(route, distance_matrix):
    total_distance = calculate_distance(route, distance_matrix)
    print("Order of Cities:", [city + 1 for city in route]) 
    print("Total Distance:", total_distance)
    

# Example usage:
file_path = "Dane/Dane_TSP_127.xlsx"
distance_matrix = read_distance_matrix(file_path)

population_size = 50
generations = 1000000
crossover_rate = 0.4
mutation_rate = 0.1
selection_type = 'tournament'  # or 'rank', 'roulette'
crossover_method = 'PMX'  # or crossover_OX
mutation_type = 'swap'  # or 'reversed'
max_stagnation=100000

df_distance = pd.DataFrame(columns=['Distance'])
df_cities=pd.DataFrame()
save_file_name = '127_pop%s_gen%s_mutat_rate%s_cross_rate%s_mutat_type%s_cross_type%s.xlsx' % (
    population_size,generations, mutation_rate, crossover_rate, mutation_type, crossover_method
)

for i in range(1,11):
    best_individual = genetic_algorithm(distance_matrix, population_size, generations, crossover_rate, mutation_rate, selection_type, crossover_method, mutation_type, max_stagnation)
    print_route(best_individual[0], distance_matrix)
    total_distance= calculate_distance(best_individual[0], distance_matrix)
    df_distance.loc[i]= total_distance
    df_cities[i]= [city + 1 for city in best_individual[0]]

print(df_distance)

with pd.ExcelWriter("Wyniki_GA/127/"+save_file_name) as writer:
    df_distance.to_excel(writer, sheet_name='Distance', index=True)
    df_cities.to_excel(writer, sheet_name='Route', index=False)