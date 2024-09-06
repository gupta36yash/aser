# 1-  turn the .wav file into suitable format
# 2-  get the model running
# 3-  send audio into the model
# 4-  return output to main.py
from librosa import load
import numpy as np
from librosa.feature import mfcc
from keras import models

def preprocess(filename):
    X, sample_rate = load(filename,duration=3.0,sr=44100,offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
    
    #normalization
    mean = np.mean(mfccs, axis=0)
    std = np.std(mfccs, axis=0)
    mfccs=(mfccs-mean)/std

    return mfccs #returns numpy array of features


def model(arr):
    model = models.load_model('ser.keras')

    ar=np.array([arr])
    
    return (model.predict(ar)*100)

