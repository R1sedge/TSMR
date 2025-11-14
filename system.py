import sympy as sp
from win32com.client import constants


class System:
    def __init__(self, system_path, constants_path, start_path):
        self.equations = {}
        self.variables = []
        self.constants = {}
        self.start_point = {}
        self.constants = {}

        self.read_constants(constants_path)
        self.read_system(system_path)
        self.read_start_point(start_path)
        self.replace_constants()

    def read_system(self, system_path):
        with open(system_path) as file:
            for line in file:
                left, right = line.split(' = ')

                var_name = left[0:-1]
                self.variables.append(var_name)

                self.equations[var_name] = sp.sympify(right)

    def read_constants(self, constants_path):
        with open(constants_path) as file:
            for line in file:
                var_name, val = line.split(' = ')
                self.constants[sp.symbols(var_name)] = sp.sympify(val).evalf()

    def replace_constants(self):
        for variable in self.variables:
            self.equations[variable] = self.equations[variable].xreplace(self.constants)
            if sp.symbols('pi') in self.constants:
                self.equations[variable] = self.equations[variable].subs(sp.pi, self.constants[sp.symbols('pi')])

        for start in self.start_point:
            self.start_point[start] =  self.start_point[start].xreplace(self.constants)
            if sp.symbols('pi') in self.constants:
                self.start_point[start] = self.start_point[start].subs(sp.pi, self.constants[sp.symbols('pi')])
    def read_start_point(self, start_path):
        with open(start_path) as file:
            for line in file:
                var_name, val = line.split(' = ')
                self.start_point[var_name] = sp.sympify(val).evalf()

    def display_system(self):
        print('System')
        for var in self.variables:
            print(f'{var} = {self.equations[var]}')

        print('\nVariables:')
        print(self.variables)

        print('\nConstants:')
        for var in self.constants:
            print(f'{var} = {self.constants[var]}')

        print('\nStart point')
        for var in self.variables:
            print(f'{var} = {self.start_point[var]}')


if __name__ == '__main__':
    system = System('data/system.txt', 'data/constants.txt', 'data/start_point.txt')
    system.display_system()




