import polars as pl
import time

timeInit = time.time()
df_movies = pl.read_csv('../dataset/ml-20m/movies.csv')
timeEnd = time.time()

print(f"Time to load the dataset with Polars: {timeEnd - timeInit:.4f} seconds")
print(df_movies.head())