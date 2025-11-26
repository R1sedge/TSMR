import logging
from utils import Equation, Monome
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import os

# Путь к файлу лога
LOG_FILE = "solver.log"

# Удаляем старый лог-файл, если он существует
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("solver.log"),  # Логи в файл
        logging.StreamHandler()              # Логи в консоль
    ]
)

class Solver:
    def __init__(self, t0, t1, system, atol, rtol, max_degree):
        self.atol = atol
        self.rtol = rtol
        self.max_degree = max_degree
        self.min_degree = 5
        if self.max_degree < self.min_degree:
            raise Exception('Максимальная степень меньше минимальной')
        self.current_degree = max_degree

        self.variables = system.variables
        self.var_num = system.var_num
        self.start_point = system.start_point

        self.var_monomes = [None] * self.var_num
        self.unique_monomes = {}

        self.max_step = 0.5
        self.current_step = 0.5

        self.t0 = t0
        self.t1 = t1
        self.current_t = t0

        self.x_history = []
        self.t_history = []

        # Создаём мономы переменных
        for variable in system.variables:
            self.unique_monomes[str(variable)] = Monome(variable, self.unique_monomes, max_degree)

        # Записываем уравнения через мономы и создаём их
        self.equations = []
        for i in range(system.var_num):
            self.equations.append(Equation(system.equations[i], self.unique_monomes, max_degree))

        # Разделяем мономы переменных и остальные
        for i in range(self.var_num):
            self.var_monomes[i] = self.unique_monomes[self.variables[i]]
            self.unique_monomes.pop(self.variables[i])

        # Вносим начальные данные
        self.use_start_point()

        # Предварительные вычисления
        self.find_step()
        self.find_degree()

    def use_start_point(self):
        for i in range(self.var_num):
            self.var_monomes[i].coeffs[0] = self.start_point[i]

    def find_coeffs(self):
        def compute_monomes(i):
            for monome in self.unique_monomes.values():
                monome.coeffs[i] = sum([monome.parents[0].coeffs[l] * monome.parents[1].coeffs[i - l] for l in range(i + 1)])

        def compute_variables(i):
            for k in range(self.var_num):
                self.var_monomes[k].coeffs[i] = self.equations[k].sum_up(i - 1)

        for j in range(self.max_degree - 1):
            compute_monomes(j)
            compute_variables(j + 1)

    def find_degree(self):
        pass

    def find_step(self):
        max_value = max([equation.sum_absolute(self.start_point) for equation in self.equations])
        if max_value != 0:
            max_step = min(1 / max_value, self.max_step)
        else:
            max_step = self.max_step
        self.current_step = max_step

    def correct_step(self):
        step = self.current_step
        new_step = (step * (sqrt((1 / self.var_num) *
                    sum([(self.delta_T(self.current_step, i) ** 2) * (self.atol + self.rtol * max(abs(self.start_point)[i], abs()))
                    for i in range(self.var_num)])))
                    ** (1 / (self.max_degree + 1)))

    def delta_T(self, step, i):
        pass

    def sum_up_series(self):
        for i in range(self.var_num):
            self.start_point[i] = self.sum_one_series(i, self.current_degree)

    def sum_one_series(self, i, degree):
        return sum(self.var_monomes[i].coeffs[m] * self.current_step ** m for m in range(degree))

    def integrate(self):
        max_steps = 1000
        steps = 0
        logging.info("Starting integration process")
        while self.current_t < self.t1 and steps < max_steps:
            self.x_history.append(self.start_point.copy())
            self.t_history.append(self.current_t)

            logging.info(f"Iteration {steps}: t = {float(self.current_t):.6f}, "
                         f"step = {float(self.current_step):.6f}, "
                         f"variables = {[round(float(val), 6) for val in self.start_point]}]")

            self.find_coeffs()
            self.find_step()

            #self.current_step = 0.05   # Для отладки

            if self.current_t + self.current_step > self.t1:
                self.current_step = self.t1 - self.current_t

            self.sum_up_series()
            self.use_start_point()

            self.current_t += self.current_step
            steps += 1

        logging.info(f"Integration finished at t = {float(self.current_t):.6f} after {steps} steps")
        logging.info(f"Final variables: {[float(val) for val in self.start_point]}")
        self.x_history.append(self.start_point.copy())
        self.t_history.append(self.current_t)
        return self.start_point.copy()

    def display(self):
        print('Variable Monomes:')
        print(self.var_monomes)
        print('Other Mononomes:')
        print(self.unique_monomes)
        print()
        for eq in self.equations:
            for coef, m in eq.monomes:
                print(str(coef), m.name, end=' ')
            print()

    def plot(self, indices):
        for i in indices:
            var_history = [val[i] for val in self.x_history]

            plt.plot(self.t_history, var_history)

            plt.xlabel('Time')
            plt.ylabel(self.variables[i])
            plt.show()