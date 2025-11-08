from latex_parser import read_system, read_constants
import re
import sympy as sp
from utils import Monome, Equation


class ODESystem:

    def __init__(self):
        self.equations = []
        self.variables = []
        self.constants = {}
        self.start_point = []

    def load_task(self, system_path, constants_path, start_point_path):
        # Константы
        self.constants = read_constants(constants_path)

        # Уравнения
        variables, equations = read_system(system_path)
        self.variables = variables
        equations = [equation.xreplace(self.constants) for equation in equations]
        equations = [Equation(equation) for equation in equations]
        self.equations = equations

        # Начальные данные




    def display(self):
        print('Equations:')
        for equation in self.equations:
            print(equation)

        print('\nVariables:')
        print(*self.variables)

        print('\nConstants:')
        for constant in self.constants:
            print(constant, '=' ,self.constants[constant])


    def preprocess1(self):
        pass




# Пример использования
if __name__ == "__main__":
    system = ODESystem()
    system.load_task('test.txt', 'test_constants.txt')
    system.display()

