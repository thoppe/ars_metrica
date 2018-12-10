import glob, os
import numpy as np
import pandas as pd
import seaborn as sns
import pylab as plt
from tqdm import tqdm
F_DATA = sorted(glob.glob("data/scored_names/*.csv"))[::-1]#[:20]


save_dest = 'data/top_names'
os.system(f"mkdir -p {save_dest}")

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
for f in tqdm(F_DATA):

    cols = "counts", "IPA_stress", "n_syllables", "name", "gender"
    df = pd.read_csv(f,usecols=cols,dtype={"IPA_stress":str})
    df = df[df['n_syllables']==fixed_n_syllables]
 
    # Drop names without any stress
    idx = df.IPA_stress.str.count("0") == df.n_syllables
    df = df[~idx]
    df = df[df['counts']>100]
    
    data.append(df)


df = pd.concat(data).groupby(["name","gender", "IPA_stress"])['counts'].sum().reset_index()

data = []
for pattern, dfx in df.groupby(["IPA_stress","gender"]):
    dfx = dfx.sort_values("counts", ascending=False)
    data.append(dfx[:10])


df = pd.concat(data)
df['IPA_stress'] = df['IPA_stress'].astype(str)
df = df.set_index(["IPA_stress", "gender"])

df.to_csv(os.path.join(save_dest, f"top_names_{fixed_n_syllables}_syllables.csv"),
          quoting=2,)

print(df)
