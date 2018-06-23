import re


########################################################################
class dataRoot:

    """docstring for dataRoot"""
    def __init__(self, win):

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

