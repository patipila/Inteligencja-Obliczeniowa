import pandas as pd
import numpy as np
import random

def read_distances_from_csv(file_path):
    distances = pd.read_excel(file_path, header=0)
    return distances

def total_distance(route, distances):
    total_distance = 0
    num_cities = len(route)
    for i in range(num_cities - 1):
        total_distance += distances.iloc[route[i], route[i + 1]]
    total_distance += distances.iloc[route[num_cities - 1], route[0]]  # powrót do pierwszego miasta
    return total_distance

def random_route(num_cities):
    route = random.sample(range(1, num_cities + 1), num_cities)
    return route

def swap(seq):
    swap_indices = random.sample(range(len(seq)), 2)
    new_seq = seq.copy()
    new_seq[swap_indices[0]], new_seq[swap_indices[1]] = new_seq[swap_indices[1]], new_seq[swap_indices[0]]
    return new_seq

def insert(seq):
    insertion_indices = sorted(random.sample(range(len(seq)), 2))
    moved_city = seq.pop(insertion_indices[0])
    seq.insert(insertion_indices[1] - 1, moved_city)
    return seq

def reverse(seq):
    reverse_indices = sorted(random.sample(range(len(seq)), 2))
    new_seq = seq.copy()
    new_seq[reverse_indices[0]:reverse_indices[1] + 1] = reversed(new_seq[reverse_indices[0]:reverse_indices[1] + 1])
    return new_seq

def hill_climbing_with_multi_start(distances, num_iterations, num_starts):
    num_cities = len(distances)
    best_route = None
    best_distance = float('inf')

    neighborhood_functions = {
        'swap': swap,
        'insert': insert,
        'reverse': reverse
    }

    for _ in range(num_starts):
        current_route = random_route(num_cities)
        current_distance = total_distance(current_route, distances)

        for _ in range(num_iterations):
            neighborhood_name, neighborhood_function = random.choice(list(neighborhood_functions.items()))
            new_route = neighborhood_function(current_route)
            new_distance = total_distance(new_route, distances)

            if new_distance < current_distance:
                current_route = new_route
                current_distance = new_distance

        if current_distance < best_distance:
            best_route = current_route
            best_distance = current_distance

    return {'route': best_route, 'distance': best_distance}

# Parametry
csv_file_path = "C:/Users/magda/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Dane_TSP_48.xlsx"
distances_data = read_distances_from_csv(csv_file_path)
max_iterations_per_start = 10000
num_starts = 100

# Implementacja funkcji
for neighborhood_name in ['swap', 'insert', 'reverse']:
    print(f"Metoda generowania sąsiedztwa: {neighborhood_name}")
    result = hill_climbing_with_multi_start(distances_data, max_iterations_per_start, num_starts)
    print(f"Najlepsza trasa: {result['route']}")
    print(f"Długość trasy: {result['distance']}\n")