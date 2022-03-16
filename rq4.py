#!/usr/bin/env python3
# %%
import matplotlib.pyplot as plt
import pandas as pd
import common


# %%
# rq4 output format:
#   o[project_url][file_path][commit_hash][commit_date] = { func, oo, proc, imp, stmts }
categories = common.get_categories()
catindexes = common.get_cat_indexes()
catindexes2 = [
    ['func', 'func', 'func', 'func',
    'oo', 'oo', 'oo', 'oo',
    'proc', 'proc', 'proc', 'proc',
    'imp', 'imp', 'imp', 'imp',
    'mixed', 'mixed', 'mixed', 'mixed'],
    ['oo', 'proc', 'imp', 'mixed',
    'func', 'proc', 'imp', 'mixed',
    'func', 'oo', 'imp', 'mixed',
    'func', 'oo', 'proc', 'mixed',
    'func', 'oo', 'proc', 'imp']
]
catdict = {
    catindexes[0]: categories[0],
    catindexes[1]: categories[1],
    catindexes[2]: categories[2],
    catindexes[3]: categories[3],
    catindexes[4]: 'Mixed'
    }

try:
    dfchanged = pd.read_parquet('data/parquet/rq4-changed.parquet')
except:
    try:
        dfnodupes = pd.read_parquet('data/parquet/rq4-nodupes.parquet')
    except:
        try:
            df = pd.read_parquet('data/parquet/rq4.parquet')
        except:
            df = common.get_data(
                'data/csv/rq4.output.csv',
                ['var', 'project', 'file', 'revid', 'commitdate', 'classification'],
                ['var', 'revid'],
                common.get_counts())
            df = common.filter_projects(df)

            df.to_parquet('data/parquet/rq4.parquet', compression='gzip')

        dfnodupes = common.remove_dupes(df)
        dfnodupes = common.split_categories(dfnodupes, categories)
        dfnodupes['classified'] = dfnodupes.apply(common.classify_file, axis=1)

        dfnodupes.to_parquet('data/parquet/rq4-nodupes.parquet', compression='gzip')

    dfchanged = dfnodupes[dfnodupes.duplicated(subset=['project', 'file'], keep=False)]

    dfchanged.to_parquet('data/parquet/rq4-changed.parquet', compression='gzip')


# %% [markdown]
# # Generate Table(s)

# %%
try:
    evolution = pd.read_parquet('data/parquet/rq4-evolution.parquet')
except:
    data = []
    firstgrp = []
    lastgrp = []

    evolution = dfchanged.groupby(['project', 'file'])
    for key, item in evolution:
        last = None
        for i in range(len(item.index)):
            cur = item.at[item.index[i], 'classified']
            if last:
                data.append(cur != last)
                firstgrp.append(last)
                lastgrp.append(cur)
            last = cur

    evolution = pd.DataFrame({'changed?': data, 'first': firstgrp, 'last': lastgrp})
    evolution.to_parquet('data/parquet/rq4-evolution.parquet', compression='gzip')

# %%
evogroups = evolution[['changed?']]
evogroups = evogroups.groupby('changed?').size().astype('float64')
common.save_table(evogroups.to_frame('files'), 'rq4-evolution', decimals=0, escape=False)

# %%
changegrps = evolution[['first', 'last']]
changegrps = changegrps.groupby(['first', 'last']).size().astype('float64')
changegrps = changegrps.reindex(catindexes2)
changegrps = changegrps.rename(catdict)
common.save_table(changegrps.to_frame('files'), 'rq4-changed', decimals=0, escape=False)

# %%
common.save_table(changegrps.groupby('first').sum().to_frame('files'), 'rq4-first', decimals=0, escape=False)
common.save_table(changegrps.groupby('last').sum().to_frame('files'), 'rq4-last', decimals=0, escape=False)
