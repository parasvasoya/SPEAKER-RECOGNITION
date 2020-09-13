import os
import pickle
import numpy as np
from scipy.io.wavfile import read
from feature_extraction import  extract_features
import warnings
warnings.filterwarnings("ignore")
import time

source="SampleData/"

modelpath="user_models/"

gmm_files=[os.path.join(modelpath,fname) for fname in os.listdir(modelpath) if fname.endswith('.gmm')]

models=[pickle.load(open(fname,'rb')) for fname in gmm_files]

speakers=[fname.split('/')[-1].split('.gmm')[0] for fname in gmm_files]

error=0
total_sample=0.0

print("do you want to test a single audio : press 1 or complete press 0")
take=int(input().strip())

if take==1:
    print("enter the file name")
    path=input().strip()
    print("testing audio",path)
    sr,audio=read(source+path)
    vector=extract_features(audio,sr)

    log_likelihood=np.zeros(len(models))

    for i in range(len(models)):
        gmm=models[i]
        scores=np.array(gmm.score(vector))
        log_likelihood[i]=scores.sum()

    winner=np.argmax(log_likelihood)
    print("detected as -",speakers[winner])

    time.sleep(1.0)

elif take==0:
    print("we are in 0 part")
