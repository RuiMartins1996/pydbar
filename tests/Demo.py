import sys
import os 

# Add cwd (containg the py_dbar module) to system path at the first position
# Assume the cwd is .../tests
sys.path.insert(0,os.getcwd())

from py_dbar import read_data, k_grid, dBar

# Parameters
L = 16                  #Number of electrodes
R = 1                   #Tank radius
A = 1                   #Electrode area

# Read the boundary measurements and create the Dirichlet-to-Neumann map
# Assuming the cwd is .../pydbar
parentFolderNow = "tests/EIT_Data/Object1"      #local path to data relative to cwd 
parentFolderHomo = "tests/EIT_Data/ObjectH"     #local path to data relative to cwd 

# Frame to determine the conductivity: 
Now = read_data.read_data(parentFolderNow, R, A, L)
# Frame of Reference - Homogeneous
Ref = read_data.read_data(parentFolderHomo, R, A, L)

# Establish a k_grid which corresponds to a spectral parameter
Kp = k_grid.k_grid(4, 4)

# Creates the model which corresponds to the Dbar equation in the spectral parameter at each z of a z_grid.
scatteringType = "partial"      
model = dBar.dBar(scatteringType, Kp, Now, Ref, 1., 4)

# Solves the problem for each z in the 2D plane, hence determining the conductivity at each z
model.solve()

# Plots the solution
model.plot()
