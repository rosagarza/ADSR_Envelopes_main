# * Creating audio of ADSR envelope*-
"""
Created on Thu May 25 20:26:43 2017

@author: Rosa Garza
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

# want to adjust modulation index
#The modulation index I=d/fm
# hold harmonicity constant (fc:fm)
#may mean depth is what is changing in order to hold harm. constant
# hold carrier freq. constant (fc)
# basically depth is changing

##NOTE: #samples per second are the "dots" in a line
#########frequency is how many periods per sec.

samplesPerSec = 44100
numOfSecs =10
maxInt=32767.0 #Max number of 16 bits

totalSamp=samplesPerSec*numOfSecs

t = np.float32(np.arange(0, totalSamp, dtype=float))/samplesPerSec

fc=440
fm=1
d=np.random.randint(1,1000)

################### ADSR Portion ############################
t4=np.round(np.random.uniform(low=0.0,high=totalSamp,size=None)) #a random time for release
t3=np.round(np.random.uniform(low=0.0,high=t4,size=None))
t2=np.round(np.random.uniform(low=0.0,high=t3,size=None))
t1=np.round(np.random.uniform(low=0.0,high=t2,size=None))

y1=1
y2=(np.random.random_sample(size=[1]))

attack_interval=np.linspace(0, y1, num=t1, endpoint=True, retstep=False, dtype=float)
decay_interval=np.linspace(y1,y2,num=(t2-t1),endpoint=True, retstep=False, dtype=float)
sustain_interval=np.linspace(y2,y2,num=(t3-t2),endpoint=True, retstep=False, dtype=float)
release_interval=np.linspace(y2,0,num=(t4-t3),endpoint=True, retstep=False, dtype=float)
remainder_interval=np.linspace(0,0,num=(totalSamp-t4),endpoint=True, retstep=False, dtype=float)

ADSR_interval=np.concatenate([attack_interval,decay_interval])
ADSR_interval=np.concatenate([ADSR_interval,sustain_interval])
ADSR_interval=np.concatenate([ADSR_interval,release_interval])
ADSR_interval=np.concatenate([ADSR_interval,remainder_interval])

#myADSR_Signal=ADSR_interval*np.sin(2*pi*freq*t)
#mySignal = np.sin(2.0*np.pi*t*(fc + d*np.sin(2.0*np.pi*t*fm)))    # This is tempting, but it is wrong ...
#mySignal = np.sin(2.0*np.pi*fc*t - d/fm*np.cos(2.0*np.pi*t*fm))   # This is correct
adjustedADSR_Signal = ADSR_interval*np.sin(2.0*np.pi*fc*t + (d/fm)*np.sin(2.0*np.pi*t*fm))    # This sounds almost the same and is a little more convenient



######### PLOTTING ######################
# Plotting is useful unless it is a long sound, then it will take
# too long to display (unless you display only some of the elements ...)
#If a plot shows up solid color, do (t[:100], (variable)[:100]) to see values better

## DISABLED PLOTTING TO SPEED UP PROGRAM ##########                                    
plt.plot(t,adjustedADSR_Signal)
plt.show()

########## SCALING TO WRITE WAV FILES #######################
# range -32768 to 32767 and cast to 16-bit integers as so:
adsr_scaled=np.int16(adjustedADSR_Signal*maxInt)

#######################################################
############ WRITING THE WAV FILES ###################
#######################################################
######## ADSR ENVELOPE ########
adsr=wave.openfp('adjustedADSR.wav','wb')
adsr.setnframes(samplesPerSec)
adsr.setsampwidth(2) #amount of bytes, 8bits/byte
adsr.setnchannels(1) #mono-1 stereo-2
adsr.setframerate(samplesPerSec)
adsr_data= adsr_scaled
adsr.writeframesraw(adsr_data)
adsr.close()

################################################
############# PLaying Audio in real time #######
################################################
chunk=1024
adsr_play=wave.open('adjustedADSR.wav','rb')
p=pyaudio.PyAudio()

stream=p.open(format=p.get_format_from_width(adsr_play.getsampwidth()),channels=adsr_play.getnchannels(),rate=adsr_play.getframerate(),output=True)

data=adsr_play.readframes(chunk)

while data:
    stream.write(data)
    data=adsr_play.readframes(chunk)
stream.stop_stream()
stream.close()
