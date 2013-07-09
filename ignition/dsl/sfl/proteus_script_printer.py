"""Script printer for Proteus"""

from ...utils import indent_code
from .sfl_printer import SFLPrinter


script_header =  """
\"\"\"test_poisson.py [options]

Solves the Heterogeneous Poisson equation on a unit cube. A full
script for testing generation and tools provided by proteus.
\"\"\"

import numpy as np
import sys

from proteus import Comm, Profiling, NumericalSolution, TransportCoefficients, default_so, default_s
from proteus.FemTools import C0_AffineLinearOnSimplexWithNodalBasis
from proteus.LinearSolvers import LU
from proteus.NonlinearSolvers import Newton
from proteus.NumericalFlux import Advection_DiagonalUpwind_Diffusion_IIPG_exterior
from proteus.Quadrature import SimplexGaussQuadrature
from proteus.superluWrappers import SparseMatrix
from proteus.TimeIntegration import NoIntegration

from ignition.utils.proteus.defaults import ProteusProblem, ProteusNumerics
from ignition.utils.proteus.optparser import get_prog_opts


log = Profiling.logEvent
nd = 3
"""

problem_template = """
class Poisson(ProteusProblem):
    \"\"\"
    Heterogeneous Poisson's equation, -div(a(x)u) = f(x), on unit domain [0,1]x[0,1]x[0,1]
    \"\"\"

    ##\page Tests Test Problems
    # \ref poisson_3d_p.py "Heterogeneous Poisson's equation, -div(a(x)u) = f(x), on unit domain [0,1]x[0,1]x[0,1]"
    #

    ##\ingroup test
    #\file poisson_3d_p.py
    #
    #\brief Heterogenous Poisson's equations in 3D unit domain [0,1]x[0,1]x[0,1]

    def __init__(self):
        self.name = "Poisson"

        #space dimension
        self.nd = 3
        #if unstructured would need variable polyfile or meshfile set

        #steady-state so no initial conditions
        self.initialConditions = None
        #use sparse diffusion representation
        self.sd=True
        #identity tensor for defining analytical heterogeneity functions
        self.Ident = np.zeros((nd,nd),'d')
        self.Ident[0,0]=1.0; self.Ident[1,1] = 1.0; self.Ident[2,2]=1.0

        #store a,f in dictionaries since coefficients class allows for one entry per component
        self.aOfX = {0:self.a5}; self.fOfX = {0:self.f5}

        #one component
        self.nc = 1
        #load analytical solution, dirichlet conditions, flux boundary conditions into the expected variables
        self.analyticalSolution = {0:self.u5Ex()}
        self.analyticalSolutionVelocity = {0:self.velEx(self.analyticalSolution[0],self.aOfX[0])}
        #
        self.dirichletConditions = {0:self.getDBC5}
        self.advectiveFluxBoundaryConditions =  {0:self.getAdvFluxBC5}
        self.diffusiveFluxBoundaryConditions = {0:{0:self.getDiffFluxBC5}}
        self.fluxBoundaryConditions = {0:'setFlow'} #options are 'setFlow','noFlow','mixedFlow'


        #equation coefficient names
        self.coefficients = TransportCoefficients.PoissonEquationCoefficients(self.aOfX, 
                                                                         self.fOfX, self.nc, self.nd)
        #
        self.coefficients.variableNames=['u0']



    #for computing exact 'Darcy' velocity
    class velEx:
        def __init__(self,duex,aex):
            self.duex = duex
            self.aex = aex
        def uOfX(self,X):
            du = self.duex.duOfX(X)
            A  = np.reshape(self.aex(X),(3,3))
            return -np.dot(A,du)
        def uOfXT(self,X,T):
            return self.uOfX(X)


    ##################################################
    #define coefficients a(x)=[a_{ij}] i,j=0,2, right hand side f(x)  and analytical solution u(x)
    #u = x*x + y*y + z*z, a_00 = x + 5, a_11 = y + 5.0 + a_22 = z + 10.0
    #f = -2*x -2*(5+x) -2*y-2*(5+y) -2*z-2*(10+z)
    #
    def a5(self, x):
        return np.array([[x[0] + 5.0,0.0,0.0],[0.0,x[1] + 5.0,0.0],[0.0,0.0,x[2]+10.0]],'d')
    def f5(self, x):
        return -2.0*x[0] -2*(5.+x[0]) -2.*x[1]-2.*(5.+x[1]) -2.*x[2]-2.*(10+x[2])

    #'manufactured' analytical solution
    class u5Ex:
        def __init__(self):
            pass
        def uOfX(self,x):
            return x[0]**2+x[1]**2+x[2]**2
        def uOfXT(self,X,T):
            return self.uOfX(X)
        def duOfX(self,X):
            du = 2.0*np.reshape(X[0:3],(3,))
            return du
        def duOfXT(self,X,T):
            return self.duOfX(X)

    #dirichlet boundary condition functions on (x=0,y,z), (x,y=0,z), (x,y=1,z), (x,y,z=0), (x,y,z=1)
    def getDBC5(self, x,flag):
        if x[0] in [0.0] or x[1] in [0.0,1.0] or x[2] in [0.0,1.0]:
            return lambda x,t: self.u5Ex().uOfXT(x,t)

    def getAdvFluxBC5(self, x,flag):
        pass
    #specify flux on (x=1,y,z)
    def getDiffFluxBC5(self, x,flag):
        if x[0] == 1.0:
            n = np.zeros((nd,),'d'); n[0]=1.0
            return lambda x,t: np.dot(self.velEx(self.u5Ex(),self.a5).uOfXT(x,t),n)
        if not (x[0] in [0.0] or x[1] in [0.0,1.0] or x[2] in [0.0,1.0]):
            return lambda x,t: 0.0

"""

