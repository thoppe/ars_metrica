import glob, os
import numpy as np
import pandas as pd
import seaborn as sns
import pylab as plt
F_DATA = sorted(glob.glob("data/scored_names/*.csv"))[::-1]#[:20]


fixed_n_syllables = 2

named_patterns = {
    "00": "pyrrhic",
    "01": "iambic",
    "10": "trochee",
    "11": "spondee",
    "000": "tribrach",
    "100": "dactyl",
    "010": "amphibrach",
    "001": "anapaest",
    "011": "bacchius",
    "110": "antibacchius",
    "101": "cretic",
    "111": "molossus",
    "0010": "terius paeon",
    "0100": "secundus paeon",
    "1010": "ditrochee",
    "1100": "major ionic",
}


data = []
for f in F_DATA:
    print(f)
    cols = "counts", "IPA_stress", "n_syllables"
    df = pd.read_csv(f,usecols=cols,dtype={"IPA_stress":str})

    df = df[df['n_syllables']==fixed_n_syllables]

    # Drop names without any stress
    idx = df.IPA_stress.str.count("0") == df.n_syllables
    df = df[~idx]

    df["counts"] /= df["counts"].sum()
    
    year = int(os.path.basename(f).split('.')[0][3:])
    g = pd.DataFrame(df.groupby("IPA_stress")["counts"].sum())
    g['year'] = year

    data.append(g)

key = 'year'
df = pd.concat(data).sort_values(key)#.reset_index().set_index(key)
sz = np.array([16.,9.])/2

# Low counts
mean_value = df.groupby(df.index)['counts'].mean()

df = df.loc[mean_value > 0.01]
mean_value = df.groupby(df.index)['counts'].mean().sort_values()[::-1]


########################################################################

fig, ax = plt.subplots(1,1,figsize=sz)

P = {}
for key, dfx in df.groupby("IPA_stress"):
    #if key in named_patterns:
    #    label = f"{key}, {named_patterns[key]}"
    #else:
    #    label = f"{key}"
    
    P[key] = plt.plot(dfx.year, dfx['counts'], label=key)

handles, labels = ax.get_legend_handles_labels()
idx = mean_value.loc[labels].argsort()[::-1]
labels = np.array(labels)[idx]
handles = np.array(handles)[idx]

labels = [x if x not in named_patterns else
           f"{x}, {named_patterns[x]}" for x in labels]

plt.legend(handles, labels, ncol=2, loc='best', fontsize=12)

sns.despine()
plt.title(f"Stress in {fixed_n_syllables}-syllable names from US Soc. Sec. data")
plt.xlabel("Year",fontsize=14)
plt.ylabel("Fraction of names", fontsize=14)

plt.xlim(xmax=2018)
plt.ylim(0,1)
plt.tight_layout()
plt.savefig(f'docs/figures/{fixed_n_syllables}_stress_patterns_per_year.png')


plt.show()
