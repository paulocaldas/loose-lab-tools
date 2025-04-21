# Loose Lab Tools

### Useful scripts for Martin's lab
Lab: https://looselab.ist.ac.at/

### notebooks:
 
#### Step Size Distribution Analysis
Functions designed to compute directionality by analyzing the distribution of step sizes, which refers to the variation in distances moved between successive points in a given process. While this approach has not yet been fully optimized, it holds significant potential for future applications.
 
#### Visualize Individual Trajectories
It runs with a single input: path/to/filename (the main functions are located in the src folder). <br>
This script allows the user to view multiple plots displaying dozens of trajectories, providing an overview of the types of trajectories available in the dataset."
 
#### Photobleach-Correction Automatization <br> 
approach adapted from https://pubmed.ncbi.nlm.nih.gov/28065316/ 
 
data from each experiment is fitted to mono-exponential decay using:
f(x) = A.exp(-x/tau_app)

then we assume that
1/tau_app = 1/tau + k_pb
k_pb = t_ex.c_pb/t_acq

where tau_app is the apparent lifetime of each experiment, which depends on the true lifetime (tau) <br>
and on the photobleaching constant (k_pb), proportional to the exposure time (t_ex) and a photobleaching constant (c_pb) <br>
and inversely proportional to the acquisition rate (t_acq).

both equations can be written as :
t_acq/tau_app = t_acq/tau + t_ex.c_pb

then in a linear fit (a = mx + b) these would correspond to:

a = t_acq/tau_app
m = 1/tau
b = t_ex * c_pb
