import numpy as np
import matplotlib.pyplot as plt
from map_tool import Tools
import pickle

datadir = "results/"

#femb_no = [1,34,38,45,3,61,35,5,12,42,41,49]
femb_no = [1,34,38,45,3,61,35,5]

for snc in [0,1]:
    for st0 in [0,1]:
        for st1 in [0,1]:
            all_rms=[]
            all_peds=[] 
            for ifemb in femb_no:
               datafile = datadir + "RMS_snc{}_st0{}_st1{}_femb{}.bin".format(snc,st0,st1,ifemb)
               with open(datafile, 'rb') as fn:
                    tmppeds,tmprms = pickle.load(fn)

               all_peds = all_peds + tmppeds
               all_rms = all_rms + tmprms  
            
            xx = range(len(all_rms)) 
            plt.plot(xx,all_rms)
            plt.show()
 
            
