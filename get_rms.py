import pickle
import numpy as np
from tools import ana_tools

#femb_no = [1,34,38,45,3,61,35,5,12,42,41,49]
femb_no = [37,19,44,31,64,77,23,78,10,18,14,59]
fembs = [0,1,2,3]

pathdir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/LN_coldbox/rms_data_1/"
qc_tools = ana_tools()

for i in range(2,3):
    fembids = [femb_no[i*4+0],femb_no[i*4+1],femb_no[i*4+2],femb_no[i*4+3]]
    datadir = pathdir+"femb{}_femb{}_femb{}_femb{}_LN/".format(fembids[0],fembids[1],fembids[2],fembids[3])
 
    for snc in [0,1]:
        for st0 in [0,1]:
            for st1 in [0,1]:

                datafile = datadir + "Raw_snc%d_st0%d_st1%d"%(snc,st0,st1) + ".bin"
                with open(datafile, 'rb') as fn:
                    raw = pickle.load(fn)

                rawdata = raw[0]
                pldata = qc_tools.data_decode(rawdata, fembs)
                pldata = np.array(pldata)

                for ifemb in fembs:
                    fp = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/LN_coldbox/rms_results_1/"
                    fname = "snc{}_st0{}_st1{}_femb{}".format(snc,st0,st1,fembids[ifemb])
                    tmp_ped,tmp_rms = qc_tools.GetRMS(pldata, ifemb, fp, fname)
                   
                     


