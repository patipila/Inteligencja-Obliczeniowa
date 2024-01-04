import pandas as pd
import numpy as np
import random
from operator import itemgetter
import time
import xlsxwriter

#Funkcja, która liczy długość patha
def getPathLength(path, distDict):
    length = distDict[f"{path[0]}:{path[-1]}"]
    for i in range(len(path)-1):
        length += distDict[f"{path[i]}:{path[i+1]}"]
    return length

#Zamiana 2 punktów miejscami
def swapPathPoints(path,point1,point2):
    p1Index = path.index(point1)
    p2Index = path.index(point2)
    path[p1Index], path[p2Index] = path[p2Index], path[p1Index]


# odwrócenie ciągu pomiędzy 2 miejscami
def reversePathPart(path, point1, point2):
    p1Index = path.index(point1)
    p2Index = path.index(point2)

    if (p1Index > p2Index):
        p1Index, p2Index = p2Index, p1Index

    reverseLength = int(round(p2Index - p1Index) / 2)

    for i in range(reverseLength):
        path[p1Index + i], path[p2Index - i] = path[p2Index - i], path[p1Index + i]


# Funkcja która oblicza długość patha na podstawie obecnej długości i potencjalnej zmiany.
# Idea tej funkcji obrazkowo https://imgur.com/a/JC1hNfS
def getNewPathLength(path, distDict, currentLength, point1, point2):
    # Znajdujemy indeksy punktów które chcemy zmienić
    p1Index = path.index(point1)
    p2Index = path.index(point2)

    if (p1Index > p2Index):
        p1Index, p2Index = p2Index, p1Index

    # Część z "Wykreślaniem"
    if (p1Index == 0):
        currentLength -= distDict[f"{path[-1]}:{path[p1Index]}"]
    else:
        currentLength -= distDict[f"{path[p1Index - 1]}:{path[p1Index]}"]
    currentLength -= distDict[f"{path[p1Index]}:{path[p1Index + 1]}"]

    if (p2Index == len(path) - 1):
        currentLength -= distDict[f"{path[p2Index]}:{path[0]}"]
    else:
        currentLength -= distDict[f"{path[p2Index]}:{path[p2Index + 1]}"]
    currentLength -= distDict[f"{path[p2Index - 1]}:{path[p2Index]}"]

    path[p1Index], path[p2Index] = path[p2Index], path[p1Index]

    # Część z "Wstawianiem."
    if (p1Index == 0):
        currentLength += distDict[f"{path[-1]}:{path[p1Index]}"]
    else:
        currentLength += distDict[f"{path[p1Index - 1]}:{path[p1Index]}"]
    currentLength += distDict[f"{path[p1Index]}:{path[p1Index + 1]}"]

    if (p2Index == len(path) - 1):
        currentLength += distDict[f"{path[p2Index]}:{path[0]}"]
    else:
        currentLength += distDict[f"{path[p2Index]}:{path[p2Index + 1]}"]
    currentLength += distDict[f"{path[p2Index - 1]}:{path[p2Index]}"]

    path[p1Index], path[p2Index] = path[p2Index], path[p1Index]

    # Zwracamy słownik, który potem trafi do tablicy, w której przechowywać będziemy ewentualne rozwiązania.
    return {"point1": point1, "point2": point2, "length": currentLength}


# Próba napisania funkcji liczącej długość patha po odwróceniu podobnie jak tej z zamiany, niestety nieudana,
# dlatego używam getPathLength(path, distDict), który działa i jest prawdopodobnie dużo bardziej czytelny, natomiast
# ma dużo większą złożoność
def getNewPathLengthReverse(path, distDict, currentLength, point1, point2):
    p1Index = path.index(point1)
    p2Index = path.index(point2)

    if (p1Index > p2Index):
        p1Index, p2Index = p2Index, p1Index

    reversePathPart(path, point1, point2)
    currentLength = getPathLength(path, distDict)
    reversePathPart(path, point1, point2)

    return {"point1": point1, "point2": point2, "length": currentLength}



# Funkcja, która sprawdza, czy ruch jest na liście tabu.
def isMoveOnTabuList(tabuList, possibleMove):
    if (len(tabuList) == 0):
        return False
    point1 = possibleMove['point1']
    point2 = possibleMove['point2']

    for tabuMove in tabuList:
        if tabuMove[0] == point1 and tabuMove[1] == point2 or tabuMove[1] == point1 and tabuMove[0] == point2:
            return True
    return False



