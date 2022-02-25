#!/usr/bin/env python3
# %%
import matplotlib.pyplot as plt
import pandas as pd
import common


# %%
# rq2 output format:
#   o[project_url][file_path][feature_name] = feature_count
try:
    df = pd.read_parquet('data/parquet/rq2.parquet')
except:
    df = common.get_data('data/csv/rq2.output.csv', ['var', 'project', 'file', 'feature', 'counts'], ['var'], common.get_counts())
    df = common.filter_projects(df)
    df.to_parquet('data/parquet/rq2.parquet', compression='gzip')

try:
    dfnodupes = pd.read_parquet('data/parquet/rq2-nodupes.parquet')
except:
    dfnodupes = common.remove_dupes(df)
    dfnodupes.to_parquet('data/parquet/rq2-nodupes.parquet', compression='gzip')


# %% [markdown]
# # Generate Table(s)

# %%
df2 = dfnodupes.groupby('feature').size()
df2.loc['Library functions'] = 0
for x in [x for x in df2.index if 'func-' in x]:
    df2.loc['Library functions'] = df2.loc['Library functions'] + df2.loc[x]
    df2 = df2.drop(x)
df2 = df2.sort_values(ascending=False).to_frame('count')

rowcolor = 'gray!15'
df2 = df2.rename({
    'method': f'\rowcolor{{{rowcolor}}} method declarations',
    'FOREACH': 'for-each',
    'RAISE': f'\rowcolor{{{rowcolor}}} \texttt{{raise}}',
    'TRY': f'\rowcolor{{{rowcolor}}} \texttt{{try}}',
    'CATCH': f'\rowcolor{{{rowcolor}}} \texttt{{except}}',
    'IN': '\texttt{in}',
    'ARRAY_COMPREHENSION': 'array comprehensions',
    'NOT_IN': '\texttt{not in}',
    'WITH': f'\rowcolor{{{rowcolor}}} \texttt{{with}}',
    'LAMBDA': '\texttt{lambda}',
    'YIELD': '\texttt{yield}',
    'FINALLY': f'\rowcolor{{{rowcolor}}} \texttt{{finally}}',
    'method-decorator': 'method decorators',
    'class-decorator': 'class decorators',
    'class': f'\rowcolor{{{rowcolor}}} class declarations',
    'inherits': f'\rowcolor{{{rowcolor}}} class inheritance',
    'higher-order-func': 'higher-order functions',
    'GENERATOR': 'generators',
    'iterable': 'iterable',
    'Library functions': 'built-in functions (functools/itertools)',
    })
df2 = df2.astype({'count': 'float64'})
common.save_table(df2, 'rq2-project', decimals=0, escape=False)
