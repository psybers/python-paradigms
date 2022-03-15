#!/usr/bin/env python3
# %%
import pandas as pd
import common

# %%
categories = common.get_categories()

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

df2 = dfnodupes.drop(['OO', 'Procedural', 'Imperative', 'Statements', 'Functional', 'pct_func', 'pct_oo', 'pct_proc', 'pct_imp', 'classified', 'file', 'commitdate', 'ppl_count'], axis=1)
df3 = df2.groupby(['project']).first()

counts = df3.describe().apply(lambda s: s.apply('{0:.2f}'.format))
common.save_table(counts, 'counts-dist', decimals=2, escape=True)

# %%
projs = len(dfnodupes.project.unique())
revs = len(dfnodupes.commitdate.unique())
files = len(dfnodupes.groupby(['project', 'file']).first())
snapshots = len(dfnodupes)
asts = dfnodupes.groupby(['project']).first()['ast_count'].sum()

df = pd.DataFrame(data=[projs, revs, files, snapshots, asts], index=['\\textbf{Projects}',
                   '\\textbf{Revisions}',
                   '\\textbf{Python Files}',
                   '\\textbf{Python File Snapshots}',
                   '\\textbf{ASTs}'])
# df = df.astype({'count': 'float64'})

common.save_table(df, 'py-dataset', decimals=0, escape=False, dropheader=True)
