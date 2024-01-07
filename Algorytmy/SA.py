import numpy as np
import pandas as pd
import random
import math

# Funkcja obliczająca długość trasy
def calculate_distance(route, data):
    distance = 0
    for i in range(len(route) - 1):
        distance += data.iloc[route[i], route[i + 1]]
    return distance + data.iloc[route[-1], route[0]]  # Wróć do punktu początkowego


# Funkcja sąsiedztwa I
def neighborhood_type_I(route):
    new_route = route.copy()
    i, j = random.sample(range(len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route


# Funkcja sąsiedztwa II
def neighborhood_type_II(route):
    new_route = route.copy()
    i = random.randint(0, len(route) - 1)
    j = (i + 1) % len(route)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route


# Implementacja algorytmu SA
def simulated_annealing(data, neighborhood_func, iterations, initial_temperature, alpha, reduction_method):
    n = len(data)
    current_route = list(range(n))
    random.shuffle(current_route)
    current_distance = calculate_distance(current_route, data)

    best_route = current_route.copy()
    best_distance = current_distance

    for iteration in range(iterations):
        if reduction_method == 'GEOMETRIC':
            temperature = initial_temperature * (alpha ** iteration)
        elif reduction_method == 'LINEAR':
            temperature = initial_temperature / (1 + alpha * iteration)

        new_route = neighborhood_func(current_route)
        new_distance = calculate_distance(new_route, data)

        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_route = new_route.copy()
            current_distance = new_distance

            if new_distance < best_distance:
                best_route = new_route.copy()
                best_distance = new_distance

    return best_route, best_distance


# Wprowadzenie danych od użytkownika
path = input("Podaj ścieżkę do pliku Excel z danymi: ")
data = pd.read_excel(path, index_col=0)

neighborhood_choice = input("Wybierz rodzaj sąsiedztwa (I/II): ").upper()
neighborhood_func = neighborhood_type_I if neighborhood_choice == 'I' else neighborhood_type_II

iterations = int(input("Podaj liczbę iteracji: "))
initial_temperature = float(input("Podaj początkową temperaturę: "))

reduction_method = input("Wybierz metodę redukcji temperatury (GEOMETRIC/LINEAR): ").upper()

alpha = float(input("Podaj wartość mnożnika redukcji: "))

# Wykonanie algorytmu SA
best_route, best_distance = simulated_annealing(data, neighborhood_func, iterations, initial_temperature, alpha, reduction_method)

# Wyświetlenie wyników
print(f"Najlepsza trasa: {best_route}")
print(f"Długość najlepszej trasy: {best_distance}")
