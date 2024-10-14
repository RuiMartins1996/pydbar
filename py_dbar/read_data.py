import numpy as np
import math
from numpy import linalg as LG

#For error handling
import os
import sys


pi = math.pi

# Our general class will read a Current file and a Voltages file to output a Dirichlet to Neumann map.
# Variables: 
# r - radius of body (assumed symmetrical for now) 
# AE -  area of the electrodes
# L - Number of Electrodes
class read_data:

    def __init__(self, parentLocalFolder, r, AE, L):
        self.L = L
        self.r = r
        self.AE = AE

        cwd = os.getcwd()

        parentGlobalFolder = cwd+"/"+parentLocalFolder

        try:
            
            if os.path.isdir(parentGlobalFolder):
            
                currentFile = parentGlobalFolder+"/Current.txt"
                voltageFile = parentGlobalFolder+"/Voltage.txt"
                if os.path.exists(currentFile) and os.path.exists(voltageFile):
                    Current = np.loadtxt(currentFile) 
                    Voltage = np.loadtxt(voltageFile)
                else:
                    raise FileNotFoundError(f"Either '{currentFile}' or '{voltageFile}' do not exist.")
            else:
                raise FileNotFoundError(f"Folder '{parentGlobalFolder}' is not a directory!")
        except Exception as e:
            print(f"Exception: {e}")
            sys.exit(1)


        self.Current = Current.transpose() # Matrix L x L-1
        self.Voltage = Voltage.transpose() # Matrix L x L-1
        self.DNmap = np.zeros((L-1, L-1))
        self.load()
        
    def load(self):
        
        self.Voltage[:,0] = self.Voltage[:, 0]/LG.norm(self.Current[:,0], 2)
        self.Current[:,0] = self.Current[:, 0]/LG.norm(self.Current[:,0], 2)
        
        for j in range(1, self.L-1):
            for jj in range(j):
                coef = np.inner(self.Current[:,j], self.Current[:, jj])
                self.Current[:, j] = self.Current[:, j] - coef*self.Current[:, jj]
                self.Voltage[:, j] = self.Voltage[:, j] - coef*self.Voltage[:, jj]
            
            self.Voltage[:, j] = self.Voltage[:, j]/LG.norm(self.Current[:, j], 2)
            self.Current[:, j] = self.Current[:, j]/LG.norm(self.Current[:, j], 2)
            
        for n in range(self.L-1):
            for m in range(self.L-1):
                C = self.Current[:, n]
                V = self.Voltage[:, m]
                self.DNmap[n, m] = np.inner(C, V)
                
        self.DNmap = (self.AE/self.r)*LG.inv(self.DNmap)
        
