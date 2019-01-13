from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor
import numpy
import math
import os
from GaussianRunner import GaussianRunner


class GaussianRunner_MPI(GaussianRunner):
    def chunks(self, arr, m):
        shared = [[] for i in range(m)]
        for index, job in enumerate(arr):
            shared[index % m].append(job)
        return shared

    def run_MPI(self, type, jobs):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        name = MPI.Get_processor_name()
        size = comm.Get_size()
        if rank == 0:
            jobs_to_share = self.chunks(jobs, size)
        else:
            jobs_to_share = None
        recvjobs = comm.scatter(jobs_to_share, root=0)

        self.runGaussianInParallel(type, recvjobs)
        self.logging(name, "(", rank+1, "/", size, ")",
                     "finish jobs:", *recvjobs)

    def run_MPIPool(self, type, jobs):
        def runGaussian(job):
            return self.runGaussianInParallel(type, job)

        with MPIPoolExecutor() as executor:
            results = executor.map(runGaussian, job)
            for _ in results:
                pass
        self.logging("finish jobs:", *jobs)
