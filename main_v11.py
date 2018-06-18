#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
import re
import matplotlib
import matplotlib.pyplot as plt
import argparse
import numpy as np
import warnings

#from PyQt5 import QtWidgets



class dataRoot(object):
    """docstring for dataRoot"""
    def __init__(self,win):
        super(dataRoot, self).__init__()
        self.win = win
        self.dic = {"date" :[0]*win,"hour": [0]*win,"SN":[0]*win,"CHAN":[0]*win,
                   "sysALARM":[0]*win,"SPO2":[0]*win,"BPM":[0]*win,"PI":[0]*win,
                   "SPHB":[0]*win,
                   "DESAT":[0]*win,"PIDELTA":[0]*win,
                   "PVI":[0]*win,
                   "TVI":[0]*win,
                   "ALARM":[0]*win,"ALARM1":[0]*win,
                   "ACSALARM":[0]*win,"EXC":[0]*win,"EXC1":[0]*win,"EXC2":[0]*win,
                   "ACSEXC":[0]*win,"eegPSI":[0]*win,"eegEMG":[0]*win,"eegSR":[0]*win,
                   "eegSEFL":[0]*win,"eegSEFR":[0]*win,"eegARTF":[0]*win,"eegALARM":[0]*win,
                   "umgALARM":[0]*win,
                   "eegEXC":[0]*win,
                   "kapnoFiSO2":[0]*win,
                   "capnoFiCO2":[0]*win,"capnoEtCO2":[0]*win,"capnoRR":[0]*win,
                   "capnoALARM":[0]*win,"capnoALARM1":[0]*win,"capnoEXC":[0]*win,"nibpSYS":[0]*win,
                   "nibpDIA":[0]*win,"nibpMAP":[0]*win,"nibpPR":[0]*win,"nibpALARM":[0]*win,
                   "nibpEXC":[0]*win,"nibpMEASTIME":[0]*win,"tempParam":[0]*win,"tempALARM": [0]*win,
                   "tempEXC":[0]*win,"tempMEASTIME":[0]*win}
        

    def parseRoot(self, vec):
        fields = vec.split()
        keys = self.dic.keys()
        fieldkeys = [(lambda x: x in fields )(x) for x in keys]

        if len(self.dic['date']) < self.win:
            self.dic['date'].append(str(fields[0]))
            self.dic['hour'].append(str(fields[1][0:5]))
        else:
            self.dic['date'].pop(0)
            self.dic['hour'].pop(0)
            self.dic['date'].append(fields[0])
            self.dic['hour'].append(fields[1][0:5])
        
        for fd in range(2,len(fields[2:])):
            tmp = fields[fd].split('=')

            if tmp[0] in keys:
                try:
                    if len(self.dic[tmp[0]]) < self.win:
                        self.dic[tmp[0]].append(float(re.sub('[a-zA-Z%]','',tmp[-1])))
                    else:
                        self.dic[tmp[0]].pop(0)
                        self.dic[tmp[0]].append(float(re.sub('[a-zA-Z%]','',tmp[-1])))
                except :
                    if len(self.dic[tmp[0]]) < self.win:
                        self.dic[tmp[0]].append(0)
                    else:
                        self.dic[tmp[0]].pop(0)
                        self.dic[tmp[0]].append(0)
            else:
                self.dic[keys[fd]].pop(0)
                self.dic[keys[fd]].append(np.nan)

        return self.dic



def handle_close(evt):
    print('Closed Figure!')



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-sP", "--serialPort", required=True, type = str,help="Port, example: COM1")
ap.add_argument("-bR", "--baudRate", required=True,type = int, help="baudrate example: 921600 ")
ap.add_argument("-w", "--window", required=True,type=int, help="windows in minutes")
ap.add_argument("-nF", "--nameFile", required=True,type=str, help="Name of the file, it must have an extension .txt")

args = vars(ap.parse_args())

warnings.filterwarnings("ignore")

# Create the serial object
serialPort = args["serialPort"]
bau = args["baudRate"]
win = args["window"]*60
nameFile = args["nameFile"]

serialObject = serial.Serial(serialPort,baudrate=bau,timeout = 1.0);
file = open(nameFile, "w")
root = dataRoot(win)


fig = plt.figure()
fig.canvas.mpl_connect('close_event', handle_close)
fig.patch.set_facecolor('black')
matplotlib.rc('axes',edgecolor='white')

t = range(0,win)
XTicks2 = np.array(range(0,win,60)) 
count2 =0

while True:
    data = str(serialObject.readline())
    file.write(data)
    if count2 == -59:
        count2 = 0
        XTicks = np.array(range(0,win,60))
    else:
        XTicks = np.array(range(count2,win,60))
        count2 -=1
        XTicks= XTicks[XTicks> 0]


    plot_vec = root.parseRoot(data)
    tmp = plot_vec['hour']
    if tmp[XTicks[-1]] != 0 :
         Ticks = [(lambda x,tmp: tmp[x] )(x,tmp) for x in XTicks]
    else:
        Ticks = [0]*len(XTicks)



    plt.clf()

    ax = fig.add_subplot(321)
    plt.rcParams['axes.facecolor'] = 'black'
   #plt.rcParams['legend.handletextpad'] = 'white'
    plt.plot(t,plot_vec['SPO2'])
    plt.hold(True)
    plt.plot(t,plot_vec['BPM'])
    plt.legend(["SPO2","BPM"],loc=1)
    plt.hold(False)
    plt.ylim([0, 100])
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.xticks(XTicks,Ticks)
    plt.draw()


    ax = fig.add_subplot(322)
    plt.plot(t,plot_vec['eegPSI'])
    plt.legend(["PSI"],loc=1)
    plt.ylim([0, 100])
    plt.hold(False)
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.xticks(XTicks,Ticks)
    plt.draw()


    ax = fig.add_subplot(323)
    plt.plot(t,plot_vec['capnoFiCO2'])
    plt.hold(True)
    plt.plot(t,plot_vec['capnoEtCO2'])
    plt.plot(t,plot_vec['capnoRR'])
    plt.legend(["FiCO2","EtCO2","RR"],loc=1)
    plt.hold(False)
    plt.ylim([0, 50])
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.xticks(XTicks,Ticks)
    plt.draw()

    ax = fig.add_subplot(324)
    plt.plot(t,plot_vec['nibpSYS'])
    plt.hold(True)
    plt.plot(t,plot_vec['nibpDIA'])
    plt.plot(t,plot_vec['nibpMAP'])
    plt.plot(t,plot_vec['nibpPR'])
    plt.legend(["SYS","DIA","MAP","PR"],loc=1)
    plt.hold(False)
    plt.ylim([0, 120])
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.xticks(XTicks,Ticks)
    plt.draw()

    ax = fig.add_subplot(325)
    plt.plot(t,plot_vec['tempParam'])
    plt.legend(["temperature"],loc=1)
    plt.ylim([0, 50])
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.xticks(XTicks,Ticks)
    plt.draw()

    ax = fig.add_subplot(326)
    plt.plot(t,plot_vec['BPM'])
    plt.plot(t,plot_vec['eegPSI'])
    plt.legend(["BPM","PSI"],loc=1)
    plt.ylim([0, 100])
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.xticks(XTicks,Ticks)
    plt.draw()

    plt.pause(0.5)

serialObject.close()
file.close()
