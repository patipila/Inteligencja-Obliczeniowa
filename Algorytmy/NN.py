import pandas as pd
import numpy as np
import random

def losowe_miasto_startowe(dane):
    return random.randint(0, dane.shape[0] - 1)

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
    poczatkowe_dane = dane.copy()
    dane[dane == 0] = np.nan
    kolejnosc = [None] * len(dane)
    kolejnosc[0] = start
    miasto = start

    for _ in range(2, dane.shape[0] + 1):
        dostepne_indeksy = dane.index[dane.index.notna()]  # Pobierz dostępne indeksy
        dostepne_indeksy = dostepne_indeksy.difference(kolejnosc)  # Usuń już użyte indeksy

        if dostepne_indeksy.empty:
            break  # Wyjdź z pętli, jeśli wszystkie indeksy zostały już użyte
        

        kolejnosc.append(int(dane.loc[miasto, dostepne_indeksy].idxmin()))
        miasto = kolejnosc[-1]

    wynik = pd.DataFrame(kolejnosc, columns=['Miasto'])
    wynik.loc[1] = oblicz_odl(kolejnosc, poczatkowe_dane)
    
    return wynik

# Wczytaj plik Excel
dane = pd.read_excel("C:/Users/magda/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Dane_TSP_48.xlsx", sheet_name="dane", header=None)

# Usuń pierwszą kolumnę
dane = dane.iloc[:, 1:]

# Przykładowe użycie:
losowe_start = losowe_miasto_startowe(dane)
nn_result = najblizszy_sasiad(dane, losowe_start)

# Zapisz wynik do pliku Excel
nn_result.to_excel("NN_48.xlsx", index=False)


#czat
import numpy as np
import pandas as pd

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

# Przykładowe dane (ramka danych odległości między miastami)
#
 #   'A': [0, 10, 15, 20],
 #   'B': [10, 0, 35, 25],
 #   'C': [15, 35, 0, 30],
 #   'D': [20, 25, 30, 0]
#})

dane = pd.read_excel("C:/Users/magda/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Dane_TSP_48.xlsx",header=None)
start = losowe_miasto_startowe(dane)
trasa = najblizszy_sasiad(dane, start)
odleglosc = oblicz_odl(trasa, dane)

print("Trasa:", trasa)
print("Odleglosc:", odleglosc)

#kajetan
import numpy as np
import pandas as pd

def NN(dataMatrix, start, route=None):
    if route is None:
        route = []
        route.append(start)
        return NN(dataMatrix, start, route)
    else:
        if len(route) < len(dataMatrix):
            notVisitedCities = [i for i in range(len(dataMatrix)) if i not in route]
            lastCity = route[-1]
            distances = []
            for i in notVisitedCities:
                distances.append(dataMatrix[lastCity][i])
            nearestCity = notVisitedCities[np.argmin(distances)]
            route.append(nearestCity)
            return NN(dataMatrix, start, route)
        else:
            return route
        
def NNAll(dataMatrix):
    bestRoute = []
    bestDistance = 0
    for i in range(len(dataMatrix)):
        route = NN(dataMatrix, i)
        distance = 0
        for j in range(len(route) - 1):
            distance += dataMatrix[route[j]][route[j + 1]]
        distance += dataMatrix[route[-1]][route[0]]
        if bestDistance == 0 or distance < bestDistance:
            bestDistance = distance
            bestRoute = route
    return bestRoute, bestDistance      

dataMatrix = pd.read_excel("C:/Users/magda/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Dane_TSP_48.xlsx",header=None)
dataMatrix.head()

route, distance = NNAll(dataMatrix)
print("Najlepsza trasa: ", route)
print("Długość trasy: ", distance)


