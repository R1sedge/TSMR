from scipy.integrate import solve_ivp

from system import System
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt


def diff_eq2(t, y):
    x0, x1, x2, x3 = y
    dx0dt = x1
    dx1dt = -k ** 2 * x2
    dx2dt = x1 * x3
    dx3dt = -x1 * x2
    return [dx0dt, dx1dt, dx2dt, dx3dt]

def diff_eq3(t, y):
    x0, x1 = y
    dx0dt = x0 - x0*x1
    dx1dt = -x1 + x0*x1
    return [dx0dt, dx1dt]

if __name__ == '__main__':
    system = System('data2')
    k = sqrt(9.8)
    y0 = [system.start_point[i] for i in range(system.var_num)]
    t_span =(-10, 10)
    t_eval = np.linspace(-10, 10, 100)

    solution = solve_ivp(diff_eq2, t_span, y0, t_eval=t_eval, method='RK45', atol=1e-10, rtol=1e-10)
    print(f'x0 = {solution.y[0][-1]}')
    print(f'x1 = {solution.y[1][-1]}')

    # Визуализация

    plt.plot(solution.t, solution.y[0])
    plt.title('x0(t)' + f' = {solution.y[0][-1]}')
    plt.xlabel('Время')
    plt.ylabel('x0')
    plt.show()

    plt.plot(solution.t, solution.y[1])
    plt.title('x1(t)' + f' = {solution.y[1][-1]}')
    plt.xlabel('Время')
    plt.ylabel('x1')
    plt.show()

