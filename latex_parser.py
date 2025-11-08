import re
import sympy as sp


def convert_expression(expr):
    # Удаляем все пробелы из выражения
    expr = expr.replace(" ", "")

    # Обрабатываем дроби: заменяем \frac{num}{den} на (num)/(den)
    pattern_frac = r'\\frac\{([^}]+)\}\{([^}]+)\}'
    expr = re.sub(pattern_frac, r'(\1)/(\2)', expr)

    # Расставляем операторы умножения где необходимо
    patterns = [
        (r'(\d+(?:\.\d*)?)([a-zA-Z])', r'\1*\2'),  # Число и буква
        (r'([a-zA-Z])([a-zA-Z])', r'\1*\2'),  # Буква и буква
        (r'(x_\w+)([a-zA-Z])', r'\1*\2'),  # Переменная и буква
        (r'\)([a-zA-Z])', r')*\1')  # Закрывающая скобка и буква
    ]

    for pattern, replacement in patterns:
        expr = re.sub(pattern, replacement, expr)

    return expr

def read_system(path):

    variables = []
    equations = []

    with open(path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        left, right = line.split('=')

        # Достаём имена переменных
        temp = re.match(r'\\dv\{([^}]+)\}\{([^}]+)\}', left)
        variables.append(temp.group(1))

        expr = convert_expression(right)
        expr = sp.sympify(expr)

        equations.append(expr)

    return variables, equations

def read_constants(path):
    with open(path, 'r') as f:
        lines = f.readlines()

        constants = {}

        for line in lines:
            l, r = line.split('=')
            const_name = l.strip()
            const_val = r.strip()
            constants[sp.symbols(const_name)] = sp.sympify(const_val)
    return constants

def read_starting_point(path):
    with open(path, 'r') as f:
        lines = f.readlines()

        starting_points = []
        for line in lines:
            pass



if __name__ == '__main__':
    print(read_system('data/system.txt'))
    print(read_constants('data/constants.txt'))
    print(read_starting_point('data/starting_point.txt'))