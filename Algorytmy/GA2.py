import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

def read_distance_matrix(file_path):
    df = pd.read_excel(file_path, index_col=0)
    return df.values

def initialize_population(population_size, num_cities):
    population = []
    for _ in range(population_size):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

def calculate_fitness(individual, distance_matrix):
    total_distance = 0
    for i in range(len(individual) - 1):
        total_distance += distance_matrix[individual[i], individual[i + 1]]
    total_distance += distance_matrix[individual[-1], individual[0]]
    return 1 / total_distance

def select_parents(population, fitness_scores):
    idx_parent1 = np.random.choice(len(population), p=fitness_scores)
    idx_parent2 = np.random.choice(len(population), p=fitness_scores)
    return population[idx_parent1], population[idx_parent2]

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = [-1] * len(parent1)
    for i in range(crossover_point):
        child[i] = parent1[i]
    idx = crossover_point
    for city in parent2:
        if city not in child:
            child[idx] = city
            idx += 1
    return child

def mutate_swap(individual, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

def mutate_inversion(individual, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        start, end = random.sample(range(len(individual)), 2)
        if start > end:
            start, end = end, start
        individual[start:end + 1] = reversed(individual[start:end + 1])
    return individual


def genetic_algorithm(distance_matrix, population_size, max_generations=1000, max_stagnation=500, mutation_rate=0.1, crossover_rate=0.8, mutation_method=mutate_inversion):
    num_cities = len(distance_matrix)
    population = initialize_population(population_size, num_cities)

    best_individual = None
    best_fitness = 0
    stagnation_counter = 0

    for generation in range(max_generations):
        fitness_scores = [calculate_fitness(individual, distance_matrix) for individual in population]
        fitness_scores = np.array(fitness_scores) / sum(fitness_scores)

        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitness_scores)

            if random.uniform(0, 1) < crossover_rate:
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
            else:
                child1, child2 = parent1[:], parent2[:]

            child1 = mutation_method(child1, mutation_rate)
            child2 = mutation_method(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population

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

    return best_individual, best_fitness

file_path = "Dane/Przykład_TSP_29.xlsx"
distance_matrix = read_distance_matrix(file_path)




population_size = 55
max_generations = 1000000
max_stagnation = 600
mutation_rate = 0.05
crossover_rate = 0.8
mutation_method = mutate_swap    # Wybór jedenj z mutacji:  mutate_swap lub mutate_inversion

best_route, best_fitness = genetic_algorithm(distance_matrix, population_size, max_generations, max_stagnation, mutation_rate, crossover_rate, mutation_method)



# def plot_results(parameter_values, fitness_values, parameter_name):
#     plt.plot(parameter_values, fitness_values, marker='o')
#     plt.title(f"Effect of {parameter_name} on Route Length")
#     plt.xlabel(parameter_name)
#     plt.ylabel("Route Length (Fitness)")
#     plt.show()

# def run_experiment(parameter_values, parameter_name, distance_matrix, max_generations=1000,population_size=5000, max_stagnation=500, mutation_rate=0.1, crossover_rate=0.8, mutation_method=mutate_inversion):
#     fitness_results = []

#     for parameter_value in parameter_values:
#         if parameter_name == "population_size":
#             population_size = parameter_value
#         elif parameter_name == "max_generations":
#             max_generations = parameter_value
#         elif parameter_name == "max_stagnation":
#             max_stagnation = parameter_value
#         elif parameter_name == "mutation_rate":
#             mutation_rate = parameter_value
#         elif parameter_name == "crossover_rate":
#             crossover_rate = parameter_value

#         best_route, best_fitness = genetic_algorithm(distance_matrix, population_size, max_generations, max_stagnation, mutation_rate, crossover_rate, mutation_method)
#         fitness_results.append(best_fitness)

#     plot_results(parameter_values, fitness_results, parameter_name)

# Wczytaj macierz odległości z pliku Excel
# # Parametry eksperymentu
# population_sizes = [1000, 5000, 10000]
# max_generation_values = [10000, 50000, 100000]
# mutation_rates = [0.01, 0.03, 0.05, 0.1]

# # Eksperyment dla rozmiaru populacji
# #run_experiment(population_sizes, "population_size", distance_matrix)

# # Eksperyment dla maksymalnej liczby generacji
# run_experiment(max_generation_values, "max_generations", distance_matrix)

# # Eksperyment dla współczynnika mutacji
# run_experiment(mutation_rates, "mutation_rate", distance_matrix)

print("Najlepsza trasa:", best_route)
print("Najlepsze przystosowanie:", best_fitness)

# Wyświetlenie wyników
print("Miasta po kolei:")
for city in best_route:
    print(city + 1)

# Wyświetlenie odległości między miastami
print("\nOdległości między miastami:")
for i in range(len(best_route) - 1):
    city1, city2 = best_route[i], best_route[i + 1]
    distance = distance_matrix[city1, city2]
    print(distance)

# Dodanie odległość między ostatnim a pierwszym miastem
last_city, first_city = best_route[-1], best_route[0]
distance = distance_matrix[last_city, first_city]
print(distance)

 # Wyświetlenie długość trasy
total_distance = sum(distance_matrix[best_route[i], best_route[i + 1]] for i in range(len(best_route) - 1))
total_distance += distance_matrix[best_route[-1], best_route[0]]  # Wróć do pierwszego miasta
print("Długość trasy:", total_distance)
