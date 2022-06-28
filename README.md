# Loose Lab Tools

### functions and algorithms that might be useful

#### notebooks:
 
#### Step Size Distribution Analysis
functions to compute directionality using this approach <br>
still not used efficiently, but has potential
 
#### Visualize Individual Trajectories
small script to visualize multiple trajectories <br>
runs with a single input: path/to/filename (main functions are in the src folder)
 
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
