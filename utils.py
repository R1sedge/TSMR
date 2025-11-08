import re
import numpy as np

class Monome:
    def __init__(self, s, max_series_degree=50):
        self.max_series_degree = max_series_degree
        self.degree = 0
        self.signature = {}
        self.parents = []
        self.coeffs = np.zeros(self.max_series_degree)

        parts = re.split(r'(?<!\*)\*(?!\*)', s)

        for part in parts:
            parts = part.split('**')
            if len(parts) == 2:
                name, deg = parts[0], int(parts[1])
            else:
                name, deg = parts[0], 1
            self.signature[name] = deg
            self.degree += deg


class Equation:
    def __init__(self, equation):
        equation = str(equation)
        self.monomes = []
        temp = re.split(r' \+ | - ', equation)
        for monome in temp:
            self.monomes.append(Monome(monome))




if __name__ == "__main__":
    monome = Monome('x_0**2*x_1**2')
    print(monome.signature)
