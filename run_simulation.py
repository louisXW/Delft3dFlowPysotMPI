import os
#rank = 1
workingdir = "/home/users/nus/e0022672/delft3d/examples/01_standard/"
os.chdir(workingdir)
os.system(workingdir + "run_flow2d3d_parallel.sh >null")
print 2
