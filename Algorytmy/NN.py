import pandas as pd
import numpy as np
import random

def losowe_miasto_startowe(dane):
    return np.random.randint(0, len(dane))

def oblicz_odl(kolejnosc, dane):
    suma = 0
    koniec = len(dane)

    for i in range(koniec):
        if i < koniec - 1:
            suma += dane.iloc[kolejnosc[i], kolejnosc[i + 1]]
        else:
            suma += dane.iloc[kolejnosc[i], kolejnosc[0]]

    return float(suma)

def najblizszy_sasiad(dane, start):
    kolejnosc = [start]
    miasto = start

    for _ in range(1, len(dane)):
        dostepne_indeksy = [idx for idx in range(len(dane)) if idx not in kolejnosc]
        if not dostepne_indeksy:
            break

        indeks_najblizszego = min(dostepne_indeksy, key=lambda idx: dane.iloc[miasto, idx])
        kolejnosc.append(indeks_najblizszego)
        miasto = indeks_najblizszego

    # Dodaj powrót do punktu początkowego
    kolejnosc.append(kolejnosc[0])
    

    return kolejnosc

dane = pd.read_excel("C:/Users/magda/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Dane_TSP_48k.xlsx",header=None)
start = losowe_miasto_startowe(dane)
trasa = najblizszy_sasiad(dane, start)
odleglosc = oblicz_odl(trasa, dane)

print("Trasa:", trasa)
print("Odleglosc:", odleglosc)