#Parametry
#-liczba iteracji
#-Ilość iteracji bez poprawy
#-Długość listy tabu
#-Rodzaj sąsiedztwa
iterationList = [100,250,500,750]
noImprovementList = [4,8,16,""]
tabuListLengths = [3,4,5]
neighborhoodKinds = ["swap", "reverse"]

#Tworzymy tablicę słowników, żeby łatwiej iterować po kombinacjach parametrów
paramCombinations = []
for iteracje in iterationList:
    for warunek_koncowy in noImprovementList:
        for tabu in tabuListLengths:
            for sasiedztwo in neighborhoodKinds:
                paramCombinations.append({'iteracje': iteracje, 'warunek_koncowy': warunek_koncowy, 'tabu': tabu, 'sasiedztwo': sasiedztwo})


#Przygotowanie danych, oraz ich miejsca późniejszego zapisania
file_name, sheet = "C:/Users/emili/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Dane_TSP_48.xlsx", "dane"
excelData = pd.read_excel(file_name, sheet_name = sheet, engine = 'openpyxl')
vals = excelData.values
distDict = {}
for y in range(1,len(vals)+1):
    for x in range(0, len(vals)):
        distDict[f"{x+1}:{y}"] = vals[x,y]

results = []
impBreak = False

for params in paramCombinations:

    # Brak poprawy jako czynnik kończący
    impBreak = "brak"

    currentNoImprovement = 0
    path = list(range(1, len(vals) + 1))

    random.shuffle(path)
    startLength = getPathLength(path, distDict)
    currentLength = startLength
    tabuList = []
    bestPath = {'path': path.copy(), 'length': currentLength}

    for i in range(params['iteracje']):

        if currentNoImprovement == params['warunek_koncowy']:
            impBreak = i
            break

        bestPossibleMoves = [{"point1": 0, "point2": 0, "length": 999999999}] * (params['tabu'] + 1)

        for point1 in range(1, len(path) + 1):
            for point2 in range(point1 + 1, len(path) + 1):

                if (params['sasiedztwo'] == 'swap'):
                    possibleMove = getNewPathLength(path, distDict, currentLength, point1, point2)
                if (params['sasiedztwo'] == 'reverse'):
                    possibleMove = getNewPathLengthReverse(path, distDict, currentLength, point1, point2)
                if possibleMove['length'] > bestPossibleMoves[-1]['length']:
                    continue
                for i in range(len(bestPossibleMoves)):
                    if possibleMove['length'] < bestPossibleMoves[i]['length']:
                        bestPossibleMoves[i] = possibleMove
                        break

        for possibleMove in bestPossibleMoves:
            if not isMoveOnTabuList(tabuList, possibleMove):
                if possibleMove['length'] > currentLength:
                    currentNoImprovement += 1
                else:
                    currentNoImprovement = 0
                tabuList.insert(0, [possibleMove['point1'], possibleMove['point2']])
                if len(tabuList) == params['tabu'] + 1:
                    del tabuList[-1]

                if (params['sasiedztwo'] == 'swap'):
                    swapPathPoints(path, possibleMove['point1'], possibleMove['point2'])
                if (params['sasiedztwo'] == 'reverse'):
                    reversePathPart(path, possibleMove['point1'], possibleMove['point2'])

                currentLength = possibleMove['length']
                if bestPath['length'] > currentLength:
                    bestPath['length'] = currentLength
                    bestPath['path'] = path.copy()
                break

    params['noImprovementIteration'] = impBreak
    results.append({'params': params, 'bestPathLen': bestPath['length'], 'path': bestPath['path']})

# sortowaniee według najlepszej długości ścieżki
results = sorted(results, key=lambda d: d['bestPathLen'])

print("Najlepszy wynik dla 100 iteracji:")
for result in results:
    if result['params']['iteracje'] == 100:
        print("Parametry:", result['params'])
        print("Długość trasy:", result['bestPathLen'])
        print("Trasa:", result['path'])
        break


print("Najlepszy wynik dla 250 iteracji:")
for result in results:
    if result['params']['iteracje'] == 250:
        print("Parametry:", result['params'])
        print("Długość trasy:", result['bestPathLen'])
        print("Trasa:", result['path'])
        break


print("Najlepszy wynik dla 500 iteracji:")
for result in results:
    if result['params']['iteracje'] == 500:
        print("Parametry:", result['params'])
        print("Długość trasy:", result['bestPathLen'])
        print("Trasa:", result['path'])
        break


print("Najlepszy wynik dla 750 iteracji:")
for result in results:
    if result['params']['iteracje'] == 750:
        print("Parametry:", result['params'])
        print("Długość trasy:", result['bestPathLen'])
        print("Trasa:", result['path'])
        break
