import glob, os
import numpy as np
import pandas as pd
import seaborn as sns
import pylab as plt


data = []
f = 'data/scored_names/yob2017.csv'
cols = "name", "counts", "IPA_stress", "n_syllables"
df = pd.read_csv(f,usecols=cols,dtype={"IPA_stress":str})
df = df[df['counts']>200]

N = 10

X = df[df.IPA_stress=='01']
total = float(X["counts"].sum())
W0 = np.random.choice(X.name, size=N*2, replace=False, p=X.counts/total)

X = df[df.IPA_stress=='10']
total = float(X["counts"].sum())
W1 = np.random.choice(X.name, size=N, replace=False, p=X.counts/total)

X = df[df.IPA_stress=='010']
total = float(X["counts"].sum())
W2 = np.random.choice(X.name, size=N, replace=False, p=X.counts/total)

X = df[df.IPA_stress=='101']
total = float(X["counts"].sum())
W3 = np.random.choice(X.name, size=N, replace=False, p=X.counts/total)


for n in range(N):
    print("%s %s %s-%s"%(W0[n], W0[n+N], W2[n], W3[n]))








