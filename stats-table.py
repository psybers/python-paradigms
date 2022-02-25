#!/usr/bin/env python3
# %%
import pandas as pd
import common

# %%
#dfnodupesrq1 = pd.read_parquet('data/parquet/rq1-nodupes.parquet')
#dfnodupesrq2 = pd.read_parquet('data/parquet/rq2-nodupes.parquet')

# %%
#mb = pd.read_csv('data/csv/dataset-stats-main.csv', header=None, index_col=0, names=['var', 'count'])

df = pd.read_csv('data/csv/dataset-stats.csv', header=None, index_col=0, names=['var', 'count'])

#df.loc['a'] = [dfnodupesrq1.shape[0]]
#df.loc['b'] = [mb.loc['FILES']['count']]
#df.loc['c'] = [dfnodupesrq2.shape[0]]

df = df.reindex(['PROJECTS', 'REVS', 'FILES', 'SNAPSHOTS', 'AST'])
#df = df.reindex(['PROJECTS', 'REVS', 'FILES', 'a', 'b', 'SNAPSHOTS', 'c', 'AST'])

rowcolor = 'gray!15'
df = df.rename({
    'PROJECTS': '\\textbf{Projects}',
    'REVS': '\\textbf{Revisions}',
    'FILES': '\\textbf{Python Files}',
#    'a': f'\\rowcolor{{{rowcolor}}}\\textbf{{\\qquad Without Duplicates}}',
#    'b': f'\\rowcolor{{{rowcolor}}}\\textbf{{\\qquad Main Branch Only}}',
    'SNAPSHOTS': '\\textbf{Python File Snapshots}',
#    'c': f'\\rowcolor{{{rowcolor}}}\\textbf{{\\qquad Without Duplicates}}',
    'AST': '\\textbf{ASTs}',
    })
df = df.astype({'count': 'float64'})
common.save_table(df, 'py-dataset', decimals=0, escape=False, dropheader=True)

# %%
