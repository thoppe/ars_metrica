import prosodic as p
import pandas as pd
import os
from tqdm import tqdm


year = 2017


save_dest = os.path.join('..', 'data','scored_names')
os.system('mkdir -p {}'.format(save_dest))


def compute(year):
    f_names = os.path.join('..', 'data','social_security_info','yob%s.txt'%year)
    f_save = os.path.join(save_dest, 'yob%s.csv'%year)

    if os.path.exists(f_save):
        print("Already completed", year)
        return False


    df = pd.read_csv(
        f_names,header=None,names=["name","gender","counts"],
        encoding='utf-8'
    )

    data = []

    #df = df[:5]

    for _, row in tqdm(df.iterrows()):
        name = row["name"]

        sx = p.Text(name).syllables()

        item = {}
        item["name"] = name
        item["gender"] = row["gender"]
        item["counts"] = row["counts"]
        item["n_syllables"] = len(sx)
        item['IPA'] = ' '.join(map(str, sx))

        if not item["IPA"]:
            continue

        item['IPA_stress'] = ''.join(['1' if x[0] in "'`" else '0'
                                    for x in item["IPA"].split()])

        #print(item)
        data.append(item)

    df = pd.DataFrame(data).set_index(["name", "gender"])
    df = df.sort_values("counts", ascending=False)
    df.to_csv(f_save, encoding='utf-8')
    print(df)
    print(f_save)

ITR = range(2017, 1879, -1)

import joblib
func = joblib.delayed(compute)
with joblib.Parallel(-1,batch_size=1) as MP:
    MP(func(x) for x in ITR)

