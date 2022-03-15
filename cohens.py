#!/usr/bin/env python3
# %%
import pandas as pd
import common

categories = common.get_categories()[0:4]
cats = {}
for i in range(len(categories)):
    cats[categories[i]] = i + 1
cats['Mixed'] = len(categories) + 1

df = pd.read_csv('data/judgements.csv',
                 header=0,
                 usecols=['Human', 'Machine'],
                 index_col=False)
df.Human = df.Human.map(lambda x: cats[x])
df.Machine = df.Machine.map(lambda x: cats[x])

from sklearn.metrics import cohen_kappa_score
cohen_kappa_score(df.Human.tolist(), df.Machine.tolist())
