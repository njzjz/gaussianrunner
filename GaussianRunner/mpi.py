from mpi4py import MPI
import numpy
import math
import os
from GaussianRunner import GaussianRunner

class GaussianRunner_MPI(GaussianRunner):
    def chunks(self,arr, m):
        n = int(math.ceil(len(arr) / float(m)))
        return [arr[i:i + n] for i in range(0, len(arr), n)]

    def run_MPI(self,type,jobs):
        comm=MPI.COMM_WORLD
        rank=comm.Get_rank()
        name=MPI.Get_processor_name()
        size=comm.Get_size()
        if rank == 0:
            jobs_to_share = chunks(jobs,size)
        else:
            jobs_to_share = None
        recvjobs = comm.scatter(jobs_to_share, root=0)

        self.runGaussianInParallel(type,recvjobs)
        self.logging(name,"(",rank+1,"/",size,")","finish jobs:",*recvjobs)
