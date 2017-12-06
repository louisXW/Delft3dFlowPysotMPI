"""
.. module:: test_subprocess_mpi
  :synopsis: Test an external objective function
.. moduleauthor:: David Eriksson <dme65@cornell.edu>
"""
from pySOT import *
from pySOT import Sphere, SyncStrategyNoConstraints, \
    SymmetricLatinHypercube, CandidateDYCORS, \
    RBFInterpolant
from poap.mpiserve import MPIController, MPIProcessWorker
import numpy as np
import time
import sys
import os
import os.path
import logging
# from ObjectWAQmpi import *
from Objectlongnew import *
if sys.version_info < (3, 0):
    # Try to import from subprocess32
    try:
        from subprocess32 import Popen, PIPE
    except Exception as err:
        print("ERROR: You need the subprocess32 module for Python 2.7. \n"
              "Install using: pip install subprocess32")
        exit()
else:
    from subprocess import Popen, PIPE
# Try to import mpi4py
try:
    from mpi4py import MPI
except Exception as err:
    print("ERROR: You need mpi4py to use the POAP MPI controller")
    exit()


def array2str(x):
    return ",".join(np.char.mod('%f', x))


class CppSim(MPIProcessWorker):
    def eval(self, record_id, params, extra_args=None):
        try:
            fp = open("TEST_AGAIN.txt", "a")
            fp.write("this is try to launch process%s\n" % (rank))
            fp.write("this is try to launch process%s\n" % (str(record_id)))
            fp.write("this is try to launch process%s\n" % (str(params[0])))
            fp.write("this is try to launch process%s\n" % (array2str(params[0])))

            fp.write("this is try to launch process%s\n" % (str(params[1])))
            fp.write("this is try to launch process%s\n" % (str(params[2])))
            fp.write("this is try to launch process%s\n" % (type(params)))
            fp.close()
            # # self.process = Popen(['python', "object_func.py", array2str(params[0]), "%s" % rank], stdout=PIPE)
            # workingdir = "/home/users/nus/e0022672/delft3d/examples/" + str(params[1]) + "/"
            workingdir = "/home/users/nus/e0022672/delft3d/examples/"
            # os.chdir(workingdir)
            # os.system("./run_flow2d3d.sh")
            self.process = Popen(["python", workingdir + "run_simulation.py", array2str(params[0]), str(params[1]), str(params[2])], stdout=PIPE)
            out = self.process.communicate()[0]
            # val = 2
            self.finish_success(record_id, float(out))
        except ValueError:
            logging.info("WARNING: Incorrect output or crashed evaluation")
            self.finish_cancel(record_id)


def main_worker():
    logging.basicConfig(filename="./logfiles/test_subprocess_mpi.log",
                        level=logging.INFO)
    CppSim().run()


def main_master(nworkers):

    if not os.path.exists("./logfiles"):
        os.makedirs("logfiles")
    if os.path.exists("./logfiles/test_subprocess_mpi.log"):
        os.remove("./logfiles/test_subprocess_mpi.log")
    print "remove the log file"

    logging.basicConfig(filename="./logfiles/test_subprocess_mpi.log",
                        level=logging.INFO)

    print("\nTesting the POAP MPI controller with {0} workers".format(nworkers))
    print("Maximum number of evaluations: 200")
    print("Search strategy: Candidate DYCORS")
    print("Experimental design: Symmetric Latin Hypercube")
    print("Surrogate: Cubic RBF")

    maxeval = 40

    # data = ObjectWAQmpi(dim=2)
    data = delft3d(dim=9)
    print(data.info)

    # Create a strategy and a controller
    strategy = \
        SyncStrategyNoConstraints(
            worker_id=0, data=data,
            maxeval=maxeval, nsamples=nworkers,
            exp_design=SymmetricLatinHypercube(dim=data.dim, npts=5),
            sampling_method=CandidateDYCORS(data=data, numcand=100*data.dim),
            response_surface=RBFInterpolant(kernel = CubicKernel, tail = LinearTail, maxp = maxeval) )

    controller = MPIController(strategy)

    # Run the optimization strategy
    result = controller.run()
    print('Best value found: {0}'.format(result.value))
    print('Best solution found: {0}\n'.format(
        np.array_str(result.params[0], max_line_width=np.inf,
                     precision=5, suppress_small=True)))

if __name__ == '__main__':
    # Extract the rank
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocs = comm.Get_size()

    if rank == 0:
        print nprocs
        main_master(nprocs)
    else:
        print "this is salvei %s" %rank
        fp = open("TEST_AGAIN.txt", "a")
        fp.write("this is try to launch process%s\n" % (rank))
        fp.close()
        main_worker()
