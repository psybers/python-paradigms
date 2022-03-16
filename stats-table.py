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

counts = df3.describe().drop('count').astype('float64')#apply(lambda s: s.apply('{:,.2f}'.format))
counts = counts[['revs_count', 'files_count', 'stmts_count', 'ast_count']]
counts = counts.rename(columns={'revs_count': 'Revisions', 'files_count': 'Python Files', 'stmts_count': 'Statements', 'ast_count': 'ASTs'})

common.save_table(counts, 'counts-dist', decimals=0, escape=True)#, column_format='lrrrr')

# %%
try:
    rq1nodupes = pd.read_parquet('data/parquet/rq1-nodupes.parquet')
except:
    try:
        df = pd.read_parquet('data/parquet/rq1.parquet')
    except:
        df = common.get_data('data/csv/rq1.output.csv', ['var', 'project', 'file', 'revid', 'commitdate', 'classification'], ['var', 'revid', 'commitdate'], common.get_counts())
        df = common.filter_projects(df)
        df.to_parquet('data/parquet/rq1.parquet', compression='gzip')

    rq1nodupes = common.remove_dupes(df)
    rq1nodupes = common.split_categories(rq1nodupes, categories)

    rq1nodupes['classified'] = rq1nodupes.apply(common.classify_file, axis=1)
    rq1nodupes.to_parquet('data/parquet/rq1-nodupes.parquet', compression='gzip')

firsts = dfnodupes.groupby(['project']).first()

projs = len(dfnodupes.project.unique())
allrevs = firsts['revs_count'].sum()
revs = len(dfnodupes.commitdate.unique())
files = len(dfnodupes.groupby(['project', 'file']).first())
filesmain = len(rq1nodupes)
snapshots = len(dfnodupes)
asts = firsts['ast_count'].sum()

df = pd.DataFrame(data=[projs, allrevs, revs, files, filesmain, snapshots, asts], index=['\\textbf{Projects}',
                   '\\textbf{All Revisions}',
                   '\\textbf{Revisions (with a Python file)}',
                   '\\textbf{Python Files}',
                   '\\rowcolor{gray!15}\\qquad\\textbf{Python Files (main branch)}',
                   '\\textbf{Python File Snapshots}',
                   '\\textbf{ASTs}'])

common.save_table(df, 'py-dataset', decimals=0, escape=False, dropheader=True)
