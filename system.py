import sympy as sp

class System:
    """
    Класс для считывания и хранения системы дифференциальных уравнений.
    Данные считываются из дирректории data_path следующей структуры:

    data_path:\n
    - system.txt - файл с уравнениями \n
    - constants.txt - файл с константами \n
    - start_point.txt - файл с начальной точкой

    """
    def __init__(self, data_path):

        system_path = data_path + '/system.txt'
        constants_path = data_path + '/constants.txt'
        start_path = data_path + '/start_point.txt'

        self.equations = []
        self.variables = []
        self.constants = {}
        self.start_point = []
        self.var_num = 0

        self.read_constants(constants_path)
        self.read_system(system_path)
        self.read_start_point(start_path)
        self.replace_constants()

    def read_system(self, system_path):
        """Читаем систему уравнений из файла data/system.txt"""
        with open(system_path) as file:
            for line in file:
                left, right = line.split(' = ')

                var_name = left[0:-1]
                self.variables.append(var_name)

                self.equations.append(sp.sympify(right))
        self.var_num = len(self.variables)

    def read_constants(self, constants_path):
        """Читаем константы из файла data/constants.txt"""
        with open(constants_path) as file:
            for line in file:
                var_name, val = line.split(' = ')
                self.constants[sp.symbols(var_name)] = sp.sympify(val).evalf()

    def replace_constants(self):
        """Заменяем константы в уравнениях"""

        for i in range(self.var_num):
            self.equations[i] = self.equations[i].xreplace(self.constants)
            if sp.symbols('pi') in self.constants:
                self.equations[i] = self.equations[i].subs(sp.pi, self.constants[sp.symbols('pi')])

            self.start_point[i] =  self.start_point[i].xreplace(self.constants)
            if sp.symbols('pi') in self.constants:
                self.start_point[i] = self.start_point[i].subs(sp.pi, self.constants[sp.symbols('pi')])

    def read_start_point(self, start_path):
        """Читаем начальную точку из файла data/start_point.txt"""
        self.start_point = [0] * self.var_num
        with open(start_path) as file:
            for line in file:
                var_name, val = line.split(' = ')
                self.start_point[self.variables.index(var_name)] = sp.sympify(val).evalf()

    def display_system(self):
        print('System')
        for i in range(self.var_num):
            print(f'{self.variables[i]} = {self.equations[i]}')

        print('\nVariables:')
        print(self.variables)

        print('\nConstants:')
        for var in self.constants:
            print(f'{var} = {self.constants[var]}')

        print('\nStart point')
        for i in range(self.var_num):
            print(f'{self.variables[i]} = {self.start_point[i]}')


if __name__ == '__main__':
    system = System('data2')
    system.display_system()




