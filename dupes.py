# %%
import pandas as pd
import common

# %%
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

try:
    dfnodupes = pd.read_parquet('data/parquet/rq4-nodupes.parquet')
except:
    categories = common.get_categories()
    dfnodupes = common.remove_dupes(df)
    dfnodupes = common.split_categories(dfnodupes, categories)
    dfnodupes['classified'] = dfnodupes.apply(common.classify_file, axis=1)

    dfnodupes.to_parquet('data/parquet/rq4-nodupes.parquet', compression='gzip')

# %%
allfiles = len(df.groupby(['project', 'file']))
nodupes = len(dfnodupes.groupby(['project', 'file']))

removed = allfiles - nodupes
print('dupe files removed', removed)

pct = round(removed / allfiles * 100, 2)
print('dupe files pct', pct)
