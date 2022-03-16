#!/usr/bin/env python3
# %%
import matplotlib.pyplot as plt
import pandas as pd
import common


# %%
# rq1 output format:
#   o[project_url][file_path][commit_hash][commit_date] = { func, oo, proc, imp, stmts }
categories = common.get_categories()
catindexes = common.get_cat_indexes()
catdict = {
    catindexes[0]: categories[0],
    catindexes[1]: categories[1],
    catindexes[2]: categories[2],
    catindexes[3]: categories[3],
    catindexes[4]: 'Mixed'
    }
bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

try:
    dfnodupes = pd.read_parquet('data/parquet/rq1-nodupes.parquet')
except:
    try:
        df = pd.read_parquet('data/parquet/rq1.parquet')
    except:
        df = common.get_data('data/csv/rq1.output.csv', ['var', 'project', 'file', 'revid', 'commitdate', 'classification'], ['var', 'revid', 'commitdate'], common.get_counts())
        df = common.filter_projects(df)
        df.to_parquet('data/parquet/rq1.parquet', compression='gzip')

    dfnodupes = common.remove_dupes(df)
    dfnodupes = common.split_categories(dfnodupes, categories)

    dfnodupes['classified'] = dfnodupes.apply(common.classify_file, axis=1)
    dfnodupes.to_parquet('data/parquet/rq1-nodupes.parquet', compression='gzip')


# %% [markdown]
# # Generate Chart(s)

# %%
stmtcounts = dfnodupes['stmts_count'].quantile(bins)

mydf_stmts = dfnodupes[['stmts_count', 'classified']]
mydf_stmts = mydf_stmts.groupby(['classified', pd.cut(mydf_stmts.stmts_count, [stmtcounts[x] for x in bins])])
mydf_stmts = mydf_stmts.size().unstack()

# %%
mydf1 = mydf_stmts.iloc[1:]
mydf1 = mydf1.reindex(catindexes[1:])
mydf1 = mydf1.rename(catdict)
subplot = mydf1.plot.bar(figsize=(8,4), logy=False,rot=0,xlabel='',legend=False)
subplot.grid(axis='y')
subplot.set_axisbelow(True)
from matplotlib.ticker import FuncFormatter
subplot.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
plt.ylabel('Files')
plt.savefig('figures/' + 'rq3-hist.pdf', dpi=1200, bbox_inches='tight')
plt.close()

# %%
mydf2 = mydf_stmts.iloc[0:1]
mydf2 = mydf2.rename(catdict)
subplot = mydf2.plot.bar(figsize=(4,4), logy=False,rot=0,xlabel='',legend=False)
subplot.grid(axis='y')
subplot.set_axisbelow(True)
plt.ylabel('Files')
plt.savefig('figures/' + 'rq3-hist-func.pdf', dpi=1200, bbox_inches='tight')
plt.close()


# %%
pplcounts = dfnodupes['ppl_count'].quantile(bins)

mydf_ppl = dfnodupes[['ppl_count', 'classified']]
mydf_ppl = mydf_ppl.groupby(['classified', pd.cut(mydf_ppl.ppl_count, [pplcounts[x] for x in bins], duplicates='drop')])
mydf_ppl = mydf_ppl.size().unstack()

# %%
mydf3 = mydf_ppl
mydf3 = mydf3.reindex(catindexes)
mydf3 = mydf3.rename(catdict)
subplot = mydf3.plot.bar(figsize=(8,4), logy=False,rot=0,xlabel='',legend=True)
subplot.grid(axis='y')
subplot.set_axisbelow(True)
from matplotlib.ticker import FuncFormatter
subplot.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
plt.ylabel('Files')
plt.savefig('figures/' + 'rq3-ppl-hist.pdf', dpi=1200, bbox_inches='tight')
plt.close()


# %%
revscounts = dfnodupes['revs_count'].quantile(bins)

mydf_revs = dfnodupes[['revs_count', 'classified']]
mydf_revs = mydf_revs.groupby(['classified', pd.cut(mydf_revs.revs_count, [revscounts[x] for x in bins], duplicates='drop')])
mydf_revs = mydf_revs.size().unstack()

# %%
mydf4 = mydf_revs
mydf4 = mydf4.reindex(catindexes)
mydf4 = mydf4.rename(catdict)
subplot = mydf4.plot.bar(figsize=(8,4), logy=False,rot=0,xlabel='',legend=False)
subplot.grid(axis='y')
subplot.set_axisbelow(True)
from matplotlib.ticker import FuncFormatter
subplot.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
plt.ylabel('Files')
plt.savefig('figures/' + 'rq3-revs-hist.pdf', dpi=1200, bbox_inches='tight')
plt.close()
