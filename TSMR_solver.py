import numpy as np
from utils import Equation, Monome


class Solver:
    def __init__(self, atol, max_degree, system):
        self.atol = atol
        self.max_degree = max_degree

        self.variables = system.variables
        self.unique_monomes = {}

        # Создаём мономы переменных
        for variable in system.variables:
            self.unique_monomes[str(variable)] = Monome(variable, self.unique_monomes)

        # Записываем уравнения через мономы и создаём их
        self.equations = []
        for variable in system.variables:
            self.equations.append(Equation(system.equations[variable], self.unique_monomes))

    def find_coefs(self):
        pass

    def find_step(self):
        pass

    def integrate(self):
        pass

    def make_step(self):
        pass

    def display(self):
        print(self.unique_monomes)
        print()
        for eq in self.equations:
            for coef, m in eq.monomes:
                print(str(coef), m.name, end=' ')
            print()

if __name__ == '__main__':
    pass