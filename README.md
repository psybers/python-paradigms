# Replication Package
## An Exploratory Study on the Use of Programming Language Features in Python

This replication package contains all data and scripts needed to reproduce the results from the paper.

Note that all data was originally processed on a MacBook Pro with 2.6GHz 6-Core Intel Core i7 CPU and 32GB memory.  Some of the scripts (rq4) require substantial memory (around 55GB), but all are able to run on the 32GB MBP in about 12 minutes (when all Parquet files are pre-cached, or over an hour without).

TLDR: run `make rqs` to generate the tables/figures

------------------------------------------------------

### File Organization

Here is an overview of the folders layout.  The root contains scripts for generating tables/figures for the paper, and this `README.md` file.

The file `data/Python Classification - Data Science dataset.xlsx` contains the human classifications of some sample data, as well as the automated classification on that sample. The human inter-rater agreement Fleiss' kappa is also computed here, but the human-machine agreement Cohen's kappa is generated in a script.

#### Subdir: `boa`
These are the Boa queries used to generate data for the paper.

#### Subdir: `data`
This is the output of the Boa queries (the `.txt`) files, as well as processed versions of that output (`.csv` and `.parquet`).

#### Subdir: `figures`
Any generated figures (`.pdf`) will go into this folder.

#### Subdir: `tables`
Any generated tables (`.tex`) will go into this folder.

------------------------------------------------------

### Getting Boa Output

The first step is to run Boa queries to generate output data for further processing.

Here we provide instructions on manually getting the output, but it is probably easier to just run the helper script: `make get-boa-output`

#### Get some per-project counts
Run `boa/counts.boa` and save the output to `data/txt/counts.txt`.

#### Get file hashes for dupe checking
Run `boa/hashes.boa` and save the output to `data/txt/hashes.txt`.

Then run `make gendupes` to keep only the hashes for files with at least one dupe.  This generates `data/txt/dupes.txt`.

If you use the `make data` command instead of manually obtaining the outputs, you do not need to do anything else as it will call this target for you.

#### Get data for RQ1
Run `boa/rq1-proj-classify.boa` and save the output to `data/txt/rq1.output.txt`.

#### Get data for RQ2
Run `boa/rq2-features.boa` and save the output to `data/txt/rq2.output.txt`.

#### Get data for RQ4
Run `boa/rq4-evolution.boa` and save the output to `data/txt/rq4.output.txt`.

### Processing Boa Output

The Boa output is in a custom format, so first we convert it all into standard CSV format: `make csvs`

If you use the `make data` command instead of manually obtaining the outputs, you do not need to do anything else as it will call this target for you.

### Generating Figures and Tables

To generate all the figures and tables for the paper, you need to run the script for each specific research question on the output from Boa.

**Note: when you run these scripts, they load the Parquet files if they exist or fall back to loading CSV files. If you need to make any changes to the data, you will want to delete the Parquet files and regenerate the CSVs (`make csvs` does both) before you re-run these scripts.**

#### Generate the dataset statistics tables

> `python3 stats-table.py`

This generates the following:

- Table 2: `tables/py-dataset.tab.tex`
- Table 3: `tables/counts-dist.tab.tex`

> `python3 dupes.py`

This reports how many dupes were removed.

#### Generate the judgements table

> `python3 judgements.py`

This generates the following:

- Table 4: `tables/judgements.tab.tex`

#### Generate Cohen's kappa

> `python3 cohens.py`

This generates Cohen's kappa for inter-rater agreement between humans and machine.  Note the Fleiss' kappa (human inter-rater agreement) is generated inside the Excel spreadsheet.

#### RQ1: What is the distribution of programming paradigms for Python projects as a whole, and each individual file, on GitHub?

> `python3 rq1.py`

This generates the following:

- Figure 2: `figures/rq1-statement-dist.pdf`
- Figure 2: `tables/rq1-statement-dist.tab.tex`
- Figure 3: `figures/rq1-statement-pct.pdf`
- Figure 4: `figures/rq1-file-totals.pdf`
- Table 5: `tables/rq1-3col-projects.tab.tex`

#### RQ2: What are the most and least used features for each programming paradigm?

> `python3 rq2.py`

This generates the following:

- Table 6: `tables/rq2-project.tab.tex`

#### RQ3: Does project size (number of committers? number of files? number of statements? number of commits?) influence choice of programming paradigm?

> `python3 rq3.py`

This generates the following:

- Figure 5: `figures/rq3-hist-func.pdf`
- Figure 5: `figures/rq3-hist.pdf`
- Figure 6: `figures/rq3-ppl-hist.pdf`

#### RQ4: How does the programming paradigm choice change over time?

> `python3 rq4.py`

This generates the following:

- Table 7: `tables/rq4-evolution.tab.tex`
- Table 8: `tables/rq4-changed.tab.tex`
- Table 9: `tables/rq4-first.tab.tex`
- Table 9: `tables/rq4-last.tab.tex`
