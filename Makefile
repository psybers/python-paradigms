rqs: clean
	python3 judgements.py &
	python3 cohens.py &
	python3 rq2.py
	python3 rq4.py &
	python3 rq1.py
	python3 rq3.py &
	python3 counts.py &
	python3 stats-table.py

all: data rqs

data: getdata gendupes csv

getdata:
	./getdata.py

gendupes:
	python3 data/gendupes.py data/txt/hashes.txt > data/txt/dupes.txt

csv: rmparquet
	python3 data/boaToCsv.py -t '2,\.i?py(nb)?' data/txt/counts.txt > data/csv/counts.csv
	python3 data/boaToCsv.py -d 1 -t '2,\.i?py(nb)?' data/txt/dataset-stats-main.txt > data/csv/dataset-stats-main.csv
	python3 data/boaToCsv.py -d 1 -t '2,\.i?py(nb)?' data/txt/dataset-stats.txt > data/csv/dataset-stats.csv
	python3 data/boaToCsv.py -t '2,\.i?py(nb)?' data/txt/dupes.txt > data/csv/dupes.csv
	python3 data/boaToCsv.py -t '2,\.i?py(nb)?' data/txt/rq1.output.txt > data/csv/rq1.output.csv
	python3 data/boaToCsv.py -t '2,\.i?py(nb)?' data/txt/rq2.output.txt > data/csv/rq2.output.csv
	python3 data/boaToCsv.py -t '2,\.i?py(nb)?' data/txt/rq4.output.txt > data/csv/rq4.output.csv

rmparquet:
	rm -f data/parquet/*

package:
	zip -r replication-pkg.zip Makefile *.py LICENSE.txt README.md tables/ figures/ data/ boa/ -x \*/.DS_Store

clean:
	rm -Rf __pycache__
	rm -f figures/*
	rm -f tables/*
