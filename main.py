import sympy as sp
import re


class ODESystem:
    def __init__(self):
        self.equations = {}
        self.variables = []
        self.parameters = {}

    def read_system(self, filename):
        """Считывает систему ОДУ из файла в LaTeX формате"""
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('%'):
                continue

            # Парсим уравнение вида \frac{dx}{dt} = выражение
            match = re.match(r'\\frac\{d(\w+)\}\{dt\}\s*=\s*(.+)', line)
            if match:
                var_name, rhs_latex = match.groups()
                self.variables.append(var_name)

                # Преобразуем LaTeX в Python выражение
                python_expr = self._latex_to_python(rhs_latex)
                self.equations[var_name] = sp.sympify(python_expr)

        self.variables.sort()
        print(f"Загружено {len(self.equations)} уравнений")

    def _latex_to_python(self, latex_str):
        """Преобразует LaTeX в Python/sympy выражение"""
        expr = latex_str.replace(' ', '')

        # Греческие буквы
        greek_map = {
            '\\alpha': 'alpha', '\\beta': 'beta', '\\gamma': 'gamma', '\\delta': 'delta',
            '\\epsilon': 'epsilon', '\\zeta': 'zeta', '\\eta': 'eta', '\\theta': 'theta',
            '\\iota': 'iota', '\\kappa': 'kappa', '\\lambda': 'lambda', '\\mu': 'mu',
            '\\nu': 'nu', '\\xi': 'xi', '\\pi': 'pi', '\\rho': 'rho', '\\sigma': 'sigma',
            '\\tau': 'tau', '\\phi': 'phi', '\\chi': 'chi', '\\psi': 'psi', '\\omega': 'omega'
        }

        for latex_greek, english_name in greek_map.items():
            expr = expr.replace(latex_greek, english_name)

        # Степени: x^2 -> x**2
        expr = re.sub(r'(\w+)\^(\d+)', r'\1**\2', expr)
        expr = re.sub(r'\)\^(\d+)', r')**\1', expr)

        # Дроби: \frac{a}{b} -> (a)/(b)
        expr = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)', expr)

        return expr

    def read_parameters(self, filename):
        """Считывает параметры из файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('%'):
                continue

            # Формат: имя = значение
            if '=' in line:
                name, value = line.split('=', 1)
                name = name.strip()
                value = float(value.strip())
                self.parameters[name] = value

        print(f"Загружено {len(self.parameters)} параметров")

    def display(self, substitute_params=False):
        """Отображает систему уравнений"""
        print("\n" + "=" * 50)
        print("СИСТЕМА ДИФФЕРЕНЦИАЛЬНЫХ УРАВНЕНИЙ")
        print("=" * 50)

        for var in self.variables:
            expr = self.equations[var]

            if substitute_params:
                # Подставляем численные значения параметров
                for param, value in self.parameters.items():
                    expr = expr.subs(sp.Symbol(param), value)

            print(f"d{var}/dt = {expr}")

        if self.parameters and not substitute_params:
            print(f"\nПараметры: {list(self.parameters.keys())}")

        print("=" * 50)


# Пример использования
if __name__ == "__main__":
    # Использование
    system = ODESystem()
    system.read_system('system.txt')
    system.read_parameters('parameters.txt')

    # Отображаем систему с параметрами
    system.display(substitute_params=False)

    # Отображаем систему с подставленными значениями
    system.display(substitute_params=True)