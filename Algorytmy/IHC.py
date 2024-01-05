import numpy as np
import pandas as pd

def losowe_rozwiazanie(dane):
    return np.random.permutation(len(dane))

def oblicz_odleglosc(trasa, dane):
    suma = 0
    for i in range(len(trasa) - 1):
        suma += dane.iloc[trasa[i], trasa[i+1]]
    return suma

def wspinaczka_z_multistartem(dane, liczba_startow, liczba_iteracji):
    najlepsza_trasa = None
    najlepsza_odleglosc = float('inf')

    for _ in range(liczba_startow):
        trasa = losowe_rozwiazanie(dane)

        for _ in range(liczba_iteracji):
            nowa_trasa = trasa.copy()
            indeks1, indeks2 = np.random.choice(len(trasa), 2, replace=False)
            nowa_trasa[indeks1], nowa_trasa[indeks2] = nowa_trasa[indeks2], nowa_trasa[indeks1]

            nowa_odleglosc = oblicz_odleglosc(nowa_trasa, dane)
            if nowa_odleglosc < oblicz_odleglosc(trasa, dane):
                trasa = nowa_trasa.copy()

        aktualna_odleglosc = oblicz_odleglosc(trasa, dane)
        if aktualna_odleglosc < najlepsza_odleglosc:
            najlepsza_trasa = trasa.copy()
            najlepsza_odleglosc = aktualna_odleglosc

    return najlepsza_trasa

# Przykładowe dane (ramka danych odległości między miastami)
dane = pd.DataFrame({
    'A': [0, 10, 15, 20],
    'B': [10, 0, 35, 25],
    'C': [15, 35, 0, 30],
    'D': [20, 25, 30, 0]
})

liczba_startow = 5
liczba_iteracji = 1000

najlepsza_trasa = wspinaczka_z_multistartem(dane, liczba_startow, liczba_iteracji)
print("Najlepsza trasa:", najlepsza_trasa)
print("Najlepsza odległość:", oblicz_odleglosc(najlepsza_trasa, dane))