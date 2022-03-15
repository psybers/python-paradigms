#!/usr/bin/env python3
# %%
import matplotlib.pyplot as plt
import pandas as pd
import common


# %%
# rq1 output format:
#   o[project_url][file_path][commit_hash][commit_date] = { func, oo, proc, imp, stmts }
categories = common.get_categories()
catindexes = ['func', 'oo', 'proc', 'imp', 'mixed']

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
subplot = dfnodupes.boxplot(boxprops={'facecolor': 'white', 'color': 'black'}, patch_artist=True, column=[categories[-1]] + categories[0:-1], showfliers=False)
subplot.grid(axis='x')
subplot.set_axisbelow(True)
plt.axvline(x=1.5)
plt.ylabel('Statements (per file)')
plt.savefig('figures/' + 'rq1-statement-dist.pdf', dpi=1200, bbox_inches='tight')
plt.show()

# %%
from matplotlib.ticker import PercentFormatter
subplot = dfnodupes.boxplot(boxprops={'facecolor': 'white', 'color': 'black'}, patch_artist=True, column=['pct_func', 'pct_oo', 'pct_proc', 'pct_imp'], showfliers=False)
subplot.grid(axis='x')
subplot.set_axisbelow(True)
subplot.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
subplot.set_xticklabels(labels=categories[0:-1])
plt.ylabel('File Statements (%)')
plt.savefig('figures/' + 'rq1-statement-pct.pdf', dpi=1200, bbox_inches='tight')
plt.show()

# %%
filecounts = dfnodupes.groupby('classified').size()
filecounts = filecounts.reindex(catindexes)
subplot = filecounts.plot.bar(rot=0)
subplot.set_xticklabels(labels=categories[0:-1] + ['Mixed'])
subplot.grid(axis='y')
subplot.set_axisbelow(True)
subplot.bar_label(subplot.containers[0], fmt='%d')
from matplotlib.ticker import FuncFormatter
subplot.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
plt.xlabel(None)
plt.ylabel('Files')
plt.savefig('figures/' + 'rq1-file-totals.pdf', dpi=1200, bbox_inches='tight')
plt.show()


# %% [markdown]
# # Generate Table(s)

# %%
dftab1 = dfnodupes[[categories[-1]] + categories[0:-1]].describe()
dftab1 = dftab1.drop(index='count')
common.save_table(dftab1, 'rq1-statement-dist')


# %%
projsum = dfnodupes.groupby(['project']).sum()
projsum = common.compute_pcts(projsum, categories)
projsum['classified'] = projsum.apply(common.classify_project, axis=1)
projsum = projsum.groupby('classified').size()
projsum = projsum.reindex(catindexes)
projsum = projsum.rename({'func': f'\textbf{{{categories[0]}}}', 'oo': f'\textbf{{{categories[1]}}}', 'proc': f'\textbf{{{categories[2]}}}', 'imp': f'\textbf{{{categories[3]}}}', 'mixed': '\textbf{Mixed}'})
projsum = projsum.astype('float64')
common.save_table(projsum.to_frame('all projects'), 'rq1-projects', decimals=0, escape=False)


# %%
projsum2 = dfnodupes
projsum2 = projsum2.loc[projsum2['revs_count'] >= 10]

projsum2 = projsum2.groupby(['project']).sum()
projsum2 = common.compute_pcts(projsum2, categories)
projsum2['classified'] = projsum2.apply(common.classify_project, axis=1)
projsum2 = projsum2.groupby('classified').size()
for k in catindexes:
    if k not in projsum2: projsum2[k] = 0
projsum2 = projsum2.reindex(catindexes)
projsum2 = projsum2.rename({'func': f'\textbf{{{categories[0]}}}', 'oo': f'\textbf{{{categories[1]}}}', 'proc': f'\textbf{{{categories[2]}}}', 'imp': f'\textbf{{{categories[3]}}}', 'mixed': '\textbf{Mixed}'})
projsum2 = projsum2.astype('float64')
common.save_table(projsum2.to_frame('no toy projects'), 'rq1-no-toy-projects', decimals=0, escape=False)

# %%
projsum3 = dfnodupes
projsum3 = projsum3.loc[dfnodupes['files_count'] == 1]

projsum3 = projsum3.groupby(['project']).sum()
projsum3 = common.compute_pcts(projsum3, categories)
projsum3['classified'] = projsum3.apply(common.classify_project, axis=1)
projsum3 = projsum3.groupby('classified').size()
for k in catindexes:
    if k not in projsum3: projsum3[k] = 0
projsum3 = projsum3.reindex(catindexes)
projsum3 = projsum3.rename({'func': f'\textbf{{{categories[0]}}}', 'oo': f'\textbf{{{categories[1]}}}', 'proc': f'\textbf{{{categories[2]}}}', 'imp': f'\textbf{{{categories[3]}}}', 'mixed': '\textbf{Mixed}'})
projsum3 = projsum3.astype('float64')
common.save_table(projsum3.to_frame('1-file projects'), 'rq1-onefile-projects', decimals=0, escape=False)

# %%
tab1 = projsum.to_frame('all projects')
tab2 = projsum2.to_frame('no toy projects')
tab3 = projsum3.to_frame('1-file projects')

common.save_table(tab1.join(tab2).join(tab3), 'rq1-3col-projects', decimals=0, escape=False)
