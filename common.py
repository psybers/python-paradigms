import pandas as pd


def get_counts():
    try:
        counts = pd.read_parquet('data/parquet/counts.parquet')
    except:
        counts = pd.read_csv('data/csv/counts.csv', header=None, index_col=False, names=['var', 'project', 'count'])
        counts['count'] = pd.to_numeric(counts['count'], downcast='signed')
        counts.sort_values(by='project')

        counts_ast = counts.loc[counts['var'] == 'AST']
        counts_ast = counts_ast.drop(columns='var')
        counts_ast = counts_ast.rename(columns={'count': 'ast_count'})

        counts_revs = counts.loc[counts['var'] == 'REVS']
        counts_revs = counts_revs.drop(columns='var')
        counts_revs = counts_revs.rename(columns={'count': 'revs_count'})

        counts_files = counts.loc[counts['var'] == 'FILES']
        counts_files = counts_files.drop(columns='var')
        counts_files = counts_files.rename(columns={'count': 'files_count'})

        counts_ppl = counts.loc[counts['var'] == 'PPL']
        counts_ppl = counts_ppl.drop(columns='var')
        counts_ppl = counts_ppl.rename(columns={'count': 'ppl_count'})

        counts_stmts = counts.loc[counts['var'] == 'STMTS']
        counts_stmts = counts_stmts.drop(columns='var')
        counts_stmts = counts_stmts.rename(columns={'count': 'stmts_count'})

        counts = pd.merge(counts_ast, counts_revs, how='inner', on='project')
        counts = pd.merge(counts, counts_files, how='inner', on='project')
        counts = pd.merge(counts, counts_ppl, how='inner', on='project')
        counts = pd.merge(counts, counts_stmts, how='inner', on='project')

        counts.to_parquet('data/parquet/counts.parquet', compression='gzip')

    return counts


def get_data(filename, cols, drops=[], counts=None):
    df = pd.read_csv(filename, header=None, index_col=False, names=cols)
    df = df.drop(columns=drops)

    if 'commitdate' in df:
        df['commitdate'] = pd.to_numeric(df['commitdate'], downcast='signed')
        df['commitdate'] = pd.to_datetime(df['commitdate'], unit='us')

    if counts is not None:
        if 'commitdate' in df:
            df.sort_values(by=['project', 'file', 'commitdate'])
        else:
            df.sort_values(by=['project', 'file'])
        df = pd.merge(df, counts, how='outer', on='project')

    return df


def remove_dupes(df):
    try:
        df2 = pd.read_parquet('data/parquet/dupes.parquet')
    except:
        df2 = pd.read_csv('data/csv/dupes.csv', header=None, index_col=False, names=['var', 'hash', 'path'])
        df2[['project', 'file']] = df2['path'].str.extract('(.*)/blob/master/(.*)')
        df2 = df2.drop(columns=['var', 'path'])
        df2 = df2[df2.duplicated(subset=['hash'])]
        df2.to_parquet('data/parquet/dupes.parquet', compression='gzip')

    df2 = pd.merge(df, df2, how='left', left_on=['project', 'file'], right_on=['project', 'file'])
    # df2 consists of rows in df2 where 'hash' is 'NaN' (meaning that they did not exist in df2.duplicated(subset=['hash']))
    df2 = df2[pd.isnull(df2['hash'])].drop(columns=['hash'])

    return df2


def get_categories():
    return ['Functional', 'OO', 'Procedural', 'Imperative', 'Statements']

def get_cat_indexes():
    return ['func', 'oo', 'proc', 'imp', 'mixed']


def compute_pcts(df, categories):
    df['pct_func'] = df[categories[0]] / df[categories[4]]
    df['pct_oo'] = df[categories[1]] / df[categories[4]]
    df['pct_proc'] = df[categories[2]] / df[categories[4]]
    df['pct_imp'] = df[categories[3]] / df[categories[4]]
    return df


def split_categories(df, categories):
    df[[categories[0], categories[1], categories[2], categories[3], categories[4]]] = df['classification'].str.extract('{ (\d+), (\d+), (\d+), (\d+), (\d+) }')
    df = df.drop(columns='classification')

    for i in range(0, 5):
        df[categories[i]] = pd.to_numeric(df[categories[i]], downcast='signed')

    return compute_pcts(df, categories)


def classify_file(row):
    m = max(row.Functional, row.OO, row.Procedural, row.Imperative)

    if m == 0 or len([x for x in [row.Functional == m, row.OO == m, row.Procedural == m, row.Imperative == m] if x]) != 1:
        return 'mixed'

    if m == row.Procedural:
        return "proc"
    if m == row.Imperative:
        return "imp"
    if m == row.OO:
        return "oo"
    return "func"


def classify_all_projects(df):
    categories = get_categories()
    catindexes = get_cat_indexes()

    projsum = df.groupby(['project']).sum()
    projsum = compute_pcts(projsum, categories)
    projsum['classified'] = projsum.apply(classify_project, axis=1)
    projsum = projsum.groupby('classified').size()
    projsum = projsum.astype('float64')
    for k in catindexes:
        if k not in projsum:
            projsum[k] = 0
    projsum = projsum.reindex(catindexes)
    projsum = projsum.rename({'func': f'\textbf{{{categories[0]}}}',
                              'oo': f'\textbf{{{categories[1]}}}',
                              'proc': f'\textbf{{{categories[2]}}}',
                              'imp': f'\textbf{{{categories[3]}}}',
                              'mixed': '\textbf{Mixed}'})
    return projsum

def classify_project(row):
    if row.Statements == 0:
        return 'mixed'

    pcts = [row.pct_func, row.pct_oo, row.pct_proc, row.pct_imp]
    pcts.sort()

    if pcts[-2] > 2/3 or pcts[-1] < 1/3:
        return 'mixed'
    if pcts[-2] > 0.5 and pcts[-1] - pcts[-2] < 0.2:
        return 'mixed'
    if pcts[-1] <= 0.5 and pcts[-1] - pcts[-2] < 0.1:
        return 'mixed'

    if pcts[-1] == row.pct_func:
        return "func"
    if pcts[-1] == row.pct_oo:
        return "oo"
    if pcts[-1] == row.pct_proc:
        return "proc"
    return "imp"


def filter_projects(df):
#   df = df.loc[df['files_count'] > 1]
#   df = df.loc[df['revs_count'] > 10]
    df = df.dropna()
    return df


colsepname = ''
def save_table(df, filename, decimals=2, dropheader=False, colsep=False, **kwargs):
    global colsepname
    if not colsep is False:
        colsepname = colsepname + 'A'

    pd.options.display.float_format = ('{:,.' + str(decimals) + 'f}').format

    with pd.option_context("max_colwidth", 1000):
        tab1 = df.to_latex(**kwargs)

    if dropheader:
        lines = tab1.splitlines()
        tab1 = '\n'.join(lines[0:2] + lines[lines.index('\\midrule') + 1:])

    print(tab1)
    with open('tables/' + filename + '.tab.tex', 'w', encoding='utf-8') as f:
        f.write('% DO NOT EDIT\n')
        f.write('% this file was automatically generated\n')
        if not colsep is False:
            f.write('\\newcommand{\\oldtabcolsep' + colsepname + '}{\\tabcolsep}\n')
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + '}\n')
        f.write(tab1)
        if not colsep is False:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + colsepname + '}\n')
