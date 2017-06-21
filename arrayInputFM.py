# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 12:03:11 2017

@author: Rosa
"""

import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile
from scipy.io.wavfile import write
import pyaudio
import wave
import random

fs = 44100    # The sampling rate in samples/sec

numberOfSeconds = 6   # The sound will be 6 seconds long
t = np.float32(np.arange(0, numberOfSeconds*fs, dtype=float))/fs

#fc = 440;     # Carrier frequency is a "A 440" note tuned around 440Hz
#fm = 220.5;   # Modulation frequency is 220.5Hz--it is so fast the timbre changes and becomes brighter
#d = 1000;     # The frequency deviation needs to be increased so that the modulation is still audible
# Note: The modulation index I=d/fm

#randoms[0]=fc , randoms[1]=depth (freq. deviation), randoms[2]=fm

randoms=[]
for i in range(3):
    randoms.append(np.random.randint(1,1000))
    print(randoms)

randoms=np.array(randoms)

#mySignal = np.sin(2.0*np.pi*t*(fc + d*np.sin(2.0*np.pi*t*fm)))    # This is tempting, but it is wrong ...
#mySignal = np.sin(2.0*np.pi*fc*t - d/fm*np.cos(2.0*np.pi*t*fm))   # This is correct
mySignal = np.sin(2.0*np.pi*randoms[0]*t + (randoms[1]/randoms[2])*np.sin(2.0*np.pi*t*randoms[2]))    # This sounds almost the same and is a little more convenient


# To actually write it to a wave file, the sound has to be scaled to the
# range -32768 to 32767 and cast to 16-bit integers as so:
scaled = np.int16(mySignal * 32767.0)

#######################################################
############ WRITING THE WAV FILES ###################
#######################################################
######## Fast Sine WAV File ########
arraySine=wave.openfp('arrayInputFM.wav','wb')
arraySine.setnframes(fs)
arraySine.setsampwidth(2) #amount of bytes, 8bits/byte
arraySine.setnchannels(1) #mono-1 stereo-2
arraySine.setframerate(fs)
arraySine.writeframesraw(scaled)
arraySine.close()

################################################
############# PLaying Audio in real time #######
################################################
chunk=1024
arraySin_play=wave.open('arrayInputFM.wav','rb')
p=pyaudio.PyAudio()

stream=p.open(format=p.get_format_from_width(arraySin_play.getsampwidth()),channels=arraySin_play.getnchannels(),rate=arraySin_play.getframerate(),output=True)

data=arraySin_play.readframes(chunk)

while data:
    stream.write(data)
    data=arraySin_play.readframes(chunk)
stream.stop_stream()
stream.close()

# Plotting is useful unless it is a long sound, then it will take
# too long to display (unless you display only some of the elements ...)
#plt.plot(t[1:2*fs], mySignal[1:2*fs])
#plt.show()
