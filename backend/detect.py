import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import scipy

def detect_gunshots(title):
    
    _, audio = scipy.io.wavfile.read(title + ".wav")

    indices = scipy.signal.find_peaks(audio)[0]

    # print(indices)

    for i in indices:
         if(i > np.mean(audio) + 2 * np.std(audio)):
             return True
    
    return False