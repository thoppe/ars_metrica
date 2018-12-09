import prosodic as p
import pandas as pd
from tqdm import tqdm

df = pd.read_csv(
    "genderizer_collected.csv",
    encoding='utf-8',
    nrows=12000)

print len(df)

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
    
    data.append(item)


data = pd.DataFrame(data).set_index('name')
df = df.set_index('name')

for col in data.columns:
    df[col] = data[col]

print df

df.to_csv("stressed_names.csv",encoding='utf-8')

    


