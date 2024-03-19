"""Zadanie z kreślenia wykresów."""

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np

# Chcemy zapisać dwa wykresy ułożone w jednym wierszu i dwóch kolumnach
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

first_ax: Axes = ax[0]
second_ax: Axes = ax[1]

# Wykres pierwszy
# x to dziedzina: 50 próbek z zakresu [-3, 3] wygenerowanych liniowo
# y to exp(-x^2)
# y_err to szum pochodzący z rozkładu normalnego o zadanych parametrach
x = np.linspace(start=-3, stop=3, num=50)
y = np.exp(-(x**2))
y_err = np.random.normal(loc=np.mean(y), scale=0.1, size=len(y))

# Zaznaczamy x, y oraz obszar szumu wokół funkcji
# wykreślenie y
first_ax.plot(x, y, label="exp(-x^2)")
first_ax.fill_between(x, y - y_err, y + y_err, alpha=0.2, label="+/- szum")

# Dodajemy oznaczenia osi i legendę na górze po lewej stronie
first_ax.set_xlabel("x")
first_ax.set_ylabel("y")
first_ax.legend(loc="upper left")

# Wykres drugi
# Definiujemy dziedzinę (x) oraz funkcje do wykreślenia (y_1, y_2)
x = np.arange(start=-50.0, stop=50.0, step=0.1)
y_1 = np.cos(x / 3.0)
y_2 = np.sin(x)

# Kreślimy obie funkcje
second_ax.plot(x, y_1, label="cos(x/3)")
second_ax.plot(x, y_2, label="sin(x)")

# Ustawiamy skalę osi x na symetryczną-logarytmiczną oraz dodajemy siatkę w
# tle kreślonych krzywych
second_ax.set_xscale("symlog")
second_ax.grid(True)

# Dodajemy oznaczenia osi i legendę na dole po prawej stronie
second_ax.set_xlabel("x")
second_ax.set_ylabel("y")
second_ax.legend(loc="lower right")

# Dodajemy tytuł
plt.suptitle("Funkcje wygenerowane w 'numpy' i wykreślone w 'matplotlib'")
plt.savefig("wykres.png")
