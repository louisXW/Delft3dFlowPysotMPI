import os
from Objectlongnew import *

import sys
import argparse
import numpy as np
first_arg = sys.argv[0]
second_arg = sys.argv[1]
third_arg = sys.argv[2]
fouth_arg = sys.argv[3]
x = second_arg
simid =int(third_arg)
simiter = int(fouth_arg)
x = x.split(',')
y = []
for item in x:
   y.append(float(item))
x = np.array(y)
workingdir = "/home/users/nus/e0022672/delft3d/examples/" + str(simid) + "/"
os.chdir(workingdir)
fp = open("TEST_AGAIN_1.txt", "a")
fp.write("this is the x in simulaiton 1: %s\n" % (str(x)))
fp.write("this is the x %s in simulaiton %d iteration %d:\n" % (str(x), simid, simiter))
fp.close()

data = delft3d(dim=9)
y = data.objfunction(x, simid, simiter, workingdir)
print y
