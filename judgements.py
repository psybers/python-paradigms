#!/usr/bin/env python3
# %%
import matplotlib.pyplot as plt
import pandas as pd
import common


# %% [markdown]
# # Generate Table(s)

# %%
df = pd.read_csv('data/judgements.csv',
                 header=0,
                 index_col=False,
                 usecols=['Human', 'Machine'])

df2 = pd.DataFrame({'Human Judgements': df.groupby(['Human']).size(),
                   'Machine Judgements': df.groupby(['Machine']).size()})

common.save_table(df2, 'judgements', decimals=0)
