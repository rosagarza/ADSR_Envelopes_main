# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 20:01:01 2017

@author: Rosa
"""


import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile
from scipy.io.wavfile import write
import pyaudio
import wave

fs = 44100    # The sampling rate in samples/sec

numberOfSeconds = 6   # The sound will be 6 seconds long
t = np.float32(np.arange(0, numberOfSeconds*fs, dtype=float))/fs

#fc = 440;     # Carrier frequency is a "A 440" note tuned around 440Hz
#fm = 220.5;   # Modulation frequency is 220.5Hz--it is so fast the timbre changes and becomes brighter
#d = 1000;     # The frequency deviation needs to be increased so that the modulation is still audible
# Note: The modulation index I=d/fm

input_fc = input("Enter carrier frequency (Hz): ")
print ("Carrier frequency will be at " + input_fc + "Hz")
input_fc=float(input_fc)

input_fm = input("Enter modulation frequency (Hz): ")
print ("Modulation frequency will be at " + input_fm + "Hz")
input_fm=float(input_fm)


input_d = input("Enter frequency deviation (Hz): ")
print ("Frequency deviation (depth) will be at " + input_d + "Hz")
input_d=float(input_d)


#mySignal = np.sin(2.0*np.pi*t*(fc + d*np.sin(2.0*np.pi*t*fm)))    # This is tempting, but it is wrong ...
#mySignal = np.sin(2.0*np.pi*fc*t - d/fm*np.cos(2.0*np.pi*t*fm))   # This is correct
mySignal = np.sin(2.0*np.pi*input_fc*t + (input_d/input_fm)*np.sin(2.0*np.pi*t*input_fm))    # This sounds almost the same and is a little more convenient


# To actually write it to a wave file, the sound has to be scaled to the
# range -32768 to 32767 and cast to 16-bit integers as so:
scaled = np.int16(mySignal * 32767.0)

#######################################################
############ WRITING THE WAV FILES ###################
#######################################################
######## Fast Sine WAV File ########
userSine=wave.openfp('userInputFM.wav','wb')
userSine.setnframes(fs)
userSine.setsampwidth(2) #amount of bytes, 8bits/byte
userSine.setnchannels(1) #mono-1 stereo-2
userSine.setframerate(fs)
userSine.writeframesraw(scaled)
userSine.close()

################################################
############# PLaying Audio in real time #######
################################################
chunk=1024
userSin_play=wave.open('userInputFM.wav','rb')
p=pyaudio.PyAudio()

stream=p.open(format=p.get_format_from_width(userSin_play.getsampwidth()),channels=userSin_play.getnchannels(),rate=userSin_play.getframerate(),output=True)

data=userSin_play.readframes(chunk)

while data:
    stream.write(data)
    data=userSin_play.readframes(chunk)
stream.stop_stream()
stream.close()

# Plotting is useful unless it is a long sound, then it will take
# too long to display (unless you display only some of the elements ...)
#plt.plot(t[1:2*fs], mySignal[1:2*fs])
#plt.show()
