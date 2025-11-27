import re
import numpy as np
import sympy as sp


class Monome:
    """Класс монома"""
    def __init__(self, s, unique_monomes,  max_series_degree=100):
        self.name = str(s)
        self.max_series_degree = max_series_degree
        self.degree = 0
        self.parents = None
        self.signature = []
        self.coeffs = np.zeros(self.max_series_degree)

        # Разбиваем выражение на множители, например: x1*x2**2 -> x1, x2**2
        parts = re.split(r'(?<!\*)\*(?!\*)', self.name)

        for part in parts:
            if '**' in part:
                name, deg_part = part.split('**')
                name = name.strip()
                deg = int(deg_part)
            else:
                name = part.strip()
                deg = 1
            self.degree += deg

            match = re.match(r'x_(\d+)', name)
            if match:
                idx = int(match.group(1))
            else:
                raise ValueError(f"Invalid variable name in monome: {name}")
            self.signature.extend([idx] * deg)
        if self.degree >1:
            self.parents = [unique_monomes[f'x_{idx}'] for idx in self.signature]
        else:
            self.parents = None

    def eval(self, x_val):
        """Вычисление монома"""
        result = 1.0
        for idx in self.signature: # Пока что и так нормально
            result *= x_val[idx]
        return result

class Equation:
    """Класс уравнения"""
    def __init__(self, equation, unique_monomes, max_series_degree=100):
        equation = str(equation)
        self.monomes = []
        parts = re.split(r' (\+|-) ', equation)

        elements = parts[::2]
        operators = ['+'] + parts[1::2]

        for sign, monome_name in zip(operators, elements):

            # Обработка "-" перед мономом
            coef = 1
            neg_flag = True if monome_name[0] == '-' else False
            if neg_flag:
                monome_name = monome_name[1:]
                coef = -1

            split_id = monome_name.find('*')
            if split_id != -1 and monome_name[split_id + 1] != '*': # Если это умножение двух переменных
                try:
                    coef *= float(monome_name[0:split_id])
                    monome_name = monome_name[split_id + 1:]
                except ValueError:
                    pass

            coef = -coef if sign == '-' else coef

            if monome_name not in unique_monomes.keys(): # Если моном ещё не определён
                monome = Monome(monome_name, unique_monomes, max_series_degree)
                self.monomes.append((coef, monome))
                unique_monomes[monome_name] = monome
            else:
                self.monomes.append((coef, unique_monomes[monome_name]))

    def sum_up(self, i):
        """Сумма мономов уравнения"""
        result = 0
        for coef, monome in self.monomes:
            result += coef * monome.coeffs[i]
        result /= (i + 1)
        return result

    def sum_up_absolute(self, x_val):
        """Сумма модулей мономов уравнения"""
        result = 0
        for coef, monome in self.monomes:
            result += abs(coef * monome.eval(x_val))
        return result


if __name__ == "__main__":
    pass
