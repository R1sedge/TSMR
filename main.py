from TSMR_solver import Solver
from system import System
from utils import *

system = System('data/system.txt', 'data/constants.txt', 'data/start_point.txt')
solver = Solver(atol=1e-6, max_degree=50, system=system)
solver.display()
