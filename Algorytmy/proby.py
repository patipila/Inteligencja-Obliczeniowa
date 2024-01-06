import pandas as pd
import numpy as np
import random

dane = pd.read_excel("C:/Users/magda/Documents/GitHub/Inteligencja-Obliczeniowa/Dane/Dane_TSP_48k.xlsx", sheet_name="dane", header=None)
dane = dane.iloc[:, 1:]
print(dane)