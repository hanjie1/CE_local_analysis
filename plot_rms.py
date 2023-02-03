import numpy as np
import matplotlib.pyplot as plt
from map_tool import Tools
import pickle

datadir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4a/CRP4a_coldbox/results_LN2/"
#plotdir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/RT_coldbox/rms_plots/"

#datadir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/LN_coldbox/rms_results_1/"
#datadir1 = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/Plots/rms_results/"
#plotdir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/LN_coldbox/rms_plots/"

femb_no = [1,34,38,45,3,61,35,5,12,42,41,49]
#femb_no = [37,19,44,31,64,77,23,78,10,18,14,59]

sts=["1_0us","0_5us","3_0us","2_0us"]
bls=["900mV","200mV"]

def PlotCRP(rms,snc,st0,st1):
#def PlotCRP(rms,rms1,snc,st0,st1):
    uplane=[[]]*476
    vplane=[[]]*476
    xplane=[[]]*584

#    uplane1=[[]]*476
#    vplane1=[[]]*476
#    xplane1=[[]]*584
#
    smap = Tools()
    for i in range(12):
        df = smap.LoadMap(i+1)
    
        for ich in range(128):
            global_ch = i*128+ich
            plane,strip = smap.FindStrips(df, i+1, ich)
            if plane==1:
               uplane[strip-1]=rms[global_ch]
#               uplane1[strip-1]=rms1[global_ch]
            if plane==2:
               vplane[strip-1]=rms[global_ch]
#               vplane1[strip-1]=rms1[global_ch]
            if plane==3:
               xplane[strip-1]=rms[global_ch]
#               xplane1[strip-1]=rms1[global_ch]

    xx_u=range(476)
    xx_v=range(476,952)
    xx_x=range(952,1536)

    if st0==0 and st1==0:
       pkt=sts[0]
    if st0==1 and st1==0:
       pkt=sts[1]
    if st0==0 and st1==1:
       pkt=sts[2]
    if st0==1 and st1==1:
       pkt=sts[3]

    if snc==0:
       bl=bls[0]
    if snc==1:
       bl=bls[1]

    fname = "RMS_{}_{}".format(bl,pkt)
    
    plt.scatter(xx_u,uplane,marker='o',label='u plane')
    plt.scatter(xx_v,vplane,marker='o',label='v plane')
    plt.scatter(xx_x,xplane,marker='o',label='x plane')
#    plt.scatter(xx_u,uplane1,marker='o',label='u plane1')
#    plt.scatter(xx_v,vplane1,marker='o',label='v plane1')
#    plt.scatter(xx_x,xplane1,marker='o',label='x plane1')
    plt.legend()
    plt.title(fname)
#    plt.savefig(plotdir+fname+".png")
#    plt.ylim(0, 60)
#    plt.savefig(plotdir+fname+"_zoomin.png")
#    plt.close()
    plt.show()
        

for snc in [0,1]:
    for st0 in [0,1]:
        for st1 in [0,1]:
            all_rms=[]
            all_peds=[] 

            all_rms1=[]
            all_peds1=[] 
            for ifemb in femb_no:
               datafile = datadir + "RMS_snc{}_st0{}_st1{}_femb{}.bin".format(snc,st0,st1,ifemb)
               with open(datafile, 'rb') as fn:
                    tmppeds,tmprms = pickle.load(fn)
               all_peds = all_peds + tmppeds
               all_rms = all_rms + tmprms  

               #datafile1 = datadir1 + "RMS_snc{}_st0{}_st1{}_femb{}.bin".format(snc,st0,st1,ifemb)
               #with open(datafile1, 'rb') as fn:
               #     tmppeds1,tmprms1 = pickle.load(fn)
               #all_peds1 = all_peds1 + tmppeds1
               #all_rms1 = all_rms1 + tmprms1 
            
            PlotCRP(all_rms, snc, st0, st1) 
            #PlotCRP(all_rms, all_rms1, snc, st0, st1) 
                
 
            
