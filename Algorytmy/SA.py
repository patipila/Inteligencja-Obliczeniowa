import pandas as pd
import numpy as np
import random
import math

# Wczytaj dane z pliku Excel
data = pd.read_excel("/Users/aleksandrapalka/Desktop/Inteligencja-Obliczeniowa/Dane/Dane_TSP_48.xlsx",
                     sheet_name="dane")
cities = data.iloc[:, 1:].values  # Pomijamy pierwszą kolumnę i wiersz


# Funkcja obliczająca koszt ścieżki
def calculate_cost(solution):
    total_distance = 0
    for i in range(len(solution) - 1):
        total_distance += cities[solution[i] - 1, solution[i + 1] - 1]
    total_distance += cities[solution[-1] - 1, solution[0] - 1]
    return total_distance


# Trzy różne strategie generowania sąsiednich rozwiązań
def generate_neighbor_swap(solution):
    new_solution = solution[:]
    idx1, idx2 = random.sample(range(len(new_solution)), 2)
    new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]
    return new_solution


def generate_neighbor_reverse(solution):
    new_solution = solution[:]
    start, end = random.sample(range(len(new_solution)), 2)
    if start > end:
        start, end = end, start
    new_solution[start:end + 1] = reversed(new_solution[start:end + 1])
    return new_solution


def generate_neighbor_shift(solution):
    new_solution = solution[:]
    start, end = random.sample(range(len(new_solution)), 2)
    segment = new_solution[start:end + 1]
    del new_solution[start:end + 1]
    pos = random.randint(0, len(new_solution))
    new_solution = new_solution[:pos] + segment + new_solution[pos:]
    return new_solution


# Algorytm Symulowanego Wyżarzania z trzema strategiami sąsiednich rozwiązań
def simulated_annealing(initial_solution, temperature, cooling_rate, iterations):
    current_solution = initial_solution[:]
    current_cost = calculate_cost(current_solution)

    best_solution = current_solution[:]
    best_cost = current_cost

    for i in range(iterations):
        # Wybór strategii generowania sąsiedniego rozwiązania
        strategy = random.choice([generate_neighbor_swap, generate_neighbor_reverse, generate_neighbor_shift])
        new_solution = strategy(current_solution)

        new_cost = calculate_cost(new_solution)

        # Akceptacja nowego rozwiązania
        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
            current_solution = new_solution[:]
            current_cost = new_cost

            if new_cost < best_cost:
                best_solution = new_solution[:]
                best_cost = new_cost

        # Obniżanie temperatury
        temperature *= cooling_rate

    return best_solution, best_cost


# Parametry SA
initial_solution = list(range(1, 49))  # początkowe rozwiązanie
initial_temperature = 1000.0
cooling_rate = 0.995
iterations = 10000

# Uruchomienie algorytmu
best_solution, best_cost = simulated_annealing(initial_solution, initial_temperature, cooling_rate, iterations)

# Wyświetlenie wyników
print(f"Najlepsze rozwiązanie: {best_solution}")
print(f"Koszt najlepszego rozwiązania: {best_cost}")



