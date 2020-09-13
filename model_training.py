import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import gaussian_mixture
from sklearn import mixture
from feature_extraction import extract_features
#from speakerfeatures import extract_features
import warnings
import os
import librosa
warnings.filterwarnings("ignore")
DATASET_PATH = "DATASET"

fhand=open("user_name.txt",mode='r+')
features = np.asarray(())
dest="user_models/"
name_list=fhand.read()
name_list=name_list.split()
print(name_list)
a="bharat"
count = 1
DATASET_PATH="DATASET/"+a
if a not in name_list:
    print(a)
    fhand.write(a)

    for dirpath,dirnames,filenames in os.walk(DATASET_PATH):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            #read audio file
            sr,audio = read(file_path)
            vector   = extract_features(audio,sr)

            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))

            if count==5:
                gmm = gaussian_mixture.GaussianMixture(n_components = 16,max_iter = 200, covariance_type='diag',n_init = 3)
                gmm.fit(features)

                    # dumping the trained gaussian model
                picklefile = a+".gmm"
                print("model name ",picklefile)
                file=open(dest+picklefile,mode="wb")

                pickle.dump(gmm,file)
                
                print ('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)
                features = np.asarray(())
                count = 0

            count = count + 1

fhand.close()
