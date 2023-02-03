import pickle
import sys
import numpy as np
import matplotlib.pyplot as plt
from tools import ana_tools

def GetFFT(data,ch):
    nevent = len(data)
    for i in range(nevent):
        ch_data = data[i,ch]
        if i==0:
           ch_fft = np.abs(np.fft.fft(ch_data))
        else:
           ch_fft = ch_fft + np.abs(np.fft.fft(ch_data))
    
    ch_fft = ch_fft/nevent
    
    dt = 0.5e-6 # MHz
    freq = np.fft.fftfreq(len(ch_data), d=dt)
    return ch_fft,freq

femb_no = [1,34,38,45,3,61,35,5,12,42,41,49]
#femb_no = [37,19,44,31,64,77,23,78,10,18,14,59]
nfemb=2
fembs = [2]

#datadir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/LN_coldbox/rms_data_1/femb10_femb18_femb14_femb59_LN/"
datadir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4a/CRP4a_coldbox/coldbox_data_RT2/femb1_femb34_femb38_femb45_RT_R001/"
plotdir = "/Users/hanjie/Desktop/cold_electronics/CRP/CRP4/CRP4b/LN_coldbox/rms_plots/"

datafile = datadir+"Raw_snc0_st01_st11.bin"
qc_tools = ana_tools()

with open(datafile, 'rb') as fn:
    raw = pickle.load(fn)

rawdata = raw[0]
pldata = qc_tools.data_decode(rawdata,fembs)
pldata = np.array(pldata)

##### raw waveform
#data_ch = pldata[:,5]
#data_ch = data_ch.reshape(-1)
#plt.plot(range(len(data_ch)),data_ch)
#
##### get fft
nevent = len(pldata)
for i in range(nevent):
    tmpdata1 = pldata[i,nfemb*128+55]
    tmpdata2 = pldata[i,nfemb*128+48]
    tmpdata3 = pldata[i,nfemb*128+25]
    if i==0:
       ch_fft1 = np.abs(np.fft.fft(tmpdata1))
       ch_fft2 = np.abs(np.fft.fft(tmpdata2))
       ch_fft3 = np.abs(np.fft.fft(tmpdata3))
    else:
       ch_fft1 = ch_fft1 + np.abs(np.fft.fft(tmpdata1))
       ch_fft2 = ch_fft2 + np.abs(np.fft.fft(tmpdata2))
       ch_fft3 = ch_fft3 + np.abs(np.fft.fft(tmpdata3))

ch_fft1 = ch_fft1/nevent
ch_fft2 = ch_fft2/nevent
ch_fft3 = ch_fft3/nevent

dt = 0.5e-6 # MHz
freq1 = np.fft.fftfreq(len(tmpdata1), d=dt)
freq2 = np.fft.fftfreq(len(tmpdata2), d=dt)
freq3 = np.fft.fftfreq(len(tmpdata3), d=dt)

n_oneside=len(freq1)//2
f_oneside = freq1[1:n_oneside]
plt.plot(freq1[1:n_oneside], ch_fft1[1:n_oneside],label='ch25, strip 1154')
plt.plot(freq2[1:n_oneside], ch_fft2[1:n_oneside],label='ch54, strip 1153')
plt.plot(freq3[1:n_oneside], ch_fft3[1:n_oneside],label='ch55, strip 1155')
plt.legend()
plt.title("FFT: Magnitude vs. freq (Hz) (900mV, 2us)")
plt.show()

#ch_fft,freq = GetFFT(pldata,48)
#n_oneside=len(freq)//2
#plt.plot(freq[1:n_oneside], ch_fft[1:n_oneside],label='xplane, strip 1')
#plt.legend()
#plt.title("FFT: Magnitude vs. freq (Hz) (900mV, 2us)")
#plt.show()
