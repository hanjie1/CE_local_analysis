import pickle
import sys
import numpy as np
import matplotlib.pyplot as plt
from tools import ana_tools
from map_tool import Tools

u_fft=[[]]*476
v_fft=[[]]*476
x_fft=[[]]*584

u_freq=[[]]*476
v_freq=[[]]*476
x_freq=[[]]*584

def GetFFT(data,nset):
    nevent = len(data)
    nchn = len(data[0])
    dt = 0.5e-6 # MHz

    smap = Tools()
    for ifemb in range(4):
        nfemb = ifemb+nset*4
        df = smap.LoadMap(nfemb+1)

        for ich in range(128):
            global_ch = ifemb*128+ich
            for iev in range(nevent):
              ch_data = data[iev,global_ch]
              if iev==0:
                 ch_fft = np.abs(np.fft.rfft(ch_data))
              else:
                 ch_fft = ch_fft + np.abs(np.fft.rfft(ch_data))
  
            ch_fft = ch_fft/nevent
            ch_fft = 10*np.log10(ch_fft)
    
            ch_freq = np.fft.rfftfreq(len(ch_data), d=dt)
    
            plane,strip = smap.FindStrips(df, nfemb+1, ich)
            if plane==1:
               u_fft[strip-1]=ch_fft
               u_freq[strip-1]=ch_freq
            if plane==2:
               v_fft[strip-1]=ch_fft
               v_freq[strip-1]=ch_freq
            if plane==3:
               x_fft[strip-1]=ch_fft
               x_freq[strip-1]=ch_freq


#femb_no = [1,34,38,45,3,61,35,5,12,42,41,49]
femb_no = [37,19,44,31,64,77,23,78,10,18,14,59]
fembs = [0,1,2,3]

#pathdir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/CRP/CRP4a/coldbox_final/coldbox_data_LN2/"
#plotdir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/CRP/CRP4a/coldbox_final/fft_plots_LN2/"

pathdir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/CRP/CRP4b/LN_coldbox/rms_data_1/"
plotdir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/CRP/CRP4b/LN_coldbox/fft_plots_1/"

qc_tools = ana_tools()

for i in range(0,3):
    fembids = [femb_no[i*4+0],femb_no[i*4+1],femb_no[i*4+2],femb_no[i*4+3]]
    datadir = pathdir+"femb{}_femb{}_femb{}_femb{}_LN/".format(fembids[0],fembids[1],fembids[2],fembids[3])

    datafile = datadir + "Raw_snc1_st01_st11.bin"
    with open(datafile, 'rb') as fn:
        raw = pickle.load(fn)

    rawdata = raw[0]
    pldata = qc_tools.data_decode(rawdata, fembs)
    pldata = np.array(pldata)

    GetFFT(pldata,i)
  
for i in range(476):
    nl = (i+1)%14
    nn = (i+1)/14
    if nl==1:
       plt.subplots(figsize=(15, 9))

    strip_fft = u_fft[i][1:]
    strip_fft = 10*np.log10(strip_fft)
    plt.plot(u_freq[i][1:],strip_fft,label='u_strip%d'%i)
    if nl==0:
       plt.legend()
       plt.title("u plane FFT magnitude(dB) vs. freq(Hz) LN")
       plt.savefig(plotdir+"uplane%d"%nn+".png")
       plt.close()

for i in range(476):
    nl = (i+1)%14
    nn = (i+1)/14
    if nl==1:
       plt.subplots(figsize=(15, 9))

    strip_fft = v_fft[i][1:]
    strip_fft = 10*np.log10(strip_fft)
    plt.plot(v_freq[i][1:],strip_fft,label='v_strip%d'%i)
    if nl==0:
       plt.legend()
       plt.title("v plane FFT magnitude(dB) vs. freq(Hz) LN")
       plt.savefig(plotdir+"vplane%d"%nn+".png")
       plt.close()

for i in range(584):
    nl = (i+1)%8
    nn = (i+1)/8
    if nl==1:
       plt.subplots(figsize=(15, 9))

    strip_fft = x_fft[i][1:]
    strip_fft = 10*np.log10(strip_fft)
    plt.plot(x_freq[i][1:],strip_fft,label='x_strip%d'%i)
    if nl==0:
       plt.legend()
       plt.title("x plane FFT magnitude(dB) vs. freq(Hz) LN")
       plt.savefig(plotdir+"xplane%d"%nn+".png")
       plt.close()