numeric_template = """
class C0P1_Poisson_Numerics(ProteusNumerics):
    #steady-state so no time integration
    timeIntegration = NoIntegration
    #number of output timesteps
    nDTout = 1

    #finite element spaces
    femSpaces = {0:C0_AffineLinearOnSimplexWithNodalBasis}
    #numerical quadrature choices
    elementQuadrature = SimplexGaussQuadrature(nd,4)
    elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,4)

    #number of nodes in x,y,z
    nnx = 7
    nny = 7
    nnz = 7
    #if unstructured would need triangleOptions flag to be set


    #number of levels in mesh
    nLevels = 1

    #no stabilization or shock capturing
    subgridError = None

    shockCapturing = None

    #nonlinear solver choices
    multilevelNonlinearSolver  = Newton
    levelNonlinearSolver = Newton
    #linear problem so force 1 iteration allowed
    maxNonlinearIts = 2
    maxLineSearches = 1
    fullNewtonFlag = True
    #absolute nonlinear solver residual tolerance
    nl_atol_res = 1.0e-8
    #relative nonlinear solver convergence tolerance as a function of h
    #(i.e., tighten relative convergence test as we refine)
    tolFac = 0.0

    #matrix type
    matrix = SparseMatrix

    #convenience flag
    parallel = False

    if parallel:
        multilevelLinearSolver = KSP_petsc4py
        #for petsc do things lie
        #"-ksp_type cg -pc_type asm -pc_asm_type basic -ksp_atol  1.0e-10 -ksp_rtol 1.0e-10 -ksp_monitor_draw" or
        #-pc_type lu -pc_factor_mat_solver_package
        #can also set -pc_asm_overlap 2 with default asm type (restrict)
        levelLinearSolver = KSP_petsc4py#
        #for petsc do things like
        #"-ksp_type cg -pc_type asm -pc_asm_type basic -ksp_atol  1.0e-10 -ksp_rtol 1.0e-10 -ksp_monitor_draw" or
        #-pc_type lu -pc_factor_mat_solver_package
        #can also set -pc_asm_overlap 2 with default asm type (restrict)
        #levelLinearSolver = PETSc#
        #pick number of layers to use in overlap
        nLayersOfOverlapForParallel = 0
        #type of partition
        parallelPartitioningType = MeshParallelPartitioningTypes.node
        #parallelPartitioningType = MeshParallelPartitioningTypes.element
        #have to have a numerical flux in parallel
        numericalFluxType = Advection_DiagonalUpwind_Diffusion_IIPG_exterior
        #for true residual test
        linearSolverConvergenceTest = 'r-true'
        #to allow multiple models to set different ksp options
        #linear_solver_options_prefix = 'poisson_'
        linearSmoother = None
    else:
        multilevelLinearSolver = LU
        levelLinearSolver = LU
        numericalFluxType = Advection_DiagonalUpwind_Diffusion_IIPG_exterior

    #linear solver relative convergence test
    linTolFac = 0.0
    #linear solver absolute convergence test
    l_atol_res = 1.0e-10

    #conservativeFlux =  {0:'pwl'}

"""

