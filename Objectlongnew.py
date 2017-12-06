import numpy as np
from math import *
import subprocess
import csv
import traceback
import sys
import logging
import time
import datetime
import multiprocessing
import os
# from threading import Lock
from  threading import Lock

class delft3d:
    #  Global optimum: f(0,0,...,0)=0
    def __init__(self, dim=9):
        # self.xlow = np.zeros(dim)
        # self.xup = np.ones(dim)
        # PREPARE INPUT FILE  [Secchi, Vicouv, Dicouv, Vicoww, Dicoww, OzmidovXlo, Stantn, Dalton, Ccofu&v ]
        self.xlow = np.array([0.1, 0.1, 0.1, 0, 0, 0, 0.001, 0.001, 0.02])
        self.xup = np.array([2.0, 1.0, 1.0, 0.005, 0.005, 0.05, 0.002, 0.002, 0.03])
        # self.xlow = np.array([0.1, 0.1, 0.1, 0, 0])
        # self.xup = np.array([2.0, 1.0, 1.0, 0.005, 0.005])
        self.dim = dim
        self.info = str(dim) + " Ansoulate error function \n" + \
                    "Global optimum: f(0,0,...,0) = 0"
        self.integer = []
        self.continuous = np.arange(0, dim)
        self.simid = 0
        self.simlen = 365  # the simlutation length unit /day
        self.simiter = 0  # the iteration of the simulation
        self.lock = Lock()
        # self.exp_iteration = 1
        # self.exp_simid = []

    def objfunction(self, x, simid, simiter, workdir):
        # with self.lock:
        #     abssimid = self.simid
        #     logging.info('SimID: the absoluate simulationID is %d ' % abssimid)
        #     self.simid = self.simid + 1
        # simiter = (abssimid ) // 24 + 1
        # simid = (abssimid + 1) % 24
        simid = simid
        simiter = simiter
        workingdir = workdir
        os.chdir(workingdir)

        logging.info('The %d iteration %d simulation called objfunction' % (simiter, simid))
        # t_pal1 = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        # fp = open("/home/users/nus/e0225114/scratch/xiawei/pub_flow/run_time.txt", "a")
        # fp.write("EvaluationBegin: %d iteration %d evaluation %s \n" % (simiter, simid, t_pal1))
        # fp.close()

        if len(x) != self.dim:
            raise ValueError('Dimension mismatch')
        try:
            object_value = self.delft3d_flow(x, simiter, simid, workdir)
        except:
            # logging.info('CalculateError: %d iteration %d evaluation calculate abnormally' % (simiter, simid))
            # exc_type, exc_value, exc_traceback = sys.exc_info()
            # logging.exception("Trackback Error:%d iteration %d evaluation" % (simiter, simid))
            # parms = x.tolist()
            # fp = open("/home/users/nus/e0225114/scratch/xiawei/pub_flow/pysot_result.txt", "a")
            # fp.write("%s\t%s\t%s\t@%s\n" % (simiter, simid, 'None', parms))
            # fp.close()
            # t_pal2 = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            # fp = open("/home/users/nus/e0225114/scratch/xiawei/pub_flow/run_time.txt", "a")
            # fp.write("EvaluationEnd: %d iteration %d evaluation %s \n" % (simiter, simid, t_pal2))
            # fp.close()
            return 0  # return a big enough value
        else:
            # parms = x.tolist()
            # fp = open("/home/users/nus/e0225114/scratch/xiawei/pub_flow/pysot_result.txt", "a")
            # fp.write("%s\t%s\t%s\t@%s\n" % (simiter, simid, object_value, parms))
            # fp.close()
            # t_pal2 = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            # fp = open("/home/users/nus/e0225114/scratch/xiawei/pub_flow/run_time.txt", "a")
            # fp.write("EvaluationEnd: %d iteration %d evaluation %s \n" % (simiter, simid, t_pal2))
            # fp.close()
            return object_value

    def delft3d_flow(self, x, simiter, simid, workdir):
        # [Secchi, Vicouv, Dicouv, Vicoww, Dicoww]
        simiter = simiter
        str_dir = simid
        workingdir = workdir
        fp = open("TEST_AGAIN.txt", "a")
        fp.write("this is the x in simulaiton 1: %s\n" % (str(x)))
        fp.write("this is the x %s in simulaiton %d iteration %d:\n" % (str(x), simid, simiter))
        fp.close()

        # ---------------------modify the MDF file -----------------#
        #   x=[1.0,0.5,0.5,0.00005,0.00005]
        # PREPARE INPUT FILE  [Secchi, Vicouv, Dicouv, Vicoww, Dicoww, OzmidovXlo, Stantn, Dalton, Ccofu&v ]
        # par_linenum = [71, 82, 83, 85, 86, 81, 72, 73, 79, 80]  # the respective line numbers of these parameters in the .bsn file
        # fp = open(workingdir + "/up22.mdf", "rb")
        # file_copy = fp.readlines()
        # for i in range(len(par_linenum)):
        #     if i == (len(par_linenum) - 1):
        #         par = "{:.7e}".format(x[i-1])
        #         str1 = file_copy[par_linenum[i]]
        #         str2 = str1.split()
        #         str3 = str2[0] + ' ' + str2[1] + '  ' + str(par) + '\n'
        #         file_copy[par_linenum[i]] = str3
        #     else:
        #         par = "{:.7e}".format(x[i])
        #         str1 = file_copy[par_linenum[i]]
        #         str2 = str1.split()
        #         str3 = str2[0] + ' ' + str2[1] + '  ' + str(par) + '\n'
        #         file_copy[par_linenum[i]] = str3
        # fp.close()
        # fp = open(workingdir + "/up22.mdf", "wb")
        # for item in file_copy:
        #     fp.write("%s" % item)
        # fp.close()
        # logging.info('%s iteration %s evaluation: finished changing the MDF file' % (simiter, str_dir))
        #
        # # ----------------------run the delft3D model on linux--------------------------#
        # # cmd = './clean.sh'
        # # subprocess.call(cmd, cwd=workingdir)
        # # logging.info('%s iteration %s evaluation: finished cleanning the orginal data' % (simiter, str_dir))
        # t3 = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        # fp = open("/home/users/nus/e0225114/scratch/xiawei/pub_flow/run_time.txt", "a")
        # fp.write("SimulationBegin: %d iteration %d evaluation %s \n" % (simiter, simid, t3))
        # fp.close()
        # t0 = time.time()
        try:
            os.system(workingdir + "run_flow2d3d_parallel.sh >null")
            # cmd = './run_flow2d3d.sh'
            # subprocess.Popen(cmd, cwd=workingdir).wait()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            logging.exception("Trackback Error:%d iteration %d evaluation" % (simiter, simid))

            pass
        else:
            obj_val = 1
            # t1 = time.time()
            # t2 = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            # str_dir = str(str_dir)
            # fp = open("/home/users/nus/e0225114/scratch/xiawei/pub_flow/run_time.txt", "a")
            # fp.write("SimulationEnd: %d iteration %d evaluation %s \n" % (simiter, simid, t2))
            # fp.close()
            # logging.info('%s iteration %s evaluation: finished simulation' % (simiter, str_dir))
            # cmd2 = './his2dat.sh'
            # subprocess.call(cmd2, cwd=workingdir) # convert the histroy file to python readable dat file
            #
            # simiter_name = '{:0>3}'.format(simiter)
            # command = "cp %s/Tem.dat /home/users/nus/e0225114/scratch/xiawei/pub_flow/history_data/%s_%sTem.dat" % (
            # workingdir, simiter_name, simid)
            # subprocess.call(command, shell=True, cwd=workingdir)
            # # ----------------read Mearsured dat-----------------------#
            # file_name1 = workingdir + "/Tem_measured3.csv"
            # Tem_measured_sur, Tem_measured_mid, Tem_measured_bot = self.read_measured_data(file_name1)
            # logging.info('%s iteration %s evaluation: finished reading the measured data' % (simiter, str_dir))
            # # ---------------------read simulation data from delft3D model-----------------#
            # file_name2 = workingdir + "/Tem.dat"
            # Tem_sur, Tem_mid, Tem_bot = self.read_simulation_data(file_name2, 5, 19, 9, 3)
            # logging.info('%s iteration %s evaluation: finished reading the simulation data' % (simiter, str_dir))
            # nes_tem_sur = self.compute_nse(Tem_measured_sur, Tem_sur)
            # nes_tem_mid = self.compute_nse(Tem_measured_mid, Tem_mid)
            # nes_tem_bot = self.compute_nse(Tem_measured_bot, Tem_bot)
            # obj_val = -1 * (nes_tem_sur + nes_tem_mid + nes_tem_bot)
            # logging.info('%s iteration %s evaluation: finished calculating the objection function' % (simiter, str_dir))
            return obj_val

    def read_simulation_data(self, filename, station_id, layer_sur, layer_mid, layer_bot):
        filename = filename
        station = station_id
        layer_surface = layer_sur  # 0.5 m
        layer_middle = layer_mid  # 10 m
        layer_bottom = layer_bot  # 18
        f = open(filename, "r")
        file_copy = f.readlines()
        str1 = file_copy[3]
        str2 = str1.split()
        nrow = int(str2[0])
        ncol = int(str2[1])
        nplane = int(str2[2])
        print (nrow, ncol, nplane)
        f.close()
        Tem_sur = []
        Tem_mid = []
        Tem_bot = []
        for i in range(nplane):
            str1 = file_copy[3 + station + 17 * i]
            str2 = str1.split()
            tem = []
            tem.append(i + 1)
            tem.append(float(str2[layer_surface - 1]))
            Tem_sur.append(tem)
            tem = []
            tem.append(i + 1)
            tem.append(float(str2[layer_middle - 1]))
            Tem_mid.append(tem)
            tem = []
            tem.append(i + 1)
            tem.append(float(str2[layer_bottom - 1]))
            Tem_bot.append(tem)
        Tem_sur = np.asarray(Tem_sur)
        Tem_mid = np.asarray(Tem_mid)
        Tem_bot = np.asarray(Tem_bot)
        return Tem_sur, Tem_mid, Tem_bot

    def read_measured_data(self, filename):
        filename = filename
        Tem_measured_sur = []
        Tem_measured_mid = []
        Tem_measured_bot = []

        with open(filename) as f:
            reader = csv.reader(f, delimiter=",")
            i = 1
            for row in reader:
                if ((i > 1416) & (i < (self.simlen * 24 + 3))):  # without the warm-up time

                    if row[2] is not "":
                        tem = []
                        tem.append(i - 1)
                        tem.append(float(row[2]))  # 0.5 Meter
                        Tem_measured_sur.append(tem)
                    else:
                        pass
                    if row[7] is not "":
                        tem = []
                        tem.append(i - 1)
                        tem.append(float(row[7]))  # 10 Meter
                        Tem_measured_mid.append(tem)
                    else:
                        pass
                    if row[8] is not "":
                        tem = []
                        tem.append(i - 1)
                        tem.append(float(row[8]))  # 14 Meter
                        Tem_measured_bot.append(tem)
                    else:
                        pass
                i = i + 1
        f.close()

        Tem_measured_sur = np.asarray(Tem_measured_sur)
        Tem_measured_mid = np.asarray(Tem_measured_mid)
        Tem_measured_bot = np.asarray(Tem_measured_bot)

        return Tem_measured_sur, Tem_measured_mid, Tem_measured_bot

    def compute_nse(self, obs, sim):
        mean_obs = np.mean(obs[:, 1])
        n = np.size(obs, 0)
        m = np.size(sim, 0)
        num = 0.0
        den = 0.0
        for i in range(n):
            den = den + (obs[i, 1] - mean_obs) ** 2
            for j in range(m):
                if sim[j, 0] == obs[i, 0]:
                    num = num + (obs[i, 1] - sim[j, 1]) ** 2
                    break
        nse = 1 - (num / den)
        return nse











