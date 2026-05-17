# applied_bigdata
Applied Big Data (Máster IA &amp; Big data, Linkiafp.es)

## Project folder structure
applied_bigdata/
├── src/
|    ├── activities/
|    |    ├── lesson_01/
|    |    |   ├── comparison/
|    |    |   |   ├── notebooks/
|    |    |   |   └── scripts/
|    |    |   ├── dataset/
|    |    |   |   └── ml-20m/
|    |    |   └── mongoplayground/
|    |    ├── lesson_02/
|    |    |   ├── comparison/
|    |    |   |   ├── notebooks/
|    |    |   |   └── scripts/
|    |    |   └── dataset/
|    |    └── lesson_03/
|    |    |   ├── dataset/
|    |    |   ├── notebooks/
|    |    |   ├── scripts/
|    |    |   └── README.md
|    |    ├── reports/
|    |    └── temp/
|    ├── config/
|    └── lessons/
|        ├── 20260413-02
|        ├── 20260508-06
|        └── 20260511-07
|            ├── checksum
|            ├── data-profiling
|            └── houses-models
├── scripts/
|   └── download_dataset.sh
├── .gitignore
├── LICENSE
└── README.md

## Datasets
This proyect use the following datasets
- MovieLens 20M

Download from:
https://grouplens.org/datasets/movielens/20m/
And after unzip in:
activities/lesson_01/dataset/

- Asteroid Dataset
Download from Kaggle:
https://gitlab.com/mirsakhawathossain/pha-ml/-/raw/master/Dataset/dataset.csv
Or download from <a href="https://ssd.jpl.nasa.gov/sbdb_query.cgi"><i>NASA JPL Small Body Search Engine</i></a>
https://ssd.jpl.nasa.gov/sbdb_query.cgi
 
And after unzip in:
activities/lesson_03/dataset/

## Technical requirements
### Python version
This is not a requirement but this project has been exectued opn Python v3.13, so it is higly recommended exectued it on that Python version
### Libraries
- setuptools (an obsolete library but necessary for the proper execution of the ydata-profiling)
pip install setuptools
- ydata-profiling, pygwalker and pandas (pandas library is necessary for the proper execution of the ydata-profiling)
pip install ydata-profiling pygwalker pandas