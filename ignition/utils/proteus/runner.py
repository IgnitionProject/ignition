import sys

from proteus import Comm, Profiling, NumericalSolution, default_so, default_s

from .optparser import get_prog_opts
from .defaults import ProteusProblem, ProteusNumerics

def init_mpi_petsc(opts, log):
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

def proteus_runner(expr, problem_kws, numerics_kws, *args, **kws):
    opts, args = get_prog_opts(args, __doc__)
    log = kws.get('log', None)
    if log is None: log = Profiling.logEvent
    comm = init_mpi_petsc(opts, log)
    problem_list = [ProteusProblem(**problem_kws),]
    simulation_list = [default_s]
    numerics_list = [ProteusNumerics(**numerics_kws),]
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
