"""GaussianAnalyst."""


import numpy as np


class GaussianAnalyst:
    def __init__(self, properties=None):
        self.properties = properties if properties else ["energy"]

    def readFromLOGs(self, filenamelist):
        return list(map(self.readFromLOG, filenamelist))

    def readFromLOG(self, filename):
        with open(filename) as f:
            return self.readFromLines(f, filename=filename)

    def readFromText(self, text, filename=None):
        return self.readFromLines(text.splitlines(), filename=filename)

    def readFromLines(self, lines, filename=None):
        flag = 0
        for line in lines:
            if line.startswith(" SCF Done") and "energy" in self.properties:
                energy = float(line.split()[4])
            elif "Sum of electronic and thermal Free Energies=" in line and "free_energy" in self.properties:
                free_energy = float(line.split()[-1])
            elif line.startswith(" Center     Atomic                   Forces (Hartrees/Bohr)") and "force" in self.properties:
                flag = 1
                force = []
            elif line.startswith("                          Input orientation:") and ("coordinate" in self.properties or "atomic_number" in self.properties):
                flag = 5
                if "coordinate" in self.properties:
                    coordinate = []
                if "atomic_number" in self.properties:
                    atomic_number = []

            if 1 <= flag <= 3 or 5 <= flag <= 9:
                flag += 1
            elif flag == 4:
                if line.startswith(" -------"):
                    flag = 0
                else:
                    s = line.split()
                    force.append([float(x) for x in s[2:5]])
            elif flag == 10:
                if line.startswith(" -------"):
                    flag = 0
                else:
                    s = line.split()
                    if "atomic_number" in self.properties:
                        atomic_number.append(int(s[1]))
                    if "coordinate" in self.properties:
                        coordinate.append([float(x) for x in s[3:6]])

        read_properties = {'name': filename}
        if "energy" in self.properties:
            try:
                read_properties["energy"] = energy
            except:
                read_properties["energy"] = None
        if "free_energy" in self.properties:
            try:
                read_properties["free_energy"] = free_energy
            except:
                read_properties["free_energy"] = None
        if "force" in self.properties:
            try:
                read_properties["force"] = np.array(force)
            except:
                read_properties["force"] = None
        if "atomic_number" in self.properties:
            try:
                read_properties["atomic_number"] = np.array(atomic_number)
            except:
                read_properties["atomic_number"] = None
        if "coordinate" in self.properties:
            try:
                read_properties["coordinate"] = np.array(coordinate)
            except:
                read_properties["coordinate"] = None
        return read_properties
