import pandas as pd
import numpy as np
import random

def oblicz_odl(kolejnosc, dane):
    suma = 0
    koniec = len(dane)

    for i in range(koniec):
        if i < koniec - 1:
            suma += dane.iloc[kolejnosc[i], kolejnosc[i + 1]]
        else:
            suma += dane.iloc[kolejnosc[i], kolejnosc[0]]

    return float(suma)

def randomowa_kolejnosc(liczba_miast):
    kolejnosc = random.sample(range(liczba_miast), liczba_miast)
    return kolejnosc

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

def hill_climbing_with_multi_start(dane, liczba_iteracji, num_starts):
    liczba_miast = len(dane)
    best_kolejnosc = None
    best_odl = float('inf')

    funkcje_sasiedztwa = {
        'swap': swap,
        'insert': insert,
        'reverse': reverse
    }

    for _ in range(num_starts):
        aktualna_kolejnosc = randomowa_kolejnosc(liczba_miast)
        aktualna_odl = oblicz_odl(aktualna_kolejnosc, dane)

        for _ in range(liczba_iteracji):
            nazwa_sasiedztwa, funkcja_sasiedztwa = random.choice(list(funkcje_sasiedztwa.items()))
            nowa_kolejnosc = funkcja_sasiedztwa(aktualna_kolejnosc)
            nowa_odl = oblicz_odl(nowa_kolejnosc, dane)

            if nowa_odl < aktualna_odl:
                aktualna_kolejnosc = nowa_kolejnosc
                aktualna_odl = nowa_odl

        if aktualna_odl < best_odl:
            best_kolejnosc = aktualna_kolejnosc
            best_odl = aktualna_odl

    return {'kolejnosc': best_kolejnosc, 'odl': best_odl}

# Parametry
distances_data = pd.read_excel("C:/Users/magda/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Przykład_TSP_29.xlsx",header=None)
liczba_iteracji = 10
num_starts = 10

# Implementacja funkcji
for nazwa_sasiedztwa in ['swap', 'insert', 'reverse']:
    print(f"Metoda generowania sąsiedztwa: {nazwa_sasiedztwa}")
    result = hill_climbing_with_multi_start(distances_data, liczba_iteracji, num_starts)
    print(f"Najlepsza kolejnosc: {result['kolejnosc']}")
    print(f"Długość trasy: {result['odl']}\n")

'''
def hill_climbing(dane, liczba_iteracji):
    liczba_miast = len(dane)
    naj_kolejnosc = None
    naj_odl = float('inf')

    for _ in range(liczba_iteracji):
        aktualna_kolejnosc = randomowa_kolejnosc(liczba_miast)
        aktualna_odl = oblicz_odl(aktualna_kolejnosc, dane)

        while True:
            nowa_kolejnosc = randomowa_kolejnosc(liczba_miast)
            nowa_odl = oblicz_odl(nowa_kolejnosc, dane)

            if nowa_odl < aktualna_odl:
                aktualna_kolejnosc = nowa_kolejnosc
                aktualna_odl = nowa_odl
            else:
                break  # Wyjdź z pętli wspinaczki, jeśli nie można poprawić trasy

        if aktualna_odl < naj_odl:
            naj_kolejnosc = aktualna_kolejnosc
            naj_odl = aktualna_odl

    return naj_kolejnosc, naj_odl

# Przykładowe dane - macierz odległości między miastami
dane = pd.read_excel("C:/Users/magda/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Przykład_TSP_29.xlsx",header=None)

liczba_iteracji = 100

# Uruchom algorytm wspinaczki z multistartem
naj_kolejnosc, naj_odl = hill_climbing(dane, liczba_iteracji)

# Wyświetl wyniki
print("Najlepsza kolejnosc:", naj_kolejnosc)
print("Długość trasy:", naj_odl)
'''