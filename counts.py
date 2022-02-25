#!/usr/bin/env python3
# %%
import common
counts = common.get_counts().drop(['ppl_count'], axis=1)
common.save_table(counts.describe(), 'counts-dist', decimals=2, escape=True)
