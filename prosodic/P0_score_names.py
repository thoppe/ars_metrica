import prosodic as p
import pandas as pd
import os
from tqdm import tqdm


year = 2017
f_names = os.path.join('data','social_security_info','yob%s.txt'%year)

df = pd.read_csv(f_names,header=None,names=["name","gender","counts"])
data = []

for name in tqdm(df.name):
    sx = p.Text(name).syllables()

    item = {}
    item["name"] = name
    item["n_syllables"] = len(sx)
    item['IPA'] = ' '.join(map(str, sx))

    if not item["IPA"]:
        continue
    
    item['IPA_stress'] = ''.join(['1' if x[0] in "'`" else '0'
                                for x in item["IPA"].split()])

    print(item)
    data.append(item)
