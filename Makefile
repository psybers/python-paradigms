PYTHON:=python3
ZIP:=zip

BOATOCSV:=$(PYTHON) data/boaToCsv.py
GENDUPES:=$(PYTHON) data/gendupes.py

ZIPOPTIONS:=-u -r
ZIPIGNORES:=-x \*/.DS_Store -x \*/.keep -x data/csv/\*.csv

.PHONY: all rqs data get-boa-output gendupes csvs update-figures package

all: data rqs

rqs: clean
	$(PYTHON) judgements.py
	$(PYTHON) cohens.py
	$(PYTHON) rq1.py
	$(PYTHON) rq2.py
	$(PYTHON) rq3.py
	$(PYTHON) rq4.py
	$(PYTHON) stats-table.py
	$(PYTHON) dupes.py

data: get-boa-output gendupes csvs

get-boa-output:
	./getdata.py

gendupes:
	$(GENDUPES) data/txt/hashes.txt > data/txt/dupes.txt

csvs: clean-pq
	$(BOATOCSV) -t '2,\.i?py(nb)?' data/txt/counts.txt > data/csv/counts.csv
	$(BOATOCSV) -t '2,\.i?py(nb)?' data/txt/dupes.txt > data/csv/dupes.csv
	$(BOATOCSV) -t '2,\.i?py(nb)?' data/txt/rq1.output.txt > data/csv/rq1.output.csv
	$(BOATOCSV) -t '2,\.i?py(nb)?' data/txt/rq2.output.txt > data/csv/rq2.output.csv
	$(BOATOCSV) -t '2,\.i?py(nb)?' data/txt/rq4.output.txt > data/csv/rq4.output.csv

update-figures:
	cd paper ; git pull ; rm -Rf figures/ tables/ ; cp -R ../figures . ; cp -R ../tables . ; git add figures/ tables/ ; git commit -m 'update figures/tables' ; git push

package:
	-$(ZIP) replication-pkg.zip $(ZIPOPTIONS) *.py LICENSE.txt Makefile README.md requirements.txt tables/ figures/ boa/ $(ZIPIGNORES)
	-$(ZIP) data-py.zip $(ZIPOPTIONS) data/ boa/ $(ZIPIGNORES)

.PHONY: clean clean-gen clean-pq clean-boa clean-zip clean-all

clean:
	rm -Rf __pycache__
	rm -f figures/*.pdf
	rm -f tables/*.tex

clean-gen:
	rm -f data/csv/*.csv

clean-pq:
	rm -f data/parquet/*.parquet

clean-boa:
	rm -f data/txt/*.txt

clean-zip:
	rm -f replication-pkg.zip data-py.zip

clean-all: clean clean-gen clean-pq clean-boa clean-zip
