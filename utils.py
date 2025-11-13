import re
import numpy as np
import sympy as sp

class Monome:
    def __init__(self, s, UnMs, max_series_degree=50):
        self.name = str(s)
        self.max_series_degree = max_series_degree
        self.degree = 0
        self.parents = None
        self.signature = {}
        self.coeffs = np.zeros(self.max_series_degree)

        s = str(s)
        parts = re.split(r'(?<!\*)\*(?!\*)', s)

        for part in parts:
            parts = part.split('**')
            if len(parts) == 2:
                name, deg = parts[0], int(parts[1])
            else:
                name, deg = parts[0], 1
            self.degree += deg
            self.signature[name] = deg

        if self.degree == 2: # Если не просто переменная
            self.parents = []
            for name in self.signature:
                self.parents.append(UnMs[name])


class Equation:
    def __init__(self, equation, UnMs):
        equation = str(equation)
        self.monomes = []
        parts = re.split(r' \+ | - ', equation) # TODO Нужно добавить учёт знака в коэффициенты
        parts = equation.split(' + ')
        for monome in parts:
            split_id = monome.find('*')
            if monome[split_id + 1] != '*' and split_id != -1:
                coef = float(monome[0:split_id])
                monome = monome[split_id + 1:]
            else:
                coef = 1
            if monome not in UnMs.keys(): # Если моном ещё не определён
                m = Monome(monome, UnMs)
                self.monomes.append((coef, m))
                UnMs[monome] = m
            else:
                self.monomes.append((coef, UnMs[monome]))




if __name__ == "__main__":
    pass
