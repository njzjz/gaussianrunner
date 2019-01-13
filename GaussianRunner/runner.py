"""GaussianRunner"""


from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import subprocess as sp
import time


class GaussianRunner(object):
    def __init__(self, command="g16", cpu_num=None, nproc=4, keywords='', solution=False):
        self.command = command
        self.cpu_num = cpu_num if cpu_num else cpu_count()
        self.nproc = nproc
        self.thread_num = self.cpu_num//self.nproc
        self.keywords = keywords
        self.solution = solution

    def _logging(self, *message):
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime, 'GaussianRunner', *message)

    def runCommand(self, command, input=None):
        try:
            output = sp.check_output(command.split(), input=(
                input.encode() if input else None)).decode('utf-8')
        except sp.CalledProcessError as e:
            output = e.output.decode('utf-8')
            self._logging("ERROR: Run command", command)
        return output

    def runGaussianFunction(self, type):
        if type == 'input':
            function = self.runGaussianFromInput
        elif type == 'smiles':
            function = self.runGaussianFromSMILES
        elif type == 'gjf':
            function = self.runGaussianFromGJF
        elif type == 'xyz':
            function = self.runGaussianFromXYZ
        elif type == 'pdb':
            function = self.runGaussianFromPDB
        elif type == 'mol':
            function = self.runGaussianFromMOL
        else:
            self.fileformat = type
            function = self.runGaussianFromOthers
        return function

    def generateLOGfilename(self, inputtype, inputlist):
        if inputtype == 'input':
            outputlist = range(len(inputlist))
        elif inputtype == 'smiles':
            outputlist = [x.replace('/', '／') .replace('\\', '＼')
                          for x in inputlist]
        else:
            outputlist = [
                x[:-len(inputtype)-1] if x.lower().endswith("."+inputtype) else x for x in inputlist]
        outputlist = [x+".log" for x in outputlist]
        return outputlist

    def runGaussianInParallel(self, inputtype, inputlist, outputlist=None):
        inputtype = inputtype.lower()
        function = self.runGaussianFunction(inputtype)
        outputlist = outputlist if outputlist else self.generateLOGfilename(
            inputtype, inputlist)
        with ThreadPool(self.thread_num) as pool:
            results = pool.imap(function, inputlist)
            for index, result in enumerate(results):
                with open(outputlist[index], 'w') as f:
                    print(result, file=f)
        return outputlist

    def runGaussianFromInput(self, input):
        output = self.runCommand(self.command, input=input)
        return output

    def runGaussianFromGJF(self, filename):
        with open(filename) as f:
            output = self.runGaussianFromInput(f.read())
        return output

    def runGaussianWithOpenBabel(self, obabel_command):
        input = self.runCommand(obabel_command)
        input = self.generateGJF(input)
        output = self.runGaussianFromInput(input)
        return output

    def runGaussianFromType(self, filename, fileformat):
        obabel_command = 'obabel -i'+fileformat+' '+filename+' -ogjf'
        return self.runGaussianWithOpenBabel(obabel_command)

    def runGaussianFromXYZ(self, filename):
        return self.runGaussianFromType(filename, 'xyz')

    def runGaussianFromPDB(self, filename):
        return self.runGaussianFromType(filename, 'pdb')

    def runGaussianFromMOL(self, filename):
        return self.runGaussianFromType(filename, 'mol')

    def runGaussianFromOthers(self, filename):
        return self.runGaussianFromType(filename, self.fileformat)

    def runGaussianFromSMILES(self, SMILES):
        obabel_command = 'obabel -:'+SMILES+' --gen3d -ogjf'
        return self.runGaussianWithOpenBabel(obabel_command)

    def generateGJF(self, input):
        keywords = '%nproc=' + \
            str(self.nproc)+'\n# '+self.keywords + \
            (' scrf=smd ' if self.solution else '')
        s = input.split('\n')
        s[2] = 'Run automatically by GaussianRunner'
        input = '\n'.join(s)
        output = input.replace(
            '#Put Keywords Here, check Charge and Multiplicity.', keywords)
        return output