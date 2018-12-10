import glob, os
import numpy as np
import pandas as pd
import seaborn as sns
import pylab as plt
F_DATA = glob.glob("data/scored_names/*.csv")


data = []
for f in F_DATA:
    print(f)
    cols = "counts", "n_syllables"
    df = pd.read_csv(f,usecols=cols)


    df["counts"] /= df["counts"].sum()
    
    year = int(os.path.basename(f).split('.')[0][3:])
    g = pd.DataFrame(df.groupby("n_syllables")["counts"].sum())
    g['year'] = year 

    data.append(g)

key = 'year'
df = pd.concat(data).sort_values(key)#.reset_index().set_index(key)

sz = np.array([16.,9.])/2
plt.figure(figsize=sz)

#totes = np.zeros(size=(df[key].max()-df[key].min()))
totes = pd.Series(index=df[key].unique()).fillna(0.0)

X = totes.index
Y = [dfx.set_index('year').loc[X].values.ravel() for n, dfx in df.groupby("n_syllables")]
plt.stackplot(X,*Y, baseline='zero')
#plt.show()
#exit()
plt.figure(figsize=sz)

for n, dfx in df.groupby("n_syllables"):
    
    totes += dfx.set_index('year')['counts']
    plt.plot(dfx.year, dfx['counts'], label=f"{n} syllables")
    
    print(totes)

plt.legend(ncol=2)
sns.despine()
plt.xlabel("Year")
plt.ylabel("Fraction of names with this many syllables")
plt.tight_layout()

plt.show()
