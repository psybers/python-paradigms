#!/usr/bin/env python3
# %%
import matplotlib.pyplot as plt
import pandas as pd
import common


# %%
categories = common.get_categories()
df = pd.read_csv('data/judgements.csv', header=0, index_col=False)

# %% [markdown]
# # Generate Table(s)

# %%
df2 = df.groupby('Human').size().to_frame('test').rename({'test': ''}, axis=1)
df2 = df2.reindex(categories[1:4])
common.save_table(df2, 'human-judgements', decimals=0)

# %%
df3 = df.groupby('Machine').size().to_frame('test').rename({'test': ''}, axis=1)
df3 = df3.reindex(categories[1:4])
common.save_table(df3, 'machine-judgements', decimals=0)
