import pickle
import sys
import numpy as np
import matplotlib.pyplot as plt
from tools import ana_tools

#femb_no = [1,34,38,45,3,61,35,5,12,42,41,49]
femb_no = [37,19,44,31,64,77,23,78,10,18,14,59]
fembs = [0]

sts=["1_0us","0_5us","3_0us","2_0us"]
bls=["200mV","900mV"]

datadir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/RT_coldbox/rms_data/femb64_femb77_femb23_femb78_RT/"
plotdir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/RT_coldbox/rms_plots/"

for snc in [0,1]:
  for st0 in [0,1]:
      for st1 in [0,1]:
          datafile = datadir+"Raw_snc{}_st0{}_st1{}.bin".format(snc,st0,st1)
          qc_tools = ana_tools()
          
          with open(datafile, 'rb') as fn:
              raw = pickle.load(fn)
          
          rawdata = raw[0]
          pldata = qc_tools.data_decode(rawdata,fembs)
          pldata = np.array(pldata)
          
          ##### get fft
          nevent = len(pldata)
          for i in range(nevent):
              tmpdata1 = pldata[i,97]
              if i==0:
                 ch_fft1 = np.abs(np.fft.fft(tmpdata1))
              else:
                 ch_fft1 = ch_fft1 + np.abs(np.fft.fft(tmpdata1))
          
          ch_fft1 = ch_fft1/nevent
          
          dt = 0.5e-6 # MHz
          freq1 = np.fft.fftfreq(len(tmpdata1), d=dt)

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
                
          n_oneside=len(freq1)//2
          f_oneside = freq1[1:n_oneside]
          plt.plot(freq1[1:n_oneside], ch_fft1[1:n_oneside],label='{} {}'.format(bl,pkt))
plt.legend()
plt.title("FFT: Magnitude vs. freq (Hz)")
plt.show()
#
