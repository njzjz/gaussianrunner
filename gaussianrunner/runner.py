"""GaussianRunner."""


import logging
import os
import pickle
import subprocess as sp
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from .analyst import GaussianAnalyst


class GaussianRunner:
    def __init__(
            self, command="g16", cpu_num=None, nproc=4, keywords='',
            solution=False):
        self.command = command
        self.cpu_num = cpu_num if cpu_num else cpu_count()
        self.nproc = min(nproc, self.cpu_num)
        self.thread_num = self.cpu_num//self.nproc
        self.keywords = keywords
        self.solution = solution

    def runCommand(self, command, inputstr=None):
        try:
            output = sp.check_output(command.split(), input=(
                inputstr.encode() if inputstr else None)).decode('utf-8')
        except sp.CalledProcessError as e:
            output = e.output.decode('utf-8')
            logging.error(f"Run command {command} fail.")
        return output

    def runGaussianFunction(self, fileformat):
        if fileformat == 'input':
            function = self.runGaussianFromInput
        elif fileformat == 'gjf':
            function = self.runGaussianFromGJF
        elif fileformat == 'smiles':
            function = self.runGaussianFromSMILES
        else:
            def function(filename):
                return self.runGaussianFromType(filename, fileformat)
        return function

    @classmethod
    def generateLOGfilename(cls, inputformat, inputlist):
        if inputformat == 'input':
            outputlist = range(len(inputlist))
        elif inputformat == 'smiles':
            outputlist = [x.replace('/', '／') .replace('\\', '＼')
                          for x in inputlist]
        else:
            outputlist = [os.path.splitext(x)[0] for x in inputlist]
        outputlist = [f'{x}.log' for x in outputlist]
        return outputlist

    def runGaussianInParallel(self, inputtype, inputlist, outputlist=None, properties=None, savelog=True):
        inputtype = inputtype.lower()
        function = self.runGaussianFunction(inputtype)
        if outputlist is None:
            outputlist = self.generateLOGfilename(inputtype, inputlist)
        analyst = properties and GaussianAnalyst(properties=properties)
        with ThreadPool(self.thread_num) as pool:
            results = pool.imap(function, inputlist)
            for outputfile, result in zip(outputlist, results):
                if savelog:
                    with open(outputfile, 'w') as f:
                        f.write(result)
                if analyst:
                    with open(f"{os.path.splitext(outputfile)[0]}.out", 'wb') as f:
                        pickle.dump(analyst.readFromText(
                            result, filename=outputfile), f)
        return outputlist

    def runGaussianFromInput(self, inputstr):
        output = self.runCommand(self.command, inputstr=inputstr)
        return output

    def runGaussianFromGJF(self, filename):
        with open(filename) as f:
            output = self.runGaussianFromInput(f.read())
        return output

    def runGaussianWithOpenBabel(self, obabel_command):
        inputstr = self.runCommand(obabel_command)
        inputstr = self.generateGJF(inputstr)
        output = self.runGaussianFromInput(inputstr)
        return output

    def runGaussianFromType(self, filename, fileformat):
        obabel_command = f'obabel -i {fileformat} {filename} -ogjf'
        return self.runGaussianWithOpenBabel(obabel_command)

    def runGaussianFromSMILES(self, SMILES):
        obabel_command = f'obabel -:{SMILES} --gen3d -ogjf'
        return self.runGaussianWithOpenBabel(obabel_command)

    def generateGJF(self, gaussianstr):
        keywords = f'%nproc={self.nproc}\n# {self.keywords} {" scrf=smd " if self.solution else ""}'
        s = gaussianstr.split('\n')
        s[0] = keywords
        s[2] = 'Run automatically by GaussianRunner'
        return '\n'.join(s)
