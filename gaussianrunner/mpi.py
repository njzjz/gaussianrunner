import logging

from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor

from . import GaussianRunner


class GaussianRunner_MPI(GaussianRunner):
    @classmethod
    def chunks(cls, arr, m):
        shared = [[] for i in range(m)]
        for index, job in enumerate(arr):
            shared[index % m].append(job)
        return shared

    def run_MPI(self, fileformat, jobs):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        name = MPI.Get_processor_name()
        size = comm.Get_size()
        if rank == 0:
            jobs_to_share = self.chunks(jobs, size)
        else:
            jobs_to_share = None
        recvjobs = comm.scatter(jobs_to_share, root=0)

        self.runGaussianInParallel(fileformat, recvjobs)
        logging.info(f"{name} ({rank+1}/{size}) finishes {len(recvjobs)} jobs.")

    def run_MPIPool(self, fileformat, jobs):
        def runGaussian(job):
            return self.runGaussianInParallel(fileformat, job)

        with MPIPoolExecutor() as executor:
            results = executor.map(runGaussian, jobs)
            for _ in results:
                pass
        logging.info(f"finish {len(jobs)} jobs.")
