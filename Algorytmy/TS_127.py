import pandas as pd
import numpy as np
import random
from operator import itemgetter
import time
import xlsxwriter

# Funkcja, która liczy długość ścieżki
def getPathLength(path, distDict):
    length = distDict[f"{path[0]}:{path[-1]}"]
    for i in range(len(path)-1):
        length += distDict[f"{path[i]}:{path[i+1]}"]
    return length

# Zamiana 2 punktów miejscami - swap
def swapPath(path,point1,point2):
    p1Index = path.index(point1)
    p2Index = path.index(point2)
    path[p1Index], path[p2Index] = path[p2Index], path[p1Index]


# Odwrócenie ciągu pomiędzy 2 punktami - reverse
def reversePath(path, point1, point2):
    p1Index = path.index(point1)
    p2Index = path.index(point2)

    if (p1Index > p2Index):
        p1Index, p2Index = p2Index, p1Index

    reverseLength = int(round(p2Index - p1Index) / 2)

    for i in range(reverseLength):
        path[p1Index + i], path[p2Index - i] = path[p2Index - i], path[p1Index + i]


# Funkcja która oblicza długość ścieżki na podstawie obecnej długości i potencjalnej zmiany.
def getNewPathLength(path, distDict, currentLength, point1, point2):

    p1Index = path.index(point1)
    p2Index = path.index(point2)

    if (p1Index > p2Index):
        p1Index, p2Index = p2Index, p1Index

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

    # Zwracamy słownik, który potem trafi do tablicy, w której przechowywać będziemy rozwiązania.
    return {"point1": point1, "point2": point2, "length": currentLength}


def getNewPathLengthReverse(path, distDict, currentLength, point1, point2):
    p1Index = path.index(point1)
    p2Index = path.index(point2)

    if (p1Index > p2Index):
        p1Index, p2Index = p2Index, p1Index

    reversePath(path, point1, point2)
    currentLength = getPathLength(path, distDict)
    reversePath(path, point1, point2)

    return {"point1": point1, "point2": point2, "length": currentLength}



# Funkcja, która sprawdza, czy ruch jest na liście tabu
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
iterationList = [100,250,500,750]
noImprovementList = [4,8,16,""]
tabuListLengths = [3,4,5,8]
neighborhoodKinds = ["swap", "reverse"]

#Tworzymy tablicę słowników
paramCombinations = []
for iteracje in iterationList:
    for warunek_koncowy in noImprovementList:
        for tabu in tabuListLengths:
            for sasiedztwo in neighborhoodKinds:
                paramCombinations.append({'iteracje': iteracje, 'warunek_koncowy': warunek_koncowy, 'tabu': tabu, 'sasiedztwo': sasiedztwo})


#Przygotowanie danych, oraz ich miejsca późniejszego zapisania
file_name, sheet = "C:/Users/emili/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Dane_TSP_127.xlsx", "Arkusz1"
excelData = pd.read_excel(file_name, sheet_name = sheet, engine = 'openpyxl')
vals = excelData.values
distDict = {}
for y in range(1,len(vals)+1):
    for x in range(0, len(vals)):
        distDict[f"{x+1}:{y}"] = vals[x,y]

results = []
impBreak = False


# Tabu Search

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
                    swapPath(path, possibleMove['point1'], possibleMove['point2'])
                if (params['sasiedztwo'] == 'reverse'):
                    reversePath(path, possibleMove['point1'], possibleMove['point2'])

                currentLength = possibleMove['length']
                if bestPath['length'] > currentLength:
                    bestPath['length'] = currentLength
                    bestPath['path'] = path.copy()
                break

    params['noImprovementIteration'] = impBreak
    results.append({'params': params, 'bestPathLen': bestPath['length'], 'path': bestPath['path']})

# Sortowaniee według najlepszej długości ścieżki
results = sorted(results, key=lambda d: d['bestPathLen'])


# Zapisywanie do pliku xlsx
swapTime = 0
revTime = 0
pathLen = len(','.join(str(point) for point in results[0]['path']))
pathLen = int(0.85 * pathLen)
workbook = xlsxwriter.Workbook(f"wyniki_TS_127")
worksheet = workbook.add_worksheet()
worksheet.set_column(6, 6, pathLen)

row = 1
for res in results:
    worksheet.write(row, 0, res['params']['iteracje'])
    worksheet.write(row, 1, res['params']['warunek_koncowy'])
    worksheet.write(row, 2, res['params']['tabu'])
    worksheet.write(row, 3, res['params']['sasiedztwo'])
    worksheet.write(row, 4, res['bestPathLen'])
    worksheet.write(row, 5, ','.join(str(point) for point in res['path']))
    row += 1

workbook.close()