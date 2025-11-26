from TSMR_solver import Solver
from system import System

system = System('data2')
solver = Solver(t0=0, t1=1, atol=1e-6, rtol=1e-6, max_degree=100, system=system)
solver.find_coeffs()
#solver.display()
x_last = solver.integrate()
print(x_last)
solver.plot([0, 1])