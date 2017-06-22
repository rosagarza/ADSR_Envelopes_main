# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:43:28 2017

@author: Rosa
"""

import numpy as np
from numpy import pi
import math,struct
import scipy.io.wavfile
from scipy.io.wavfile import write
from matplotlib import pyplot as plt
import pyaudio
import wave
import random
import os

# Adjusted modulation index I=d/fm
# Harmonicity constant (fc:fm)
# Carrier freq. constant (fc)

##NOTE: #samples per second are the "dots" in a line
#########frequency is how many periods per sec.

samplesPerSec = 44100
numOfSecs =10
maxInt=32767.0 #Max number of 16 bits

totalSamp=samplesPerSec*numOfSecs

t = np.float32(np.arange(0, totalSamp, dtype=float))/samplesPerSec

fc=440
fm=1
y1=1
y2=(np.random.random_sample(size=[1]))

## function to get attack, decay, sustain, and release points
def adsrPoints(low=0.0,high=totalSamp,size=None):
    a=np.round(np.random.uniform(low,high,size))
    return a

## function to get attack,decay,sustain, and release intervals
def adsrIntervals(l,h,num,endpoint=True,retstep=False,dtype=float):
    i=np.linspace(l, h, num, endpoint, retstep, dtype)
    return i

def genRandomADSR(total_sample):
    t4=adsrPoints(high=totalSamp) #to get ADSR points
    t3=adsrPoints(high=t4)
    t2=adsrPoints(high=t3)
    t1=adsrPoints(high=t2)
    
    attack_interval=adsrIntervals(l=0,h=y1,num=t1) #to get ADSR intervals
    decay_interval=adsrIntervals(l=y1,h=y2,num=(t2-t1))
    sustain_interval=adsrIntervals(l=y2,h=y2,num=(t3-t2))
    release_interval=adsrIntervals(l=y2,h=0,num=(t4-t3))
    remainder_interval=adsrIntervals(l=0,h=0,num=(totalSamp-t4))
    
    ADSR_interval=np.concatenate([attack_interval,decay_interval]) #combining intervals
    ADSR_interval=np.concatenate([ADSR_interval,sustain_interval])
    ADSR_interval=np.concatenate([ADSR_interval,release_interval])
    ADSR_interval=np.concatenate([ADSR_interval,remainder_interval])
    return ADSR_interval

def write_audio(fn_str,scale):
    adsr=wave.openfp(fn_str,'wb')
    adsr.setnframes(samplesPerSec)
    adsr.setsampwidth(2) #amount of bytes, 8bits/byte
    adsr.setnchannels(1) #mono-1 stereo-2
    adsr.setframerate(samplesPerSec)
    adsr.writeframesraw(scale)
    adsr.close()
    return

def play_audio(fn):
    ############# PLaying Audio in real time #######
    chunk=1024
    adsr_play=wave.open(fn,'rb')
    p=pyaudio.PyAudio()
    stream=p.open(format=p.get_format_from_width(adsr_play.getsampwidth()),channels=adsr_play.getnchannels(),rate=adsr_play.getframerate(),output=True)
    data=adsr_play.readframes(chunk)
    while data:
        stream.write(data)
        data=adsr_play.readframes(chunk)
    stream.stop_stream()
    stream.close()
    return

# Asks user to name file, and makes a folder
cd=os.getcwd()
input_filename = input("Enter filename for audio: ")
print ("File will be under " + input_filename )
dir=cd+"\\"+input_filename
os.mkdir(dir)

# Asks user for number of audio to generate
num_audio = input("Enter number of audio to generate: ")
print ( input_filename +" ADSR wav files will be generated." )
num_audio=int(num_audio)

for i in range(num_audio):
    myAmpEnv=genRandomADSR(totalSamp)
    d=np.random.randint(1,1000)
    myADSR_Signal=myAmpEnv*np.sin(2.0*np.pi*fc*t + (d/fm)*np.sin(2.0*np.pi*t*fm))
    #freqDev=d*genRandomADSR(totalSamp)
    #secondADSR_Signal =freqDev*np.sin(2.0*np.pi*fc*t + (d/fm)*np.sin(2.0*np.pi*t*fm))
    plt.plot(t,myADSR_Signal)
    plt.show()
    #plt.plot(t,secondADSR_signal)
    #plt.show()
    
    ########## SCALING TO WRITE WAV FILES #######################
    # range -32768 to 32767 and cast to 16-bit integers as so:
    ADSR_scaled=np.int16(myADSR_Signal*maxInt)
    #ADSR2_scaled=np.int16(secondADSR_Signal*maxInt)
    
    ############ WRITING THE WAV FILES ###################
    ######## ADSR ENVELOPE ########
    i_str=str(i)
    filename=dir+'\\testADSR_'+i_str+'.wav'
    write_audio(fn_str=filename,scale=ADSR_scaled)
    play_audio(fn=filename)
    #filename_2=dir+'\\testADSR_2_'+i_str+'.wav'
    #write_audio(fn_str=filename_2,scale=ADSR2_scaled)
    #play_audio(fn=filename_2)