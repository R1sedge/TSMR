from scipy.integrate import solve_ivp

from system import System
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

def diff_eq(t, y):
    x0, x1, x2, x3 = y
    dx0dt = x1
    dx1dt = -k ** 2 * x2
    dx2dt = x1 * x3
    dx3dt = -x1 * x2
    return [dx0dt, dx1dt, dx2dt, dx3dt]

if __name__ == '__main__':
    system = System('data2')
    k = sqrt(9.8)
    y0 = [system.start_point[i] for i in range(system.var_num)]
    t_span =(0, 1)
    t_eval = np.linspace(0, 1, 100)

    solution = solve_ivp(diff_eq, t_span, y0, t_eval=t_eval, method='RK45')
    print(f'x0 = {solution.y[0][-1]}')
    print(f'x1 = {solution.y[1][-1]}')

    # Визуализация

    plt.plot(solution.t, solution.y[0])
    plt.title('x0(t)')
    plt.xlabel('Время')
    plt.ylabel('x0')
    plt.show()

    plt.plot(solution.t, solution.y[1])
    plt.title('x1(t)')
    plt.xlabel('Время')
    plt.ylabel('x1')
    plt.show()

    #x0 = -0.3330123179414051 RK
    #x_0': -0.339733698808828 25
    #'x_0': -0.339860361474420 100

    #x1 = -1.5956315338769045 RK
    #x_1': -1.58277956171820 25
    # 'x_1': -1.58265791499167 100


