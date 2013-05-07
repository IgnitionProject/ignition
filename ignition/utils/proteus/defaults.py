import proteus
import proteus.StepControl
import proteus.TimeIntegration
import proteus.Transport


class ProteusProblem(object):
    """A default Problem for Proteus """

    name = None # Name of model, None or string
    nd = 1 # Number of spatial dimensions of the model domain
    domain = None # None or proteus.Domain.D_base
    movingDomain=False
    polyfile = None
    meshfile = None
    genMesh = True
    L=(1.0,1.0,1.0) # Tuple of dimensions for simple box shaped domain
    analyticalSolution = {} #Dictionary of analytical solutions for each component
    coefficients = None
    dirichletConditions = {}
    periodicDirichletConditions = None
    fluxBoundaryConditions = {} # Dictionary of flux boundary condition flags for each component 
                                # ('outflow','noflow','setflow','mixedflow')
    advectiveFluxBoundaryConditions =  {} # Dictionary of advective flux boundary conditions setter functions
    diffusiveFluxBoundaryConditions = {} # Dictionary of diffusive flux boundary conditions setter functions
    stressFluxBoundaryConditions = {} # Dictionary of stress tensor flux boundary conditions setter functions
    initialConditions = None #Dictionary of initial condition function objects
    weakDirichletConditions = None # Dictionary of weak Dirichlet constraint setters
    bcsTimeDependent = True # Allow optimizations if boundary conditions are not time dependent
    dummyInitialConditions = False #mwf temporary hack for RD level sets
    finalizeStep = lambda c: None
    T=1.0 # End of time interval
    sd = True # Use sparse representation of diffusion tensors
    LevelModelType = proteus.Transport.OneLevelTransport

class ProteusNumerics(object):
    """The default values for numerics modules
    """
    stepController = proteus.StepControl.FixedStep # The step controller class derived from :class:`proteus.StepControl.SC_base`
    timeIntegration = proteus.TimeIntegration.NoIntegration # The time integration class derived from :class:`proteus.TimeIntegraction.TI_base
    timeIntegrator  = proteus.TimeIntegration.ForwardIntegrator # Deprecated, the time integrator class
    runCFL = 0.9 # The maximum CFL for the time step
    nStagesTime = 1 # The number of stages for the time discretization
    timeOrder= 1 # The order of the time discretization
    DT = 1.0 # The time step
    nDTout = 1 # The number of output time steps
    rtol_u = {0:1.0e-4} # A dictionary of relative time integration tolerances for the components
    atol_u = {0:1.0e-4} # A dictionary of absolute time integration tolerances for the components
    nltol_u = 0.33 # The nonlinear tolerance factor for the component error
    ltol_u = 0.05 # The linear tolerance factor for the component error
    rtol_res = {0:1.0e-4} # A dictionary of relative tolerances for the weak residuals
    atol_res = {0:1.0e-4} # A dictionary of absolute tolerances for the weak residuals
    nl_atol_res = 1.0 # The nonlinear residual tolerance
    l_atol_res = 1.0 # The linear residual tolerance
    femSpaces = {} # A dictionary of the finite element classes for each component
                   # The classes should be of type :class:`proteus.FemTools.ParametricFiniteElementSpace` 
    elementQuadrature = None # A quadrature object for element integrals
    elementBoundaryQuadrature = None # A quadrature object for element boundary integrals
    nn = 3 # Number of nodes in each direction for regular grids
    nnx = None # Number of nodes in the x-direction for regular grids
    nny = None # Number of nodes in the y-direction for regular grids
    nnz = None # Number of nodes in the z-direction for regular grids
    triangleOptions="q30DenA" # Options string for triangle or tetGen
    nLevels = 1 # Number of levels for multilevel mesh
    subgridError = None # The subgrid error object of a type derived from :class:`proteus.SubgridError.SGE_base`
    massLumping = False # Boolean to lump mass matrix
    reactionLumping = False # Boolean to lump reaction term
    shockCapturing = None # The shock capturing diffusion object of a type derived from :class:`proteus.ShockCapturing.SC_base`
    numericalFluxType = None # A numerical flux class of type :class:`proteus.NumericalFlux.NF_base`
    multilevelNonlinearSolver  = proteus.NonlinearSolvers.NLNI # A multilevel nonlinear solver class of type :class:`proteus.NonlinearSolvers.MultilevelNonlinearSolver`
    levelNonlinearSolver = proteus.NonlinearSolvers.Newton # A nonlinear solver class of type :class:`proteus.NonlinearSolvers.NonlinearSolver`
    nonlinearSmoother = proteus.NonlinearSolvers.NLGaussSeidel # A nonlinear solver class of type :class:`proteus.NonlinearSolvers.NonlinearSolver`
    fullNewtonFlag = True # Boolean to do full Newton or modified Newton
    nonlinearSolverNorm = staticmethod(proteus.LinearAlgebraTools.l2Norm) # Norm to use for nonlinear algebraic residual
    tolFac = 0.01
    atol = 1.0e-8
    maxNonlinearIts =10
    maxLineSearches =10
    psitc = {'nStepsForce':3,'nStepsMax':100}
    matrix = proteus.superluWrappers.SparseMatrix
    multilevelLinearSolver = proteus.LinearSolvers.LU
    levelLinearSolver = proteus.LinearSolvers.LU
    computeEigenvalues = False
    computeEigenvectors = None #'left','right'
    linearSmoother = proteus.LinearSolvers.StarILU #GaussSeidel
    linTolFac = 0.001
    conservativeFlux = None
    checkMass = False
    multigridCycles = 2
    preSmooths = 2
    postSmooths = 2
    computeLinearSolverRates = False
    printLinearSolverInfo = False
    computeLevelLinearSolverRates = False
    printLevelLinearSolverInfo = False
    computeLinearSmootherRates = False
    printLinearSmootherInfo = False
    linearSolverMaxIts = 1000
    linearWCycles = 3
    linearPreSmooths = 3
    linearPostSmooths = 3
    computeNonlinearSolverRates=True
    printNonlinearSolverInfo=False
    computeNonlinearLevelSolverRates=False
    printNonlinearLevelSolverInfo=False
    computeNonlinearSmootherRates=False
    printNonlinearSmootherInfo=False
    nonlinearPreSmooths=3
    nonlinearPostSmooths=3
    nonlinearWCycles=3
    useEisenstatWalker=False
    maxErrorFailures=10
    maxSolverFailures=10
    needEBQ_GLOBAL = False
    needEBQ = False
    auxiliaryVariables=[]
    restrictFineSolutionToAllMeshes=False
    parallelPartitioningType = proteus.MeshTools.MeshParallelPartitioningTypes.element
    #default number of layers to use > 1 with element partition means
    #C0P1 methods don't need to do communication in global element assembly
    #nodal partitioning does not need communication for C0P1 (has overlap 1) regardless
    nLayersOfOverlapForParallel = 1
    parallelPeriodic=False#set this to true and use element,0 overlap to use periodic BC's in parallel
    nonlinearSolverConvergenceTest = 'r'
    levelNonlinearSolverConvergenceTest = 'r'
    linearSolverConvergenceTest = 'r' #r,its,r-true for true residual
    #we can add this if desired for setting solver specific options in petsc
    #linear_solver_options_prefix= None #