script_foot_template = """
def init_mpi_petsc(opts):
    log("Initializing MPI")
    if opts.petscOptions != None:
        petsc_argv = sys.argv[:1]+opts.petscOptions.split()
        log("PETSc options from commandline")
        log(str(petsc_argv))
    else:
        petsc_argv=sys.argv[:1]
    if opts.petscOptionsFile != None:
        petsc_argv=[sys.argv[0]]
        petsc_argv += open(opts.petscOptionsFile).read().split()
        log("PETSc options from commandline")
        log(str(petsc_argv))
    return Comm.init(argv=petsc_argv)

def main(*args):
    opts, args = get_prog_opts(args, __doc__)
    comm = init_mpi_petsc(opts)
    problem_list = [Poisson(),]
    simulation_list = [default_s]
    numerics_list = [C0P1_Poisson_Numerics(),]
    numerics_list[0].periodicDirichletConditions = problem_list[0].periodicDirichletConditions
    numerics_list[0].T = problem_list[0].T
    simulation_name = problem_list[0].name + "_" + numerics_list[0].__class__.__name__
    simulation_name_proc = simulation_name + "_" + repr(comm.rank())
    simFlagsList = [{ 'simulationName': simulation_name,
                      'simulationNameProc': simulation_name_proc,
                      'dataFile': simulation_name_proc + '.dat',
                      'components' : [ci for ci in range(problem_list[0].coefficients.nc)],
                      }]

    so = default_so
    so.name = problem_list[0].name
    so.pnList = problem_list
    so.sList = [default_s]
    try:
        so.systemStepControllerType = numerics_list[0].systemStepControllerType
    except AttributeError:
        pass
    try:
        so.tnList = numerics_list[0].tnList
        so.archiveFlag = numerics_list[0].archiveFlag
    except AttributeError:
        pass

    runNumber = 0
    runName = so.name + repr(runNumber)
    Profiling.procID=comm.rank()
    if simulation_list[0].logAllProcesses or opts.logAllProcesses:
        Profiling.logAllProcesses = True
    Profiling.flushBuffer=simulation_list[0].flushBuffer

    if opts.logLevel > 0:
        Profiling.openLog(runName+".log",opts.logLevel)


    ns = NumericalSolution.NS_base(default_so, problem_list, numerics_list, simulation_list,
                                   opts, simFlagsList)

    ns.calculateSolution(runName)

if __name__ == "__main__":
    main(sys.argv[1:])

"""


class ProteusScriptPrinter(SFLPrinter):
    comment_str = "#"

    def __init__(self, generator):
        self._generator = generator

    def _print_header(self, indent):
        return script_header

    def _print_problem_class(self, indent):
        ret_code = problem_template
        return ret_code

    def _print_numeric_class(self, indent):
        ret_code = numeric_template
        return ret_code

    def _print_script_footer(self, indent):
        ret_code = script_foot_template
        return ret_code

    def print_file(self, indent=0):
        ret_code = ""
        ret_code += self._print_header(indent)
        ret_code += self._print_problem_class(indent)
        ret_code += self._print_numeric_class(indent)
        ret_code += self._print_script_footer(indent)
        return ret_code

    
