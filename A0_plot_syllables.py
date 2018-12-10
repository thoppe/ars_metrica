import glob, os
import numpy as np
import pandas as pd
import seaborn as sns
import pylab as plt
F_DATA = sorted(glob.glob("data/scored_names/*.csv"))

data = []

for f in F_DATA:
    print(f)
    cols = "counts", "n_syllables", "gender"
    df = pd.read_csv(f,usecols=cols)

    df["counts"] /= df["counts"].sum()
    
    year = int(os.path.basename(f).split('.')[0][3:])
    g = pd.DataFrame(df.groupby("n_syllables")["counts"].sum())
    g['year'] = year

    data.append(g)

key = 'year'
df = pd.concat(data).sort_values(key)#.reset_index().set_index(key)
sz = np.array([16.,9.])/2

'''
plt.figure(figsize=sz)

#totes = np.zeros(size=(df[key].max()-df[key].min()))
totes = pd.Series(index=df[key].unique()).fillna(0.0)
X = totes.index
Y = [dfx.set_index('year').loc[X].values.ravel() for n, dfx in df.groupby("n_syllables")]
plt.stackplot(X,*Y, baseline='zero')
'''


plt.figure(figsize=sz)

g0 = df.reset_index().groupby(['year','n_syllables'])["counts"].sum()
g0 = g0.reset_index()
g0['n_frac'] = g0.n_syllables*g0.counts
mean_syllables = g0.groupby('year')['n_frac'].sum()
plt.plot(mean_syllables, '--', lw=2, color='k')


sns.despine()
plt.title("Average number of syllables from US Soc. Sec. data")
plt.xlabel("Year",fontsize=14)
plt.ylabel("Mean number of syllables", fontsize=14)
plt.xlim(xmax=2018)

plt.tight_layout()
plt.savefig('docs/figures/mean_syllables_per_year.png')


########################################################################

plt.figure(figsize=sz)
for n, dfx in df.groupby("n_syllables"):
    #totes += dfx.set_index('year')['counts']
    plt.plot(dfx.year, dfx['counts'], label=f"{n} syllable(s)")



plt.legend(ncol=2, loc=2, fontsize=12)
sns.despine()
plt.title("Distribution of syllables in US Soc. Sec. data")
plt.xlabel("Year",fontsize=14)
plt.ylabel("Fraction of names\nwith n syllables", fontsize=14)
plt.xlim(xmax=2018)
plt.ylim(0,1)
plt.tight_layout()
plt.savefig('docs/figures/syllables_per_year.png')


plt.show()
