"""GaussianAnalyst"""


import numpy as np


class GaussianAnalyst(object):
    def __init__(self, properties=["free_energy"]):
        self.properties = properties

    def readFromLOGs(self, filenamelist):
        return list(map(self.readFromLOG, filenamelist))

    def readFromLOG(self, filename):
        with open(filename) as f:
            flag = 0
            for line in f:
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
            read_properties["energy"] = energy
        if "free_energy" in self.properties:
            read_properties["free_energy"] = free_energy
        if "force" in self.properties:
            read_properties["force"] = np.array(force)
        if "atomic_number" in self.properties:
            read_properties["atomic_number"] = np.array(atomic_number)
        if "coordinate" in self.properties:
            read_properties["coordinate"] = np.array(coordinate)
        return read_properties
