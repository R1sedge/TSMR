from TSMR_solver import Solver
from system import System

system = System('data2')
solver = Solver(t0=-10, t1=10, atol=1e-10, rtol=1e-10, max_degree=50, system=system)
solver.find_coeffs()
solver.display()
x_last = solver.integrate()
print(x_last)
solver.plot([0, 1])