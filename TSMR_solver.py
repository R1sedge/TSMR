import numpy as np
from utils import Equation, Monome


class Solver:
    def __init__(self, atol, max_degree, system):
        self.atol = atol
        self.max_degree = max_degree

        self.variables = system.variables
        self.var_num = len(self.variables)
        self.var_monomes = {}
        self.unique_monomes = {}

        # Создаём мономы переменных
        for variable in system.variables:
            self.unique_monomes[str(variable)] = Monome(variable, self.unique_monomes)

        # Записываем уравнения через мономы и создаём их
        self.equations = []
        for variable in system.variables:
            self.equations.append(Equation(system.equations[variable], self.unique_monomes))

        # Вносим начальные данные
        for variable in self.variables:
            self.unique_monomes[variable].coeffs[0] = system.start_point[variable]

        # Разделяем мономы переменных и остальные
        for variable in self.variables:
            self.var_monomes[variable] = self.unique_monomes[variable]
            self.unique_monomes.pop(variable)



    def find_coefs(self):

        def compute_monomes(i):
            for monome in self.unique_monomes.values():
                monome.coeffs[i] = sum([monome.parents[0].coeffs[l] * monome.parents[1].coeffs[i - l] for l in range(i + 1)])

        def compute_variables(i):
            for k in range(self.var_num):
                self.var_monomes[self.variables[k]].coeffs[i] = self.equations[k].sum_up(i - 1)


        for j in range(self.max_degree - 1):
            compute_monomes(j)
            compute_variables(j + 1)



    def find_step(self):
        pass

    def integrate(self):
        pass

    def make_step(self):
        pass

    def display(self):
        print('Variable Monomes:')
        print(self.var_monomes)
        print('Other Monomes:')
        print(self.unique_monomes)
        print()
        for eq in self.equations:
            for coef, m in eq.monomes:
                print(str(coef), m.name, end=' ')
            print()

if __name__ == '__main__':
    pass